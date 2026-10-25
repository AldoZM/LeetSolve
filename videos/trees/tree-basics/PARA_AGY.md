# Guía de árboles: estado y pasos para terminarla

Video de árboles en varios formatos, a partir del guion `GUION_VISUAL_ARBOLES.md`:

- `largo/`: horizontal 16:9 para YouTube, 63 líneas, 6:23. **Terminado** (2026-10-24, en la PC de Windows).
- `shorts/`: cinco Shorts 9:16 cortados del largo, con su voz, que se cortan a la mitad y terminan en un letrero "FULL VIDEO / ON YOUTUBE". Muestra hecha: `shorts/02-dfs`.
- `corto/`: tráiler vertical de unos 74 s con voz nueva. Queda aparte.

Todos comparten `comun.py`. Lee primero `GUIA.md` (formato 16:9, "un video en dos formatos" y "Shorts recortados de un video largo") y `RENDER.md`.

## Reglas de Aldo

- Un render a la vez: nunca dos `build.py`, ni voz y render juntos.
- Assets reales del juego, nunca inventados.
- Sin fechas en la narración.
- Los commits van sin firma de IA.

## Estado (2026-10-24, noche)

- **Largo:** terminado, 383.3 s, 151 efectos. `How Trees Really Work.mp4` en `largo/` y en `export/` (solo en la PC de Windows; los `.mp4` no se suben). Falta que Aldo lo vea en movimiento y escuche la mezcla.
- **Shorts** (los cinco cortes y sus líneas están en `BITACORA.md`, 2026-10-24 noche):
  - `02-dfs` (líneas 20 a 25): muestra hecha, 48.27 s. Falta que Aldo la apruebe.
  - `01` tijeras (12 a 18), `03` por niveles (29 a 31, cortando la 31 en "whose turn it is?"), `04` árbol de búsqueda (35 a 41) y `05` recursión y secreto (49 a 57): **faltan**.
  - Falta `descripcion.txt` de cada uno.
- **Corto (tráiler):** narración, `scenes.py` y `three/mundo.html` listos; falta la voz (8 de 13 líneas ya están en `.tts-cache`), el linter, el render y la composición.

## Para hacer otro short (desde `videos/trees/tree-basics/shorts/<nn>-<nombre>`)

1. `python ../make_short.py FIRST LAST`: escribe `timestamps.json`, `voiceover.mp3` (el tramo del largo más 3.5 s de silencio), `narration.txt` y copia `walk.json`. Necesita `largo/voiceover.mp3` (está en la copia de Drive).
2. Copiar de `02-dfs` `video.json`, `scenes.py` y `three/mundo.html`, y cambiar:
   - `video.json`: las líneas del tramo y la línea del letrero (63).
   - `three/mundo.html`: la parte del largo que toca (`anatomy`, `dfs` o `bst` de `largo/three/mundo.html`), con el árbol ya armado. Si el short no usa 3D nítido, basta el paseo de `corto/three/mundo.html` más el plano `shade` del letrero.
   - `scenes.py`: la escena del tramo (adaptada de la del largo, con el texto en filas debajo del árbol), `intro_cover("<tema>", color)` en el cuadro 0 y `Scene2_Full` con el último estado de la escena.
3. Probar el 3D con `--width 1080 --height 1920 --stills ...` y luego `python ../../../../../herramientas/build.py`.
4. Revisar el cuadro 0 (la portada no debe tapar el árbol), las hojas de cuadros y que el video dure lo mismo que el audio.

## Para terminar el largo (ya hecho; queda como referencia)

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
