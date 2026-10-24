# Cómo renderizar un video cuyo código ya está listo

Este documento sirve cuando un video ya tiene todos sus archivos escritos (narración, voz, escenas, recorrido y página 3D) y solo falta generar el `video.mp4`. Para crear un video desde cero, ver `INSTRUCCIONES_IA.md`. El contexto completo está en `GUIA.md`.

## 1. Qué debe tener la carpeta del video

En `videos/<sección>/<número>-<nombre>/`:

| Archivo | Para qué | Si falta |
|---|---|---|
| `narration.txt` | líneas de la voz | el video no está listo |
| `timestamps.json` | duración exacta de cada línea | correr el TTS (paso 3) |
| `voiceover.mp3` | la voz (no se sube a git) | correr el TTS (paso 3) |
| `walk.json` | tiempos del recorrido | `python make_walk.py` |
| `video.json` | grupos de escenas, tema, formato y fondo | el video no está listo |
| `scenes.py` | escenas de Manim | el video no está listo |
| `three/mundo.html` | el mundo 3D y el recorrido | el video no está listo |
| `script.py` | se genera solo (paso `script`) | no hace falta |

`script.py` es `prelude.py` + tema + `scenes.py` y lleva la ruta local del tema. Desde el lote #8–#19 no se sube a git (tenía el usuario de la PC); `build.py` lo vuelve a crear.

## 2. Preparar la PC (una sola vez)

Lista completa en `INSTRUCCIONES_IA.md`, sección 2. Lo mínimo:

```bash
export PATH="$HOME/.manim-skill-src/.venv/Scripts:$PATH" PYTHONUTF8=1   # en cada terminal
python herramientas/temas/minecraft-original/extraer.py                 # texturas, interfaz, sonidos, mobs y música del juego
cd herramientas/three && npm ci && npx playwright install chromium && cd ../..
```

Texturas de los lugares (`mundos/tex/`, no se suben). Los 6 lugares del lote #8–#19 se exportaron del mundo de la laptop (Minecraft 26.3), que no viene en `ClaudeEntorno.zip`. No hace falta ese mundo: las texturas se copian del jar del juego con los nombres que ya traen los `.json`. Desde `herramientas/temas/minecraft-original`:

```bash
python -c "import json,glob,mundo; n=set(); [n.update(json.load(open(f,encoding='utf8')).get('names',[])) for f in glob.glob('mundos/*.json') if 'lugares' not in f]; mundo.block_textures(sorted(n),'mundos/tex')"
```

Si el terreno sale con huecos o bloques sin textura, falta este paso.

## 3. Voz (solo si falta `voiceover.mp3`)

`voiceover.mp3` no se sube a git. Desde la carpeta del video:

```bash
python "$HOME/.manim-skill-src/skills/manim-skill/tools/tts-generate.py" --narration narration.txt
python make_walk.py
```

Las duraciones pueden variar unas centésimas respecto a las de `timestamps.json` del repositorio; `make_walk.py` recalcula los eventos con las nuevas. Revisa que el número de clips sea igual al de líneas y que la duración total siga debajo de 3 minutos.

## 4. Render

Desde la carpeta del video:

```bash
python ../../../herramientas/build.py
```

Sin argumentos corre los 7 pasos en orden. Se pueden correr sueltos, y cada uno usa lo que dejó el anterior:

| Paso | Qué hace | Deja |
|---|---|---|
| `script` | pega `prelude.py` + tema + `scenes.py` | `script.py` |
| `lint` | simula las escenas y revisa que cada línea quepa en su tiempo | nada (falla si algo se pasa) |
| `render` | renderiza las escenas de Manim en paralelo (transparentes) | `media/videos/script/1440p30/*.mp4` |
| `three` | renderiza el clip 3D de todo el video con Chromium | `media/three/fondo.mp4` |
| `composite` | pone cada escena sobre su tramo del mundo (desenfocado o nítido) | escenas compuestas en `media/` |
| `sync` | corta cada escena a sus cuadros exactos y arma los subtítulos | `media/synced/*.mp4` y `.srt` |
| `mux` | une todo, mezcla voz, efectos y música | `video_silent.mp4`, `video.mp4` |

- El paso `three` es el más largo (renderiza cuadro por cuadro todo el video). `render` también tarda, porque son 7 escenas en paralelo.
- Para rehacer una sola escena: `python ../../../herramientas/build.py script lint render Scene4_Idea sync Scene4_Idea mux`.
- Si se cambió solo `three/mundo.html`: `build.py three composite sync mux`.
- Si se cambió solo la música o los volúmenes: `build.py mux`.
- **Si el render se interrumpe**, vuelve a empezar desde el paso que quedó a medias y sigue con los demás. El paso a medias se sabe por los archivos que dejó (tabla de arriba) y por `build.log`. `sync` y `mux` siempre se pueden repetir completos.
- Los registros de cada escena quedan en `media/log_<Escena>.txt`. Si una escena falla por la caché de texto de Manim, `build.py` la reintenta sola; si falla otra vez, corre solo esa escena.
- **Un render a la vez** (regla de Aldo, 2026-10-23): no se lanza otro video (ni su voz con Qwen3-TTS) hasta que el anterior termine su `mux`. En la Mac de 8 GB dos renders juntos se quedan sin memoria y se hace un cuello de botella.

Al final `build.py` imprime `video.mp4 duration X audio Y`: las dos deben coincidir.

## 5. Revisar antes de dar el video por terminado

Lista completa en `GUIA.md`, "Lista de revisión antes de entregar". En corto:

1. Duración del video igual a la del audio.
2. Hojas de cuadros de cada escena y revisarlas mirando las imágenes: `python ../../../herramientas/sheet.py hoja.png 3 --video video.mp4 1,5,12,20,...`
3. Los 15 "Errores ya cometidos" de `GUIA.md`, uno por uno.
4. Loop: primer y último cuadro con diferencia media menor a 1 (o solo ruido en los bordes).
5. Ver el video en el visor: `python "$HOME/.manim-skill-src/skills/manim-skill/tools/video_viewer.py" video.mp4 --order concat.txt --script script.py --port 8081`
6. Renombrar `video.mp4` a `<Título> #<número>.mp4` en su carpeta y copiarlo a `export/`, y escribir `descripcion.txt` (100 caracteres o menos).
7. Agregar el resultado a "Videos hechos" de `GUIA.md` y a `BITACORA.md`.

## 6. Estado del lote #8–#19 (2026-10-21)

Todo el código está en git. Los renders de la laptop no se suben; en otra PC hay que correr todo (`build.py` sin argumentos, después de los pasos 2 y 3).

| Video | Carpeta | En la laptop | Qué falta |
|---|---|---|---|
| #8 String to Integer | `videos/strings/0008-string-to-integer` | `video.mp4` completo, 95.2 s (video = audio), 49 efectos | revisión (paso 5) |
| #9 Palindrome Number | `videos/math/0009-palindrome-number` | `video.mp4` completo, 91.3 s (video = audio), 46 efectos | revisión (paso 5) |
| #16 3Sum Closest | `videos/two-pointers/0016-three-sum-closest` | `video.mp4` completo, 102.1 s (video = audio), 63 efectos | revisión (paso 5) |
| #17 Letter Combinations | `videos/backtracking/0017-letter-combinations` | `video.mp4` completo, 90.3 s (video = audio), 86 efectos | revisión (paso 5) |
| #18 4Sum | `videos/two-pointers/0018-four-sum` | `video.mp4` completo, 104.5 s (video = audio) | revisión (paso 5) |
| #19 Remove Nth Node | `videos/linked-list/0019-remove-nth-node` | `video.mp4` completo, 84.27 s (audio 84.25 s, menos de un cuadro) | revisión (paso 5) |

- En #18 y #19 el clip 3D no se revisó con cuadros sueltos antes de renderizarlo. Al renderizar en otra PC, conviene probarlo antes del paso `three`: `node ../../../herramientas/three/render.mjs --page three/mundo.html --tema ../../../herramientas/temas/minecraft-original --stills 2,40,60 --outdir review3d` (con `--height 1920` para ver el 9:16).
- Los 6 videos se hicieron con subagentes en paralelo. Una caída de red los detuvo antes de terminar su revisión, así que ninguno tiene hojas de cuadros revisadas ni `NOTAS.md`. Los renders de #18 y #19 se terminaron después a mano.
- Los videos terminados se copian a `export/` (raíz, no se sube) como `<Título> #<número>.mp4`.
