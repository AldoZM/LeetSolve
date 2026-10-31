#!/usr/bin/env python3
"""
Minecraft Structure and Biome Locator
Herramienta para localizar aldeas, biomas y estructuras en mundos de Minecraft (Java Edition).
Diseñada para uso tanto por usuarios como por agentes de IA (Claude, Antigravity, etc.).
"""

import os
import sys
import json
import zlib
import gzip
import struct
import shutil
import tempfile
import argparse
import subprocess
from pathlib import Path

# The game's folder on each system (same rule as extraer.py)
if os.name == "nt":
    DEFAULT_MC_DIR = Path(os.path.expandvars(r"%APPDATA%\.minecraft"))
elif sys.platform == "darwin":
    DEFAULT_MC_DIR = Path.home() / "Library" / "Application Support" / "minecraft"
else:
    DEFAULT_MC_DIR = Path.home() / ".minecraft"
SAVES_DIR = DEFAULT_MC_DIR / "saves"

# -------------------------------------------------------------
# Parser NBT Básico y Rápido
# -------------------------------------------------------------

def parse_payload(stream, tag_type):
    if tag_type == 1:
        return struct.unpack('>b', stream.read(1))[0]
    elif tag_type == 2:
        return struct.unpack('>h', stream.read(2))[0]
    elif tag_type == 3:
        return struct.unpack('>i', stream.read(4))[0]
    elif tag_type == 4:
        return struct.unpack('>q', stream.read(8))[0]
    elif tag_type == 5:
        return struct.unpack('>f', stream.read(4))[0]
    elif tag_type == 6:
        return struct.unpack('>d', stream.read(8))[0]
    elif tag_type == 7:
        length = struct.unpack('>i', stream.read(4))[0]
        return stream.read(length)
    elif tag_type == 8:
        length = struct.unpack('>H', stream.read(2))[0]
        return stream.read(length).decode('utf-8', errors='replace')
    elif tag_type == 9:
        sub_type = stream.read(1)[0]
        length = struct.unpack('>i', stream.read(4))[0]
        return [parse_payload(stream, sub_type) for _ in range(length)]
    elif tag_type == 10:
        res = {}
        while True:
            sub = stream.read(1)
            if not sub or sub == b'\x00':
                break
            st = sub[0]
            nl = struct.unpack('>H', stream.read(2))[0]
            name = stream.read(nl).decode('utf-8', errors='replace')
            res[name] = parse_payload(stream, st)
        return res
    elif tag_type == 11:
        length = struct.unpack('>i', stream.read(4))[0]
        return struct.unpack(f'>{length}i', stream.read(length * 4))
    elif tag_type == 12:
        length = struct.unpack('>i', stream.read(4))[0]
        return struct.unpack(f'>{length}q', stream.read(length * 8))
    else:
        raise ValueError(f"Tag NBT desconocido: {tag_type}")

def read_nbt(path):
    with open(path, 'rb') as f:
        magic = f.read(2)
        f.seek(0)
        raw = gzip.decompress(f.read()) if magic == b'\x1f\x8b' else f.read()
    
    stream = io_bytes = (raw if isinstance(raw, bytes) else bytes(raw))
    import io
    bio = io.BytesIO(stream)
    tag_type = bio.read(1)
    if not tag_type or tag_type == b'\x00':
        return None, {}
    name_len = struct.unpack('>H', bio.read(2))[0]
    name = bio.read(name_len).decode('utf-8', errors='replace')
    payload = parse_payload(bio, tag_type[0])
    return name, payload

# -------------------------------------------------------------
# Información del Mundo
# -------------------------------------------------------------

def get_world_info(world_path):
    world_path = Path(world_path)
    if not world_path.exists():
        return None
    
    level_dat = world_path / "level.dat"
    if not level_dat.exists():
        return None

    _, ldata = read_nbt(level_dat)
    data = ldata.get("Data", {})

    # Semilla (Seed)
    seed = None
    gen_settings_file = world_path / "data" / "minecraft" / "world_gen_settings.dat"
    if gen_settings_file.exists():
        _, gdata = read_nbt(gen_settings_file)
        seed = gdata.get("data", {}).get("seed")
    if seed is None:
        seed = data.get("WorldGenSettings", {}).get("seed")
        if seed is None:
            seed = data.get("RandomSeed")

    # Posición del jugador
    player_pos = None
    players_data_dir = world_path / "players" / "data"
    if players_data_dir.exists():
        dats = list(players_data_dir.glob("*.dat"))
        if dats:
            # Archivo más recientemente modificado
            latest = max(dats, key=os.path.getmtime)
            _, pdata = read_nbt(latest)
            player_pos = pdata.get("Pos")
    
    if player_pos is None and "Player" in data:
        player_pos = data["Player"].get("Pos")

    # Spawn
    spawn = (
        data.get("spawn", {}).get("pos") or
        (data.get("SpawnX", 0), data.get("SpawnY", 64), data.get("SpawnZ", 0))
    )

    version_name = data.get("Version", {}).get("Name", "Desconocida")
    level_name = data.get("LevelName", world_path.name)

    return {
        "world_name": level_name,
        "world_path": str(world_path),
        "seed": seed,
        "spawn": list(spawn) if spawn else [0, 64, 0],
        "player_pos": [round(c, 1) for c in player_pos] if player_pos else None,
        "version": version_name,
        "data_version": data.get("DataVersion")
    }

def list_worlds():
    if not SAVES_DIR.exists():
        return []
    worlds = []
    for entry in SAVES_DIR.iterdir():
        if entry.is_dir() and (entry / "level.dat").exists():
            info = get_world_info(entry)
            if info:
                worlds.append(info)
    return worlds

# -------------------------------------------------------------
# Motor de Localización (Minecraft Java Headless)
# -------------------------------------------------------------

def find_bundled_java_and_jar(version_name="26.3"):
    versions_dir = DEFAULT_MC_DIR / "versions"
    target_ver = version_name if (versions_dir / version_name).exists() else None
    if not target_ver:
        # Tomar la versión más reciente disponible
        candidates = [d.name for d in versions_dir.iterdir() if d.is_dir() and (d / f"{d.name}.jar").exists()]
        if not candidates:
            return None, None, []
        target_ver = sorted(candidates, reverse=True)[0]

    jar_path = versions_dir / target_ver / f"{target_ver}.jar"
    json_path = versions_dir / target_ver / f"{target_ver}.json"

    # Java runtime
    runtime_dir = DEFAULT_MC_DIR / "runtime"
    java_bins = list(runtime_dir.glob("**/bin/java.exe" if os.name == "nt" else "**/bin/java"))
    java_bin = str(java_bins[0]) if java_bins else "java"

    # Classpath
    libs = [str(jar_path)]
    if json_path.exists():
        with open(json_path) as f:
            vdata = json.load(f)
        for lib in vdata.get("libraries", []):
            rel = lib.get("downloads", {}).get("artifact", {}).get("path")
            if rel:
                lp = DEFAULT_MC_DIR / "libraries" / rel
                if lp.exists():
                    libs.append(str(lp))

    return java_bin, str(jar_path), libs

def query_minecraft_structures(world_path, queries, dimension="overworld"):
    """
    Ejecuta consultas de estructuras y biomas usando el motor nativo de Minecraft en un entorno aislado.
    queries: lista de tuplas (x, z, query_cmd)
    """
    world_info = get_world_info(world_path)
    if not world_info:
        raise ValueError(f"No se pudo leer la información del mundo en: {world_path}")

    java_bin, jar_path, libs = find_bundled_java_and_jar(world_info.get("version", "26.3"))
    if not libs:
        raise RuntimeError("No se encontraron las librerías de Minecraft instaladas.")

    cp = os.pathsep.join(libs)  # ":" on Mac and Linux, ";" on Windows

    # Crear directorio temporal aislado para no tocar el mundo real
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_world = Path(tmp_dir) / "saves" / "World"
        tmp_world.mkdir(parents=True)

        # Copiar solo metadatos necesarios
        shutil.copy(Path(world_path) / "level.dat", tmp_world / "level.dat")
        data_dir = Path(world_path) / "data"
        if data_dir.exists():
            shutil.copytree(data_dir, tmp_world / "data")

        # Configuración del servidor temporal
        with open(Path(tmp_dir) / "eula.txt", "w") as f:
            f.write("eula=true\n")
        with open(Path(tmp_dir) / "server.properties", "w") as f:
            f.write("online-mode=false\nserver-port=25592\nlevel-name=World\n")

        dim_str = "minecraft:the_nether" if dimension == "nether" else ("minecraft:the_end" if dimension == "end" else "minecraft:overworld")

        commands = []
        for x, z, qcmd in queries:
            commands.append(f"execute in {dim_str} positioned {int(x)} 64 {int(z)} run {qcmd}")
        commands.append("stop")

        cmd = [java_bin, "-Xmx1G", "-cp", cp, "net.minecraft.server.Main", "--nogui"]
        proc = subprocess.Popen(
            cmd,
            cwd=tmp_dir,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        output_lines = []
        sent = False
        import time
        start = time.time()
        while time.time() - start < 40:
            line = proc.stdout.readline()
            if not line and proc.poll() is not None:
                break
            if line:
                output_lines.append(line.strip())
                if "Done" in line and not sent:
                    for c in commands:
                        proc.stdin.write(c + "\n")
                    proc.stdin.flush()
                    sent = True

        results = []
        import re
        pat = re.compile(r"The nearest (?:#)?([a-zA-Z0-9_:]+) (?:(?:\(([a-zA-Z0-9_:]+)\) )?)is at \[(-?\d+), (?:~|-?\d+), (-?\d+)\]")
        for line in output_lines:
            match = pat.search(line)
            if match:
                stype = match.group(2) if match.group(2) else match.group(1)
                bx = int(match.group(3))
                bz = int(match.group(4))
                results.append({
                    "target": stype,
                    "x": bx,
                    "z": bz,
                    "dimension": dimension,
                    "raw_output": line
                })

        return results

# -------------------------------------------------------------
# Interfaz CLI
# -------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Minecraft Structure & Biome Locator")
    subparsers = parser.add_subparsers(dest="subcommand", help="Comandos disponibles")

    # list
    subparsers.add_parser("list", help="Lista los mundos disponibles en saves/")

    # locate
    p_loc = subparsers.add_parser("locate", help="Localiza aldeas y estructuras")
    p_loc.add_argument("--world", "-w", required=True, help="Nombre del mundo (ej. MacEntorno, ClaudeEntorno) o ruta completa")
    p_loc.add_argument("--dimension", "-d", default="overworld", choices=["overworld", "nether", "end"], help="Dimensión a consultar")
    p_loc.add_argument("--type", "-t", default="all", choices=["village", "all", "structures", "biomes"], help="Tipo de búsqueda")
    p_loc.add_argument("--pos", nargs=2, type=int, metavar=("X", "Z"), help="Coordenadas de referencia en la dimensión")
    p_loc.add_argument("--json", action="store_true", help="Salida en formato JSON para herramientas/agentes")

    args = parser.parse_args()

    if args.subcommand == "list" or not args.subcommand:
        worlds = list_worlds()
        if getattr(args, "json", False):
            print(json.dumps(worlds, indent=2))
        else:
            print("\n=== MUNDOS DETECTADOS EN MINECRAFT ===")
            for w in worlds:
                print(f"- {w['world_name']} ({w['version']})")
                print(f"  Semilla: {w['seed']}")
                print(f"  Spawn: {w['spawn']}")
                print(f"  Jugador: {w['player_pos']}\n")
        return

    if args.subcommand == "locate":
        wpath = Path(args.world)
        if not wpath.exists():
            wpath = SAVES_DIR / args.world
            if not wpath.exists():
                print(f"Error: No se encontró el mundo '{args.world}' en {SAVES_DIR}", file=sys.stderr)
                sys.exit(1)

        winfo = get_world_info(wpath)
        dim = args.dimension

        # Coordenadas de referencia
        if args.pos:
            ref_x, ref_z = args.pos[0], args.pos[1]
        elif dim == "nether":
            # Si estamos en Nether, calcular la posición relativa del jugador (/8) o portal
            if winfo["player_pos"]:
                ref_x = int(winfo["player_pos"][0] // 8)
                ref_z = int(winfo["player_pos"][2] // 8)
            else:
                ref_x, ref_z = 0, 0
        else:
            ref_x = winfo["player_pos"][0] if winfo["player_pos"] else winfo["spawn"][0]
            ref_z = winfo["player_pos"][2] if winfo["player_pos"] else winfo["spawn"][2]

        queries = []
        if dim == "nether":
            if args.type in ["all", "structures"]:
                queries.append((ref_x, ref_z, "locate structure minecraft:fortress"))
                queries.append((ref_x, ref_z, "locate structure minecraft:bastion_remnant"))
            if args.type in ["all", "biomes"]:
                for b in ["crimson_forest", "warped_forest", "soul_sand_valley", "basalt_deltas", "nether_wastes"]:
                    queries.append((ref_x, ref_z, f"locate biome minecraft:{b}"))
        elif dim == "end":
            if args.type in ["all", "structures"]:
                queries.append((ref_x, ref_z, "locate structure minecraft:end_city"))
        else:
            # Overworld
            if args.type in ["village", "all"]:
                offsets = [
                    (0, 0), (1000, 0), (-1000, 0), (0, 1000), (0, -1000),
                    (1200, 1200), (-1200, 1200), (1200, -1200), (-1200, -1200),
                    (2000, 0), (-2000, 0), (0, 2000), (0, -2000)
                ]
                for dx, dz in offsets:
                    queries.append((ref_x + dx, ref_z + dz, "locate structure #minecraft:village"))

            if args.type in ["structures", "all"]:
                other_structs = [
                    "stronghold", "trial_chambers", "ancient_city",
                    "monument", "mansion", "pillager_outpost"
                ]
                for s in other_structs:
                    queries.append((ref_x, ref_z, f"locate structure minecraft:{s}"))

        results = query_minecraft_structures(wpath, queries, dimension=dim)

        # Desduplicar
        unique = {}
        import math
        for r in results:
            key = (r["target"], r["x"], r["z"])
            if key not in unique:
                dist = math.hypot(r["x"] - ref_x, r["z"] - ref_z)
                r["dist_ref"] = round(dist, 1)
                dim_arg = f"in minecraft:the_nether " if dim == "nether" else ("in minecraft:the_end " if dim == "end" else "")
                r["tp_command"] = f"/execute {dim_arg}run tp {r['x']} ~ {r['z']}"
                unique[key] = r

        sorted_res = sorted(unique.values(), key=lambda x: x["dist_ref"])

        output_data = {
            "world": winfo,
            "dimension": dim,
            "reference_position": [ref_x, ref_z],
            "total_found": len(sorted_res),
            "results": sorted_res
        }

        if args.json:
            print(json.dumps(output_data, indent=2))
        else:
            print(f"\n=== RESULTADOS EN {dim.upper()} PARA: {winfo['world_name']} ===")
            print(f"Semilla: {winfo['seed']} | Referencia: X: {int(ref_x)}, Z: {int(ref_z)}\n")
            print(f"{'Estructura / Bioma':<32} | {'X':>6} | {'Z':>6} | {'Distancia':>10} | Comando")
            print("-" * 80)
            for s in sorted_res:
                print(f"{s['target']:<32} | {s['x']:>6} | {s['z']:>6} | {int(s['dist_ref']):>9}m | {s['tp_command']}")

if __name__ == "__main__":
    main()
