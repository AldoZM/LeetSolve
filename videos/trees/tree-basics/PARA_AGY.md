# Guía de árboles: estado y pasos para terminarla

Video de árboles en dos formatos, a partir del guion `GUION_VISUAL_ARBOLES.md`:

- `largo/`: horizontal 16:9 para YouTube, 63 líneas, 6:23.
- `corto/`: vertical 9:16, un gancho de unos 74 s que invita a ver el largo.

Los dos comparten `comun.py`. Lee primero `GUIA.md` (formato 16:9 y "un video en dos formatos") y `RENDER.md`.

## Reglas de Aldo

- Un render a la vez: nunca dos `build.py`, ni voz y render juntos.
- Assets reales del juego, nunca inventados.
- Sin fechas en la narración.
- Los commits van sin firma de IA.

## Estado (2026-10-24)

| Paso | Largo | Corto |
|---|---|---|
| Narración | lista | lista |
| Voz (`voiceover.mp3`, `timestamps.json`) | lista, 383.3 s | **falta** (8 de 13 líneas ya están en `.tts-cache`) |
| `make_walk.py` → `walk.json` | listo | no lleva |
| Linter | sin problemas | **falta** |
| Escenas de Manim | renderizadas y revisadas | **falta** |
| Mundo 3D (`media/three/fondo.mp4`) | renderizado completo | **falta** |
| Composición, sincronía, mezcla | escenas 1 a 4 compuestas; se detuvo en la 5 | **falta** |
| Video final | **falta** | **falta** |

## Para terminar el largo (desde `videos/trees/tree-basics/largo`)

Si estás en la Mac de Aldo, el mundo 3D y las escenas ya están. Solo falta:

```bash
export PATH="$HOME/.manim-skill-src/.venv/bin:$HOME/Library/TinyTeX/bin/universal-darwin:$HOME/.local/bin:$PATH" PYTHONUTF8=1
python ../../../../herramientas/build.py composite sync mux
```

En otra PC (sin `media/`) corre todo, menos la voz, que ya está:

```bash
python make_walk.py
python ../../../../herramientas/build.py script lint render three composite sync mux
```

Al terminar:

1. Revisa el video con hojas de cuadros y el loop (el primer cuadro debe ser igual al último).
2. Renómbralo a `How Trees Really Work.mp4` y cópialo a `export/`.

## Para hacer el corto (desde `videos/trees/tree-basics/corto`)

```bash
PYTHONUTF8=1 ~/.manim-skill-src/.venv-tts/bin/python ../../../../pruebas/voces_demo/tts_qwen_clone.py .
python ../../../../herramientas/build.py script lint render three composite sync mux
```

- Solo se generan las 5 líneas nuevas: el gancho, la del corte con tijeras, "Stand on one block…", "Change only the last line…" y la invitación final.
- Si el linter marca líneas pasadas de tiempo, adelanta los `until(at(...))` anclados a la última palabra.
- Revisa con hojas de cuadros. Lo que más hay que vigilar: que nada se salga del cuadro de 9 × 12 ni tape el código.
- Renómbralo a `How Trees Really Work (Short).mp4` y cópialo a `export/`.

## Pendientes de diseño ya decididos

- Lugar: `birch-grove` (MacEntorno), de día, con ovejas, vacas, gallinas y un lobo. Ya está en `mundos/lugares.json`.
- En las partes 3D del largo la niebla se acerca (de 16 a 62) para que el bosque quede suave detrás del árbol.
- Objetos usados: tijeras (`shears`), rienda (`lead`), tolva (`hopper`), brote (`oak_sapling`), cofres para las carpetas y la cola, y barreras para `None`.
- Para correr `extraer.py` en otra PC: copia los nuevos objetos y los sonidos `shear` y `lead_tie`.

## Copia en Google Drive (DevSteve → Por terminar → Guia de arboles (tree-basics))

Carpeta: https://drive.google.com/drive/folders/1A47mqzlu-eJTmv6KIwwySiwjoKDY2rL0

Claude subió con `rclone` la carpeta `videos/trees/tree-basics` completa:

- Código, narraciones, voz del largo (`voiceover.mp3`, `timestamps.json`, `walk.json`) y los dos `.tts-cache`.
- Todo lo renderizado del largo, en `largo/media/`:
  - `three/fondo.mp4`: el mundo 3D completo, 790 MB.
  - Las 11 escenas de Manim, transparentes (`videos/script/1080p30/*.mov`).
  - Las escenas 1 a 4 ya compuestas (`*.mp4`).
  - Los efectos de sonido de cada escena (`sfx/*.json`).
- Con esa carpeta `media/` en su lugar, terminar el largo es solo `build.py composite sync mux`. Primero corre `build.py script`: `script.py` lleva la ruta local y no se sube. **No corras `lint`**, porque reescribe los `sfx/*.json` (ver GUIA.md).

Para trabajar con esa copia, ponla en `videos/trees/tree-basics/` de un clon del repo (rama `main`).
