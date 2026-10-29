# LeetSolve: guía para hacer los videos

Videos que explican problemas de LeetCode con Manim, voz Kokoro y una sección 3D en Three.js. Esta guía es el contexto completo: léela antes de crear o modificar un video. Lo que pasó en cada sesión está en `BITACORA.md`.

## Estilo aprobado (desde 2026-10-20)

Los videos nuevos se hacen con el **estilo Minecraft con assets del juego y su mundo de fondo**. Aldo lo aprobó con "Quedó perfecto". La plantilla es `pruebas/0001-two-sum-minecraft-original`.

- Tema `minecraft-original`: texturas, interfaz, fuente y sonidos del juego instalado (ver "Temas visuales").
- Todo el video pasa en el mundo **ClaudeEntorno**, en la pradera del spawn: un solo clip 3D de punta a punta (ver "Fondo con un mundo real").
- Escenas 2D sobre el mundo **desenfocado y oscurecido**. La parte 3D va nítida, en un lote de pasto aplanado con la montaña detrás.
- Efectos de sonido del juego mezclados bajo la voz (ver "Efectos de sonido").
- Música de fondo opcional del juego, solo cuando Aldo la pide (ver "Música de fondo"). Aprobada en el #297 con Subwoofer Lullaby.
- Videos hechos en este estilo: `trees/0297-serialize-tree` (aprobado con "Quedó perfecto"). Es buen ejemplo para árboles: `Tree2D`, `TokenLine`, barreras como nulos y un recorrido 3D que guarda y carga.
- Desde el 2026-10-21 los 9 videos anteriores (#1 a #7, #102 y #124) también están en este estilo. Sus versiones neón quedaron como `video_neon.mp4` (fuera de git) y sus fuentes siguen en el historial, en el commit `35c573f`.
- Cada video pasa en **su propio lugar** del mundo, con su **hora del día** y **mobs** caminando al fondo (ver "Lugares del mundo" y "Vida en el fondo"). Aldo pidió los dos cambios para que no se repita el paisaje y se vea vivo.

### Receta para un video nuevo en este estilo

1. **Una sola vez por PC:** `python herramientas/temas/minecraft-original/extraer.py`, y si `mundos/claude.json` no existe:
   `python herramientas/temas/minecraft-original/mundo.py export "%APPDATA%\.minecraft-youtube\saves\ClaudeEntorno" -11 71 -9 64 herramientas/temas/minecraft-original/mundos/claude.json`
2. Crear `videos/<seccion>/<numero>-<nombre>/` y copiar de la plantilla `video.json`, `scenes.py`, `make_walk.py` y `three/mundo.html`. No copiar `media/`, `timestamps.json`, `voiceover.mp3` ni `.tts-cache/`.
3. Escribir `narration.txt` del problema nuevo y generar la voz (paso 4 del flujo general).
4. Ajustar `video.json`: los grupos de escenas según las líneas nuevas, con `"tema": "minecraft-original"` y `"fondo": {"page": "three/mundo.html", "sharp": ["Scene5_Walk"]}`.
5. Reescribir `make_walk.py`: los datos del ejemplo, la mena de cada valor (`ores`), los eventos anclados a frases con `at(línea, "frase")` y `first`/`last` (las líneas del recorrido). Correrlo para generar `walk.json`.
6. Reescribir `scenes.py` con las mismas 7 escenas y los ayudantes del tema: `block_row`, `Inventory`, `Hotbar`, `toast`, `xp_bar`, `level_text`, `chest_icon`, `pickaxe`, `chat`, `MT`, `big_o_pow`. Agregar `self.sfx(...)` en los momentos clave.
7. En `three/mundo.html`:
   - Elegir un lugar de `mundos/lugares.json` que ningún otro video use, con su `turn`, y anotar el video en ese archivo. Si no queda ninguno, buscar uno nuevo (ver "Lugares del mundo").
   - Poner `clear: [-10, 10, 7, 24]` en `makeTerrain` para quitar árboles y plantas donde se para la cámara.
   - Elegir la hora y los mobs del lugar (ver "Vida en el fondo").
   - Cambiar la parte del recorrido (objetos y eventos) según el algoritmo. La mezcla de cámaras (`W0`, `W1`) y la cámara de paseo (`roamPose`) se quedan igual; `walkPose` se ajusta para que el contenido quepa entre los píxeles 130 y 735.
8. `python ../../../herramientas/build.py`, hojas de cuadros con `sheet.py`, revisar el loop y abrir el visor.
9. **Música de fondo, obligatoria (regla de Aldo, 2026-10-25):** todo video y todo short lleva música del OST de Minecraft que ya tenemos copiada del juego. Se pone `"musica"` en `video.json` (ver "Música de fondo"); si el video ya estaba hecho, basta `build.py mux`.

Detalles aprendidos en el #297:
- Para resaltar pixel art (bloques, objetos, barreras), usar un pulso de escala; `Indicate` con color lo pinta de un solo color. En texto, `Indicate` sí sirve.
- Las varillas o líneas de un árbol van detrás de los bloques: agregarlas a la escena antes que los bloques (`self.add(edges, *blocks)`) y luego animar `Create(edges)`.
- Texto armado por piezas (tokens y comas): cada pieza con una caja invisible de la altura de línea (`glyphs`), para que compartan la línea base.
- Con `max_h=3.3`, un código de 10 líneas cabe debajo del inventario.

### Medidas que funcionaron (pantalla de 9 × 12)

- Encabezado (`hdr`) en `TOP_Y = 5.4` a la izquierda; letrero del target (`target_sign(0.6)`) arriba a la derecha.
- Recorrido: inventario del cofre (`Inventory(9)`, ancho 8.6) en y = -1.15; código en y = -4.3 con `max_h=3.25`; respuesta (`chat("return [...]")`) en y = 4.3.
- En `mundo.html`, el desplazamiento vertical de la vista va de 0.12 en el paseo (más cielo) a 0.34 en el recorrido, para que la fila y el cofre queden arriba del inventario. Con eso, el cofre va en z = 3.6 y la fila en z = 0, con bloques separados 1.2.
- Fondo de las escenas 2D: `gblur` sigma 5 y brillo al 82 %.
- Volumen de efectos: 0.22 a 0.45; el sonido de logro (`challenge`) en 0.32.

## Formato fijo de cada video

- Vertical 1080×1920 (9:16, para Shorts), 30 fps, desde el 2026-10-21. Las escenas de Manim siguen en 1080×1440 (frame 9×12) y van centradas, a 240 px del borde de arriba; el mundo 3D se renderiza más alto y llena las franjas de arriba y abajo con más cielo y más terreno.
  - Se activa con `"formato": "9:16"` en `video.json`. Sin esa clave, el video sale en 3:4 como antes.
  - `makeWorld` mantiene igual la franja central: las páginas 3D no cambian. Si una página convierte coordenadas de Manim a 3D (`unproject`), debe multiplicar la y por `world.ndcY` (como `slotPoint` en #102 y #297).
- Narración en inglés con la voz madura clonada (ver "Voz humana con IA"; antes, `af_heart` de Kokoro). Duración: la que pida la explicación, siempre menos de 3 minutos y sin estirarla para llenarlos (Aldo, 2026-10-23). Los videos anteriores duran de 85 a 120 s.
- **Formato horizontal 16:9 (desde 2026-10-24, para videos largos de YouTube):** `"formato": "16:9"` en `video.json`.
  - Las escenas son de 1920 × 1080, con un cuadro de 16 × 9 unidades (x de -8 a 8, y de -4.5 a 4.5). Cada unidad mide 120 px, como en el vertical. Los encabezados van en `TOP_Y = 3.95`.
  - El mundo 3D se renderiza también a 1920 × 1080.
  - Lo que se diseñó para el vertical se ve chico en 16:9: árboles con bloques de 0.95 a 1.2, texto de 44 a 60 y código de 7.4 a 7.8 de ancho.
  - En las partes 3D, el contenido va en los dos tercios de la izquierda y el texto en una columna a la derecha (x de 2.3 a 7.8).
  - Ejemplo: `trees/tree-basics/largo`.
- **Un video en dos formatos:** dos carpetas hermanas (`largo/` y `corto/`) y un `comun.py` en la carpeta de arriba, que `video.json` agrega con `"comun": ["../comun.py"]`. Las líneas de narración idénticas reutilizan la voz si se copia el `.tts-cache/` del largo al corto.
- **Shorts recortados de un video largo (desde 2026-10-24, regla de Aldo):** Shorts 9:16 que enganchan y mandan al video completo.
  - Se dibujan de nuevo en 9:16 (recortar el 16:9 o ponerlo chico en medio deja el texto ilegible en el celular).
  - **Sin voz nueva:** su voz es el tramo exacto del `voiceover.mp3` del largo. `shorts/make_short.py FIRST LAST` escribe un `timestamps.json` con todas las líneas del largo desplazadas (la línea FIRST empieza en 0) y una línea vacía al final para el letrero; así los índices, `at()` y `walk.json` del largo sirven sin cambios.
  - **Se cortan a la mitad**, justo antes de la revelación.
  - **Entrada:** la portada (título del largo y el tema del short) está desde el cuadro 0 mientras la voz ya narra, y se va a los 2 o 3 s. Nada de segundos sin voz.
  - **Cierre:** todo el cuadro se oscurece (un plano negro pegado a la cámara del 3D, porque la capa de Manim solo cubre la franja central) y cae un letrero de madera de Minecraft, "FULL VIDEO / ON YOUTUBE", con el título del largo debajo. La voz no lo dice. Estos shorts no hacen loop.
  - Ejemplo: `trees/tree-basics/shorts/02-dfs`. Pasos en `trees/tree-basics/PARA_AGY.md`.
- La narración no menciona fechas relativas ("today", "yesterday", "daily challenge"): el video debe servir en cualquier fecha. Ver `INSTRUCCIONES_IA.md`, 3.3.
- Mientras se resuelve el ejercicio, el código se muestra a la par y una barra resalta la línea que se está ejecutando.
- Loop: el último cuadro es igual al primero. La portada (`cover()`) se dibuja igual en `Scene1_Hook` y al final de `Scene7_Outro`.
- Una sección 3D (Three.js) con el recorrido del algoritmo, con la capa de Manim (código, encabezado, lecturas) encima.
- Estilo: Minecraft con assets del juego (ver "Estilo aprobado"). Los primeros 9 videos usan el estilo neón oscuro: fondo `#0B0E1A` y paleta compartida entre Manim y Three.js (cian, magenta, amarillo, verde, rojo, violeta, naranja).

## Estructura de carpetas

```
LeetSolve/
├── GUIA.md            esta guía
├── BITACORA.md        qué se hizo en cada sesión
├── herramientas/      código compartido por todos los videos
│   ├── prelude.py     configuración, paleta, ayudantes, clases Base/Overlay de Manim y self.sfx()
│   ├── build.py       arma el video completo según video.json
│   ├── sheet.py       hojas de cuadros para revisar
│   ├── three/         render.mjs (render 3D headless) y stage.js (se sirve como /vendor/lib/stage.js)
│   └── temas/
│       ├── minecraft/            arte propio (texturas generadas y fuentes OFL)
│       └── minecraft-original/   assets del juego: extraer.py, mundo.py, tema.py, mc.js
│                                 (tex/, gui/, font/, sounds/ y mundos/tex/ son del juego y no se suben;
│                                  mundos/ClaudeEntorno.zip y mundos/claude.json sí)
├── videos/<seccion>/<numero>-<nombre>/   un video por carpeta
└── pruebas/           experimentos que no son videos finales
```

Secciones (por tema de LeetCode): `arrays-hashing`, `linked-list`, `sliding-window`, `binary-search`, `strings`, `math`, `trees`, `two-pointers`, `backtracking`, `bit-manipulation`. Crea una sección nueva cuando el problema no encaje, con nombre en inglés y en kebab-case (`graphs`, `dynamic-programming`, `two-pointers`...). La carpeta del video lleva el número del problema con 4 dígitos: `videos/trees/0102-level-order`.

## Videos hechos

- `arrays-hashing/0001-two-sum`: Two Sum, Easy. La plantilla aprobada pasada a su carpeta. Lago con playa (`lake-beach`), de día.
- `linked-list/0002-add-two-numbers`: Add Two Numbers, Medium. Cadenas de bloques (diamante y lapis) unidas por varillas, la suma en esmeralda y el acarreo como orbe. Río ancho (`wide-river`), al amanecer.
- `sliding-window/0003-longest-substring`: Longest Substring Without Repeating Characters, Medium. Ejemplo "abcbdea"; la ventana es un contorno dorado y el cofre guarda el último índice. Meandro entre colinas (`river-hills`), de día.
- `binary-search/0004-median-two-arrays`: Median of Two Sorted Arrays, Hard. Mediana 11, un corte rojo en cada fila y rayos cruzados para revisar. Colina en terrazas (`terraced-hill`), al atardecer.
- `strings/0005-longest-palindrome`: Longest Palindromic Substring, Medium. Ejemplo "abaracecar", un espejo en cada centro. Bosque de abedules (`birch-forest`), de día.
- `strings/0006-zigzag-conversion`: Zigzag Conversion, Medium. PAYPALISHIRING con 3 filas en repisas. Lomas con arena (`sand-hills`), al atardecer.
- `math/0007-reverse-integer`: Reverse Integer, Medium. 1463 y el desbordamiento de 1534236469 como límite de construcción. Loma del sur (`south-hill`), de noche.
- `trees/0102-level-order`: Binary Tree Level Order Traversal, Medium. La cola es el inventario. Bosque de robles (`oak-forest`), de noche.
- `trees/0124-max-path-sum`: Binary Tree Maximum Path Sum, Hard. Mejor camino 42; cada bloque muestra lo que ofrece hacia arriba. Bosque con piedra (`stone-forest`), al amanecer.
- `trees/0297-serialize-tree`: Serialize and Deserialize Binary Tree, Hard. Primer video del estilo aprobado. Árbol `[5,8,2,null,null,7]` guardado en 9 casillas (`5,8,#,#,2,7,#,#,#`), barreras para los hijos vacíos.
- `math/0060-permutation-sequence`: Permutation Sequence, Hard. Segundo video del estilo aprobado. n = 4, k = 9 ("2314"), salto directo por divisiones sucesivas en el sistema numérico factorial.
- Lote del 2026-10-21 (laptop, hecho con subagentes; estado en `RENDER.md`, sección 6). Los 6 están renderizados, pero ninguno está revisado con hojas de cuadros todavía:
  - `strings/0008-string-to-integer`: String to Integer (atoi), Medium. `"  -042a7"` → -42; espacios en piedra, signo en redstone, dígitos en hierro, la letra en tablones; el resultado en esmeralda. Río con orilla de arena (`river-sand`), de día. Renderizado, 95.2 s.
  - `math/0009-palindrome-number`: Palindrome Number, Easy. 12321: invertir solo la mitad (12 y 123 → 123 // 10 = 12). Lago del oeste (`west-lake`), al atardecer. Renderizado, 91.3 s.
  - `two-pointers/0016-three-sum-closest`: 3Sum Closest, Medium. `[-5, 2, 3, 4, 7]`, target 10 → 9. Estanque de abedules (`birch-pond`), al amanecer. Renderizado, 102.1 s.
  - `backtracking/0017-letter-combinations`: Letter Combinations of a Phone Number, Medium. "23" → 9 palabras que llenan las 9 casillas del cofre. Claro con flores (`flower-forest`), de día. Renderizado, 90.3 s.
  - `two-pointers/0018-four-sum`: 4Sum, Medium. `[1, 0, -1, 0, -2, 2]`, target 0 → 3 grupos, con el salto del 0 repetido. Terrazas altas (`high-terraces`), al atardecer. Renderizado, 104.5 s.
  - `linked-list/0019-remove-nth-node`: Remove Nth Node From End of List, Medium. 1→2→3→4→5, n = 2, con dummy y separación fija entre `fast` y `slow`. Sendero de robles (`oak-path`), de noche. Renderizado, 84.3 s.
- `bit-manipulation/3644-max-k-sort-permutation`: Maximum K to Sort a Permutation, Medium (problema diario del 2026-10-23). Primer video hecho en la Mac y primero con la voz madura clonada. `[0, 3, 2, 5, 4, 1, 6]` → 1: la respuesta es el AND de los bloques fuera de su lugar. Cada bit es una lámpara de redstone (`redstone_lamp`) frente a su bloque, y un panel de 3 lámparas grandes guarda el AND (111 → 011 → 001). Borde del bosque (`forest-edge`), al atardecer. 112.8 s, 21 líneas, 61 efectos.
- `arrays-hashing/3942-min-ops-sort-permutation`: Minimum Operations to Sort a Permutation, Medium (diario del 2026-10-22). `[1, 2, 3, 4, 5, 0]` → 3: girar e invertir nunca rompen el círculo, así que solo hay 4 planes; rotar 5 veces pierde contra invertir, rotar e invertir. Dos palancas dibujadas con el modelo del juego (`model_icon("lever")`; al jalarlas se cambia al modelo `lever_on`), el círculo con anillo dorado y letreros que cuentan cada plan. Colinas del oeste (`west-hills`), al amanecer. 116.5 s, 20 líneas, 52 efectos.
- `math/2409-count-days-together`: Count Days Spent Together, Easy (diario del 2026-10-24). Alice 10-28 → 11-03 y Bob 10-30 → 11-05 → 5: cada fecha se vuelve día del año (suma de los meses anteriores más el día) y los días juntos son `min(salidas) - max(llegadas) + 1`, sin bajar de 0. Fila de 10 días (octubre en redstone, noviembre en lapis), marcos dorados para Alice y aqua para Bob; la fuerza bruta es un calendario de 365 cuadros. Pradera de pasto alto (`tall-meadow`), de día. 101.2 s, 20 líneas, 39 efectos.
- `arrays-hashing/3886-sum-of-sortable-integers`: Sum of Sortable Integers, Hard (diario del 2026-10-20). `[1, 2, 3, 3, 4, 3]` → 5 (sirven k = 2 y k = 3; con valores distintos y n = 6 nunca sirven dos k, por eso hay repetidos). Una pieza gira en orden si, recorrida en círculo, tiene a lo más una caída; luego cada pieza debe empezar donde terminó la anterior o más arriba. La fila se corta en piezas con huecos, las caídas son "v" rojas y las de vuelta un arco punteado, y un letrero lleva la suma. Pradera ondulada (`east-meadow`), de noche. 129.8 s, 20 líneas, 39 efectos.
- `trees/tree-basics/largo`: How Trees Really Work, guía de árboles en 16:9 para YouTube (6:23, 63 líneas, 11 escenas). Anatomía, subárboles con tijeras, DFS con rienda (preorden, inorden y postorden), BFS con cola, árbol de búsqueda con tolva, la clase `Node`, recursión y "cambia solo la última línea". Lugar `birch-grove` (MacEntorno), de día. Terminado el 2026-10-24 en la PC de Windows; exportado como `How Trees Really Work.mp4`.
- `trees/tree-basics/shorts/02-dfs`: primer short recortado del largo (líneas 20 a 25, 48.3 s), muestra para aprobar.
- `pruebas/0001-two-sum-horizontal`: primera prueba en 16:9, sin código a la par.
- `pruebas/0001-two-sum-minecraft`: Two Sum con el tema de Minecraft. Se arma con `python ../../herramientas/build.py` (está a dos niveles, no a tres).
- `pruebas/0001-two-sum-minecraft-original`: **plantilla del estilo aprobado**. Two Sum con los assets y sonidos del juego, en el mundo ClaudeEntorno.
- `pruebas/voces_demo/`: muestras de referencia femeninas diseñadas desde cero con `Qwen3-TTS-12Hz-1.7B-VoiceDesign` (`01_joven_youtuber.mp3`, `02_calida_storyteller.mp3`, `03_clara_directa.mp3`, `04_madura_sensual.mp3`) y los scripts de diseño, clonación y limpieza de silencios.
- `pruebas/0004-joven-youtuber` y `pruebas/0004-madura-sensual`: pruebas completas del ejercicio #4 (Median of Two Sorted Arrays) con voz clonada en la GPU local (`Qwen3-TTS-12Hz-0.6B-Base`), de 93.12 s y 103.73 s respectivamente.
- `videos/tech/dns`: **How DNS Works** (155.6 s), el primer short de tecnología, todo en 3D: bibliotecarios de una aldea como servidores DNS, caché con TTL, Pi-hole, suplantación y DNSSEC, DNS cifrado y unbound, CDN.

Al terminar un video nuevo, agrégalo a esta lista.

Los videos terminados se copian a `export/` en la raíz con el nombre `<Título> #<número>.mp4` (por ejemplo `4Sum #18.mp4`), listos para subir. Esa carpeta no se sube a git.

**Nombre del video (regla de Aldo, 2026-10-23):** un video terminado nunca se queda como `video.mp4`. Al terminar, en su carpeta se renombra a `<Título> #<número>.mp4` (por ejemplo `videos/bit-manipulation/3644-max-k-sort-permutation/Maximum K to Sort a Permutation #3644.mp4`) y esa misma copia va a `export/`. `build.py` vuelve a escribir `video.mp4` en cada `mux`: después de un rebuild, renombrar otra vez. El `.gitignore` ignora `*#*.mp4`.

**Descripción para subir (regla de Aldo, 2026-10-23):** cada video lleva `descripcion.txt` en su carpeta (sí se sube a git) con la descripción para YouTube Shorts e Instagram Reels: una línea en inglés de **100 caracteres o menos** (Shorts no permite más), con el número y el nombre del problema. Formato: `LeetCode #<número> <Título>, explained in Minecraft #leetcode #coding #shorts` (quitar `#coding` si no cabe). Medir el largo con `len()` antes de guardarla. El aviso "Not an official Minecraft product" no cabe ahí: va en un comentario fijado o en la descripción larga si la plataforma la tiene.

## Entorno (Windows)

- Manim CE 0.22 y Kokoro viven en el venv `~/.manim-skill-src/.venv` (Python 3.12). Python global 3.14 no sirve.
- Antes de cualquier comando (Bash):
  ```bash
  export PATH="$HOME/.manim-skill-src/.venv/Scripts:$PATH" PYTHONUTF8=1
  ```
- Usar `python`, nunca `python3`. `PYTHONUTF8=1` es obligatorio (las herramientas imprimen "→").
- Herramientas de la skill: `~/.manim-skill-src/skills/manim-skill/tools/` (`tts-generate.py`, `lint-subtitles.py`, `video_viewer.py`).
- Render 3D: `herramientas/three/render.mjs` (Node + Playwright Chromium, usa la RX 6600 por D3D11). En una PC nueva, correr `npm ci` y `npx playwright install chromium` dentro de `herramientas/three`. Sirve su propia carpeta como `/vendor/lib/` (ahí está `stage.js`).
- En otra PC, si la skill no está en `~/.manim-skill-src`, definir `MANIM_SKILL_TOOLS` con la carpeta `tools/` de github.com/Yusuke710/manim-skill.
- LaTeX: MiKTeX. ffmpeg y ffprobe en el PATH.

## Entorno (Mac con Apple Silicon)

Montado el 2026-10-23 en una MacBook Air M2 de 8 GB. Todo vive en el usuario, sin `sudo` salvo para reparar Homebrew.

- **Homebrew:** si dice "unknown or unsupported macOS version" o que `/opt/homebrew` no se puede escribir, correr `sudo chown -R $(whoami) /opt/homebrew` y `brew update`. Luego `brew install ffmpeg cairo pango pkg-config`.
- **Python:** `uv` (instalador de astral.sh en `~/.local/bin`) crea los dos venvs con Python 3.12:
  ```bash
  uv venv ~/.manim-skill-src/.venv --python 3.12
  uv pip install --python ~/.manim-skill-src/.venv/bin/python "manim==0.22.*" "kokoro>=0.9.4" soundfile pygments pillow
  uv venv ~/.manim-skill-src/.venv-tts --python 3.12
  uv pip install --python ~/.manim-skill-src/.venv-tts/bin/python torch torchaudio qwen-tts soundfile
  ```
  En Mac los venvs usan `bin/`, no `Scripts/`. El torch normal de PyPI ya trae MPS (la GPU de Apple).
- **Herramientas de la skill:** el repo `github.com/Yusuke710/manim-skill` va dentro de `~/.manim-skill-src` (junto a los dos venvs).
- **LaTeX:** TinyTeX en `~/Library/TinyTeX` (instalador de yihui.org, sin `sudo`; el error de `sudo` al final solo es por los enlaces de `/usr/local/bin` y no importa). Paquetes de Manim: `tlmgr install standalone preview doublestroke ms everysel setspace rsfs relsize ragged2e fundus-calligra microtype wasysym physics dvisvgm jknapltx wasy cm-super babel-english gnu-freefont mathastext cbfonts-fd`.
- **3D:** `npm ci` y `npx playwright install chromium` en `herramientas/three`. En Mac, `render.mjs` usa ANGLE con Metal (en Windows, D3D11); el render reporta `ANGLE Metal Renderer: Apple M2`.
- **Minecraft:** launcher oficial (`launcher.mojang.com/download/Minecraft.dmg`, firmado por Microsoft) en `/Applications`. Los archivos del juego quedan en `~/Library/Application Support/minecraft`, y `extraer.py` ya busca ahí. Si también hay una snapshot sin `.jar`, `extraer.py` toma la versión con `.jar` más nueva.
- **Antes de cada comando:**
  ```bash
  export PATH="$HOME/.manim-skill-src/.venv/bin:$HOME/Library/TinyTeX/bin/universal-darwin:$HOME/.local/bin:$PATH" PYTHONUTF8=1
  ```
- **Voz con Qwen3-TTS en MPS:** `0.6B-Base` en `bfloat16` carga en unos 58 s y genera 7 s de audio en unos 19.5 s, unos 5 minutos por video de 20 líneas. El aviso "SoX could not be found" no afecta, porque se le pasa un `.wav`.
- `planks_sign.png` da 404 al renderizar el 3D: es opcional en `mc.js`, que usa `planks.png` si falta.

## Voz humana con IA (Qwen3-TTS: Diseño y Clonación en GPU)

**Voz elegida (2026-10-23): `04_madura_sensual.mp3`.** Los videos nuevos se narran con ella clonada (Fase 2); Kokoro `af_heart` queda como respaldo.

Además de Kokoro-82M (`af_heart`, que corre en CPU y lee plano línea por línea sin entender el contexto), el proyecto cuenta con un flujo de **diseño y clonación de voz basado en LLM (`Qwen3-TTS`)** acelerado por GPU CUDA:

### 1. Entorno dedicado (`~/.manim-skill-src/.venv-tts`)

- Para no alterar las dependencias del entorno de Manim (`~/.manim-skill-src/.venv`, que usa `torch` CPU), las herramientas de voz con IA viven en un entorno virtual separado creado con `uv` en `~/.manim-skill-src/.venv-tts` (Python 3.12).
- **Paquetes instalados en `.venv-tts`:**
  - `torch==2.14.1+cu126` y `torchaudio==2.11.0+cu126` (compilados con CUDA 12.6, aprovechando los 6 GB VRAM de la RTX 3060 Laptop GPU en precisión `bfloat16`).
  - `qwen-tts==0.1.1` (interfaz oficial `Qwen3TTSModel` con tokenizador de audio discrete multi-codebook a 12 Hz).
  - `transformers`, `accelerate`, `soundfile`, `librosa`, `scipy`, `onnxruntime` y `gradio_client`.
- **Instalación desde cero en otra PC con GPU NVIDIA:**
  ```bash
  uv venv "$HOME/.manim-skill-src/.venv-tts" --python 3.12
  uv pip install --python "$HOME/.manim-skill-src/.venv-tts/Scripts/python.exe" torch torchaudio --index-url https://download.pytorch.org/whl/cu126
  uv pip install --python "$HOME/.manim-skill-src/.venv-tts/Scripts/python.exe" -U qwen-tts soundfile
  ```

### 2. Fase 1 — Diseñar una voz desde cero (`Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign`)

- Cuando se quiere inventar una identidad vocal nueva sin partir de grabaciones reales, se usa el modelo `Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign` mediante `model.generate_voice_design(text, language="English", instruct=...)`.
- El parámetro `instruct` recibe una descripción en lenguaje natural (edad, género, timbre, ritmo, acento y actitud).
- **Por qué no se usa `VoiceDesign` directo en las 20 líneas del video:** `VoiceDesign` inventa una voz a partir del texto descriptivo en cada llamada; si se llamara 20 veces por separado, el timbre podría variar ligeramente de una línea a otra. Por eso `VoiceDesign` se usa **una sola vez** para generar las muestras candidatas de ~10–15 s en `pruebas/voces_demo/`:
  - `01_joven_youtuber.mp3` (11.8 s): voz femenina joven, energética, estilo creadora de YouTube/gamer.
  - `02_calida_storyteller.mp3` (15.3 s): voz femenina cálida y suave, estilo narradora.
  - `03_clara_directa.mp3` (10.6 s): voz femenina rápida, articulada y directa.
  - `04_madura_sensual.mp3` (17.6 s): voz femenina madura (contralto), profunda, aterciopelada y sensual.
- **Texto y descripciones usadas** (semilla 42, todas leyendo el mismo texto, que también es el `ref_text` de la clonación): *"Two Sum, Minecraft edition. LeetCode problem number one, and an interview classic. Here's the trick. If the target is twenty three and I'm holding a fifteen, I know exactly what I need. An eight."*
  - `01_joven_youtuber`: "A young, energetic female voice in her early twenties, natural American accent, bright and engaging YouTube creator tone, lively pacing with clear emphasis."
  - `02_calida_storyteller`: "A warm, soothing female voice, gentle and natural conversational tone, clear articulation, calm and inviting storyteller style."
  - `03_clara_directa`: "A crisp, confident young woman's voice, brisk and sharp tech explainer delivery, natural human inflection, articulate and modern."
  - `04_madura_sensual`: "A mature woman in her late thirties with a deep, rich, velvety and sensual voice, alluring and intimate tone, soft breathy warmth, slow confident delivery."
  - No está anotado si los `.mp3` del repo salieron de `gen_demos.py` (que guarda `.wav`) o de `gen_demos_fast.py`. Para clonar no importa: la referencia es el `.mp3`.
- **Scripts de esta fase:**
  - `pruebas/voces_demo/gen_demos.py`: corre `Qwen3-TTS-12Hz-1.7B-VoiceDesign` localmente en la GPU (`cuda:0`, `bfloat16`).
  - `pruebas/voces_demo/gen_demos_fast.py`: alternativa ligera que consulta el endpoint SSE `/gradio_api/call/generate_voice_design` de los espacios de `Qwen3-TTS` en Hugging Face sin descargar los 3.4 GB del modelo de diseño.

### 3. Fase 2 — Clonar la voz elegida en todo el video (`Qwen/Qwen3-TTS-12Hz-0.6B-Base`)

- Una vez elegido el `.mp3` de referencia, `pruebas/voces_demo/tts_qwen_clone.py` usa el modelo base **`Qwen/Qwen3-TTS-12Hz-0.6B-Base`** (~1.2 GB en disco, ~1.5 GB de VRAM en `bfloat16`) para sintetizar todas las líneas de `narration.txt` manteniendo exactamente el mismo timbre de principio a fin:
  1. **Preprocesamiento del audio de referencia con `ffmpeg`:** convierte el `.mp3` maestro a un `.wav` temporal mono a 24 kHz (evitando que `qwen-tts`/`librosa` dependan del binario externo `sox`) y le aplica `silenceremove` para recortar cualquier pausa interna mayor a `0.20 s`. Si el audio de referencia tiene pausas largas (~1 s), el LLM aprende a insertar silencios muertos a mitad de las oraciones.
  2. **Extracción única del prompt vocal:** llama una sola vez a `prompt = model.create_voice_clone_prompt(ref_audio=ref_wav, ref_text=ref_text)`, que extrae tanto los tokens acústicos/semánticos de la referencia como el vector de hablante (`x-vector`).
  3. **Síntesis línea por línea con control de alucinaciones:** recorre cada viñeta de `narration.txt` con `model.generate_voice_clone(text=text, language="English", voice_clone_prompt=prompt)`. Calcula las palabras de la línea y verifica que la duración cruda cumpla `raw_dur <= words * 0.65 + 1.5`; si el LLM alucina un silencio largo al final, reintenta automáticamente cambiando la semilla (`torch.manual_seed`).
  4. **Limpieza acústica de cada línea (`write_mp3_clean`):** antes de guardar cada clip en `.tts-cache/`, lo pasa por `ffmpeg` con:
     ```
     silenceremove=start_periods=1:start_duration=0.02:start_threshold=-40dB:stop_periods=-1:stop_duration=0.22:stop_threshold=-40dB,apad=pad_dur=0.08
     ```
     Esto elimina silencios al inicio de la línea, recorta cualquier pausa interna o final a un máximo de `0.22 s` y deja una cola limpia de `0.08 s` antes de codificar con `libmp3lame -q:a 2`.
  5. **Empaquetado compatible con `build.py`:** mide cada clip con `ffprobe`, los une en `voiceover.mp3` usando el mismo filtro `apad,atrim` que `tts-generate.py` (para no acumular padding de paquetes MP3) y escribe `timestamps.json` con `start_s`, `end_s` y `duration_s` exactos. Después basta correr `python make_walk.py` y `python ../../herramientas/build.py`.
- Si un `.tts-cache/` ya fue generado sin el filtro de silencios, `pruebas/voces_demo/fix_madura_silences.py` limpia todos los clips en caché, reconstruye `voiceover.mp3` y actualiza `timestamps.json` en un par de segundos sin volver a correr la red neuronal.

## Archivos de cada video

- `narration.txt`: solo las líneas habladas, una por viñeta, bajo `subtitles:`.
- `timestamps.json` y `voiceover.mp3`: salida del TTS. Cada `duration_s` es el tiempo exacto de esa línea.
- `scenes.py`: las escenas de Manim. **No se edita `script.py`**: `build.py` lo genera pegando `prelude.py` + `scenes.py`.
- `walk.json`: tiempos de los eventos del recorrido, compartidos por Manim y Three.js. Si los datos se calculan, se genera con `make_walk.py`.
- `three/walk.html`: la escena 3D. Define `window.renderAt(t)` y `window.sceneDuration`.
- `video.json`: qué líneas de narración van en cada escena y cuál escena es la 3D.
- `video.mp4`: el resultado final.

## Flujo para un video nuevo

1. **Elegir el ejemplo.** Pequeño y con un caso que muestre la idea clave (un descarte, un desbordamiento, una actualización del mejor). Verifica la respuesta en Python antes de escribir la narración.
2. **Crear la carpeta** `videos/<seccion>/<numero>-<nombre>/` y trabajar siempre dentro de ella.
3. **Narración** en `narration.txt`, en inglés, unas 17 líneas, a unas 2.5 palabras por segundo. Escribe el archivo con la herramienta Write, no con heredoc de Bash (los apóstrofos rompen el heredoc).
4. **TTS:**
   ```bash
   python "$HOME/.manim-skill-src/skills/manim-skill/tools/tts-generate.py" --narration narration.txt
   ```
   Confirma que el número de clips coincide con el de líneas. Para regenerar una sola línea: `--bust <índice o fragmento>`.
5. **`video.json`** con los grupos de escenas y sus índices de línea:
   ```json
   {"groups": [["Scene1_Hook", [0]], ["Scene2_Problem", [1, 2]], ["Scene3_Brute", [3]], ["Scene4_Idea", [4, 5, 6]],
               ["Scene5_Walk", [7, 8, 9, 10, 11, 12]], ["Scene6_Complexity", [13, 14]], ["Scene7_Outro", [15, 16]]],
    "three": {"scene": "Scene5_Walk", "page": "three/walk.html"}}
   ```
6. **`walk.json`**: `first` y `last` (índices de las líneas del recorrido) y cada evento como `[línea, segundos dentro de la línea]`.
7. **`scenes.py`** con las 7 escenas (ver la estructura abajo).
8. **`three/walk.html`** importando de `/vendor/lib/stage.js`.
9. **Armar:**
   ```bash
   python ../../../herramientas/build.py
   ```
   Sin argumentos corre todo: `script lint render three composite sync mux`. Se pueden correr pasos sueltos, por ejemplo `python ../../../herramientas/build.py script lint render Scene4_Idea sync Scene4_Idea mux`.
10. **Revisar** (ver la lista de revisión) y abrir el visor:
    ```bash
    python "$HOME/.manim-skill-src/skills/manim-skill/tools/video_viewer.py" video.mp4 --order concat.txt --script script.py --port 80NN
    ```

## Estructura de escenas

- `Scene1_Hook`: portada con `gradient_title`, el dibujo de `cover()` y `tags_block` (número, dificultad, tema). Al final, `FadeOut`.
- `Scene2_Problem`: enunciado con un ejemplo pequeño.
- `Scene3_*`: la solución ingenua o la idea obvia y por qué falla (Brute, Merge, String, DFS, Grid...).
- `Scene4_*`: la idea clave de la solución buena.
- `Scene5_Walk`: recorrido en 3D. Es una clase `Overlay` que se renderiza transparente (`-t`) y se encima sobre el clip 3D. Lleva el encabezado, el código con `line_bar` y lecturas en `pill`. Usa `run_events(walk, events, handler, on_first, on_last)`.
- `Scene6_Complexity`: tiempo y espacio con `big_o`.
- `Scene7_Outro`: el código completo, un repaso de sus líneas clave, y termina dibujando `cover()` igual que el primer cuadro.

## Reglas de tiempos

- Cada escena llama `self.seg(i)` al empezar cada línea de narración. Eso agrega el subtítulo con su duración exacta.
- Animar solo con `self.beat(*anims, rt=...)`, esperar con `self.hold(t)` o `self.until(u)` (u = segundos dentro de la línea actual).
- Cerrar cada línea con `self.close_seg()`. Para que algo termine justo al cerrar la línea: `self.finish(anim, rt=...)`. Para limpiar la pantalla: `self.clear_all()`.
- No dejar `until(DUR-0.5)` antes de `clear_all()`: se pasa del presupuesto.
- Todo está cuantizado a cuadros completos para que el audio no se desfase. `build.py` usa los mismos límites de cuadro en render, composición y sincronización.
- En Three.js el tiempo lo da `loadTiming(walk.first, walk.last)`: `seg(i)` es el inicio de la línea i en segundos desde el inicio del recorrido.

## Ayudantes de `prelude.py`

- Texto: `T(s, size, color)` (Segoe UI) y `M(s, size, color)` (Consolas, monoespaciado).
- Formas: `Tile`, `tile_row(values, color, y, size, gap, x)`, `index_labels`, `pill`, `header`, `corner_pill`, `tags_block`, `gradient_title`, `glow`, `ring`.
- Código: `code_panel(src, y, width=8.4, max_h=None)` y `line_bar(code, k0, k1, color)`.
- Complejidad: `big_o(tex, color, y, label)`.
- Para cambiar el color de un `Tile` usa `restyle(tile, lambda t: t.box.set_stroke(...))`. Animar solo `tile.box` hace que Manim dibuje la caja encima del texto, y `set_color` la vuelve un cuadro sólido.

## Ayudantes de `stage.js`

- `makeStage({fov, offset, bloom, gridY, gridX, fog})` devuelve `{scene, camera, look, draw(t, total)}`. `offset` desplaza la imagen hacia arriba para dejar abajo el espacio del código.
- Objetos: `makeTile`, `makeOrb`, `makeArrow`, `makeRod` (con `grow`), `makeOrbLight`, `textSprite` (con `setSize`), `textPlane`.
- Animación: `prog(t, a, b)`, `easeInOut`, `easeOutBack`, `keyed`, `bezier`, `mixColor`, `lerp`, `V`.
- Cámara: `pose`, `mixPose`, `poseTrack`, `drift`.
- El render es determinista: todo depende de `t`, nada de relojes ni de `Math.random` sin semilla.

## Temas visuales

Un tema cambia el estilo sin tocar el flujo. Vive en `herramientas/temas/<tema>/` y se activa con `"tema": "<tema>"` en `video.json`.

- `build.py` pega `tema.py` después de `prelude.py` (con `TEMA_DIR` definido) y le pasa `--tema` al render 3D, que sirve esa carpeta como `/vendor/tema/`.
- Tema `minecraft` (prueba en `pruebas/0001-two-sum-minecraft`):
  - Texturas pixeladas originales generadas por `textures.py` en `tex/`. Para agregar una, se añade al final del diccionario de `main()` y así no cambian las semillas de las demás.
  - Fuentes OFL en `fonts/`: Press Start 2P para títulos y números, VT323 para texto y código.
  - `tema.py`: cielo de fondo, `MT` (texto con sombra dura), `Block`, `block_row`, `Inventory` (cofre con casillas), `Hotbar`, `sign`, `toast` ("Advancement Made!"), `pickaxe`, `stone_title`, `splash` y un `code_panel` con colores del chat del juego.
  - `mc.js`: mundo de día con pasto, árboles y nubes, bloques con el número en la cara, cofre con tapa, marco de selección, letreros y orbes de experiencia.
  - Manim no puede usar `ImageMobject` con la versión de Pillow del venv, así que el pixel art se dibuja como rectángulos vectoriales (`pixel_art`).
  - Todo el arte de este tema es propio.
- Tema `minecraft-original` (prueba en `pruebas/0001-two-sum-minecraft-original`): usa los assets del juego instalado en la PC.
  - Antes de usarlo: `python herramientas/temas/minecraft-original/extraer.py` copia de `%APPDATA%\.minecraft` (la versión más nueva) las texturas, la interfaz (cofre, barra de objetos, barra de experiencia, aviso de logro), la fuente `ascii.png` y los sonidos.
  - Esos archivos no se pueden redistribuir: `tex/`, `gui/`, `font/` y `sounds/` están en `.gitignore` y nunca se suben a un repositorio. Al publicar un video, poner "Not an official Minecraft product" en la descripción y no usar el logo del juego.
  - Su `tema.py` empieza con `# extends: minecraft`: `build.py` pega primero el tema base y después este, que reemplaza el texto (fuente del juego dibujada como pixel art), los bloques, `Inventory` (pantalla del cofre con 9 casillas), `Hotbar`, `toast`, `xp_bar`, `level_text`, `iso_block` (bloque en vista de inventario), `chest_icon` y el panel de código.
  - **Íconos de bloques que no son cubos (palanca, antorcha, etc.): usar el modelo del juego, no inventarlos.** `extraer.py` copia cada modelo de `MODELS` (por ahora `lever` y `lever_on`) con sus texturas a `models/<nombre>/` (no se sube). `model_icon(nombre, w, rot_y=45)` en `tema.py` lo dibuja como en el inventario: cada caja del json con su rotación, cada cara recortada de su textura por su `uv`, la sombra por cara del juego y solo las caras que miran a la cámara. Con `center=False` dos estados del mismo bloque comparten coordenadas (la base de la palanca no se mueve al jalarla). La textura suelta `block/lever.png` es solo el palo de 2 × 10: usarla sola se ve como un palito, y armar una palanca a mano con otras proporciones no es la del juego (Aldo lo notó en el #3942).
  - `mc.js` arma el cofre con el modelo y la textura del juego, el contorno negro del bloque apuntado, orbes de experiencia con su color cambiante y nubes sacadas de `clouds.png`.

## Fondo con un mundo real

- En `video.json`, `"fondo": {"page": "three/mundo.html", "sharp": ["Scene5_Walk"]}` en lugar de `"three"`: se renderiza un solo clip 3D de todo el video y cada escena va encima de su tramo. Las escenas que no están en `sharp` llevan el mundo desenfocado y un poco oscurecido.
- Con `fondo`, todas las escenas se renderizan transparentes y el tema no dibuja su cielo (`FONDO = True` en `script.py`).
- El terreno sale de un mundo de Java Edition con `herramientas/temas/minecraft-original/mundo.py`:
  - `python mundo.py info <carpeta del mundo>` muestra la posición del jugador y el spawn.
  - `python mundo.py export <carpeta del mundo> X Y Z RADIO mundos/<nombre>.json` guarda los bloques visibles alrededor de ese punto (sin cuevas) y copia sus texturas a `mundos/tex/`.
  - En la página: `makeTerrain('/vendor/tema/mundos/<nombre>.json', { turn, plot })`. `turn` gira el terreno y `plot` aplana un lote de pasto donde va la fila de bloques.
- El mundo de prueba es "ClaudeEntorno" (perfil "YouTube DSA" del launcher, en `%APPDATA%\.minecraft-youtube\saves`), exportado alrededor del spawn con radio 64.
- El repositorio trae una copia del mundo en `mundos/ClaudeEntorno.zip` (sin la carpeta `players/`) y su exportación `mundos/claude.json`. Para verlo en el juego, descomprimir el zip en la carpeta `saves` de Minecraft Java 26.2 o más nuevo. Las texturas de `mundos/tex/` no se suben: las vuelve a copiar `mundo.py export` desde el juego instalado.
- La cámara del clip completo hace un recorrido periódico (`sin` y `cos` de `2π t / TOTAL`) para que el último cuadro sea igual al primero. Entra y sale de la cámara del recorrido del algoritmo en 1.5 s.

## Videos solo 3D (sin Manim)

Desde 2026-10-28, para la línea de shorts que explican tecnologías (`videos/tech/`). A Aldo le gustan más las partes 3D que las escenas 2D, así que aquí todo pasa dentro del mundo. Ejemplo: `videos/tech/dns/` (diseño en `DISENO.md`).

- **`video.json`:** `{"solo3d": {"page": "three/dns.html"}, "formato": "9:16", "tema": "minecraft-original", "musica": {...}}`. Sin `groups`. `build.py` sin argumentos corre `three mux`: renderiza la página por la duración de `voiceover.mp3` y mezcla voz, efectos y música.
- **Voz:** `narration.txt` y `pruebas/voces_demo/tts_qwen_clone.py <carpeta>` (voz madura clonada), que escribe `voiceover.mp3` y `timestamps.json` sin Manim. En la PC de Windows corre en CPU (venv `~/.manim-skill-src/.venv-tts` con torch de CPU): unos 4 minutos por línea, porque reintenta las líneas con silencios largos. Escribir números y siglas como se dicen ("one-forty-two", "D N S", "google dot com"). Revisión: `silencedetect` (ningún silencio > 0.45 s) y `pruebas/voces_demo/check_voice.py <carpeta>` con el Python de `.venv-tts`, que transcribe cada línea con Whisper y la compara con el guion (las diferencias por escribir números o siglas no cuentan; si falta una palabra corta al inicio ("The", "A"), volver a transcribir con 0.3 s de margen: Whisper sin contexto pierde las palabras átonas del inicio, aunque estén en el audio. Medir los primeros 120 ms de la línea: si empieza con silencio y sube suave, no hay recorte). Para regenerar una línea, borrar su `.mp3` de `.tts-cache/` y volver a correr el script.
- **Tiempos:** la página lee `/timestamps.json` y ancla todo a `ev(línea, fracción)` (fracción de la duración de esa línea), nunca a segundos absolutos: si la voz cambia, todo se mueve con ella. Mientras no hay voz, se puede poner un `three/timestamps.json` provisional (la carpeta de la página tiene prioridad); **hay que borrarlo** antes del render final.
- **Efectos de sonido:** la página define `window.sfxCues = [[segundos, sonido, volumen], ...]`; `render.mjs --cues` los guarda en `media/sfx/solo3d.json` y `mux` los mezcla.
- **Cámara:** lista de llaves `[tiempo, pose o función de t, segundos de mezcla]`; una función sirve para seguir a un objeto que vuela (el libro de la pregunta).
- **Personajes (`gente.js` del tema):** `makeVillager(imgs, {profession, type})` (o `{skin: 'wandering_trader'}`), `makePlayer(imgs, {skin: 'steve' | 'alex'})`, `makeIllager(imgs, {kind: 'illusioner'})`. Cada uno da `{g, head, walk(fase, cantidad), look(giro, inclinación)}`. Texturas en `gente/` (las copia `extraer.py`). El ala del sombrero solo se dibuja si la textura la tiene.
- **Aldea (`aldea.js` del tema):** `makeLibrary`, `makeTower`, `makeSite`, `makeBarrierRoom`, `makeBank`, `makeHome` (construcciones por código con las texturas del juego; todas miran hacia +z), `makeLectern` (con `setBook(líneas)` y `open(k)`), `bubble(líneas)` (tooltip del juego), `makeItem(imgs, nombre)` (con `glow` de encantamiento) y `arc(a, b, k, altura)`.
- **Globos legibles:** `bubble` y `uiSprite` registran el sprite y `placeUI(camera)` (después de mover la cámara, cada cuadro) les da el mismo tamaño en pantalla y los mete dentro del cuadro. Sin eso, en las tomas cercanas salen enormes y cortados.
- **Tomas aéreas:** en 9:16 el ancho es poco; para ver toda la aldea (70 × 70 bloques) la cámara va a unos 80 de altura, y los nombres de los edificios se ponen como globos flotantes porque los letreros no se leen.
- Errores de la primera versión, ya corregidos: el sendero como bloques quedaba enterrado bajo el pasto (va como plano encima), la casa tapaba la cámara (revisar qué hay entre la cámara y el objetivo), el destello de la explosión salía cuadrado (textura radial) y lo que se orienta hacia la cámara debe hacerlo después de moverla.

## Lugares del mundo

- 2026-10-23: `forest-edge` (−2, 69, 98, giro 1.9635), del mundo del zip. Se buscó con un escáner de heightmaps (`OCEAN_FLOOR`, `MOTION_BLOCKING`, `MOTION_BLOCKING_NO_LEAVES`, `WORLD_SURFACE`) con las reglas de abajo, a más de 45 bloques de los lugares usados, y se eligió entre 4 candidatos viendo la cámara de paseo y la del recorrido. Los otros 3 eran pradera plana con paredes de tierra en la cámara del recorrido.
- **Dos mundos.** `ClaudeEntorno` (el del zip, 26.2) ya no tiene lugares buenos libres: los 20 que había se usaron. `MacEntorno` (26.3, otra semilla, unos 512 × 512 bloques generados, en `~/Library/Application Support/minecraft/saves/MacEntorno` de la Mac) es el mundo para los lugares nuevos; en `lugares.json` sus lugares llevan `"mundo": "MacEntorno"` (los que no lo llevan son de ClaudeEntorno o del ClaudeEntorno de la laptop). Para más terreno: abrir el mundo en el juego, `/gamemode creative`, volar en línea recta en cada dirección con la distancia de renderizado alta y **guardar y salir** antes de exportar.
- Candidatos ya exportados de MacEntorno, sin video todavía (`mundos/mac-XX.json`): `mac-01` (−206, 63, −34, giro 4.7124, arena con abedules), `mac-02` (−38, 67, 62, 2.3562, arena con abedules), `mac-03` (−50, 69, 26, 5.1051, dunas frente al mar), `mac-05` (−114, 68, −50, 3.5343, playa), `mac-07` (−174, 66, −34, 1.9635, playa), `mac-09` (−86, 64, −30, 0.3927, loma de abedules con arroyo), `mac-10` (−138, 62, −94, 0.7854, bosque de abedules con flores), `mac-11` (−54, 62, 90, 3.927, mar abierto), `mac-12` (−174, 69, −222, 2.3562, abedules sobre terrazas de arena), `mac-13` (−194, 64, −134, 0.7854, abedules sobre terrazas de tierra). Todos con `plot: [-12, 12, -2, 20]`. Al usar uno, renombrar el archivo con un nombre descriptivo y anotarlo en `lugares.json`.
- Revisar el bioma antes de usar un lugar: `mundo.py` pinta pasto y hojas con el tinte de llanura; en bosque oscuro, pantano, jungla o taiga se ven mal.
- El escáner de lugares (heightmaps `OCEAN_FLOOR`, `MOTION_BLOCKING`, `MOTION_BLOCKING_NO_LEAVES`, `WORLD_SURFACE`) califica cada centro y giro: lote plano y seco, cámara libre, agua/hojas/colinas enfrente y ninguna pared a menos de 10 bloques detrás de la fila. Se vieron los candidatos con una página de vista (cámara de paseo y del recorrido) antes de elegir.
- Cada video usa un lugar distinto de ClaudeEntorno. La lista con el centro, el giro (`turn`) y el video que lo usa está en `mundos/lugares.json`; cada lugar tiene su exportación en `mundos/<lugar>.json`.
- Para buscar lugares nuevos se hizo un mapa de todo el mundo generado (unos 370 × 350 bloques) y se calificó cada centro y dirección: la zona de la cámara sin árboles ni terreno más alto que 2 bloques, el lote plano y algo interesante enfrente (agua, bosque, piedra, colinas). Luego se probaron con cuadros sueltos de la cámara de paseo.
- `makeTerrain(url, { turn, plot, clear })`:
  - `clear = [x0, x1, z0, z1]` quita árboles y plantas en esa zona de la escena (donde se para la cámara; no se ve).
  - Si el terreno baja frente al lote, se ve una pared de tierra entre la cámara y el recorrido. En el #7 se resolvió alargando `plot` hasta la cámara (`[-12, 12, -2, 20]`).
  - `terrain.surfaceAt(x, z)` dice qué bloque hay arriba de la columna (`water`, `leaves`, `log` o el nombre) y a qué altura. Lo usa `vida.js`.
- 2026-10-21: 6 lugares más (`river-sand`, `west-lake`, `birch-pond`, `flower-forest`, `high-terraces`, `oak-path`), exportados del ClaudeEntorno de la laptop (Minecraft 26.3, `%APPDATA%\.minecraft\saves\ClaudeEntorno`), que es más grande que el del zip. Se buscaron con los heightmaps de cada chunk (`OCEAN_FLOOR`, `WORLD_SURFACE`, `MOTION_BLOCKING_NO_LEAVES`) y el bioma: agua donde el bloqueo de movimiento queda arriba del piso, hojas donde la superficie queda arriba del bloqueo sin hojas. Cada centro y giro se calificó con las mismas reglas de arriba, solo en biomas con el tinte de pasto de llanura (`plains`, `forest`, `birch_forest`, `river`...), porque el `mundo.py` de `main` todavía no tiñe por bioma. Luego se vieron 12 candidatos con la cámara de paseo y se eligieron 6.
- Minecraft 26.3 guarda la paleta de bloques como `{'': 'minecraft:stone'}` en lugar de `{Name, Properties}`, y omite las propiedades con valor por defecto (por ejemplo `half=lower`). `mundo.py` lee los dos formatos.
- En otra PC, las texturas de esos 6 lugares se copian del jar con el comando de "Problemas conocidos"; no hace falta el mundo de la laptop.
- `mundo.py` ahora tiñe las hojas de abedul y abeto con su color fijo y dibuja la hojarasca (`leaf_litter`) como una capa plana café. Antes salían grises y como cruces blancas.

## Vida en el fondo (mobs y hora del día)

- `herramientas/temas/minecraft-original/vida.js` (se sirve como `/vendor/tema/vida.js`):
  - `loadMobs(imgs, kinds)` carga las texturas de `mobs/` (las copia `extraer.py`; no se suben).
  - `setTime(world, hora, { terrain, clouds, imgs })` cambia el cielo, la niebla, la luz del terreno y las nubes, y pone sol o luna (y estrellas de noche). Horas: `day`, `dawn`, `dusk`, `night`. Devuelve la luz para los mobs.
  - `planLife(terrain, grupos, { seed })` busca un lazo cerrado para cada mob donde de verdad puede caminar (sin agua, árboles ni escalones de más de un bloque, lejos del lote del recorrido), o en el agua para los calamares. `grupos = [{ kind, count, graze }]`; `graze` es cuántos se quedan quietos comiendo.
  - `makeLife(imgs, terrain, specs, TOTAL, luz)` devuelve `{ g, update(t) }`. Cada lazo se recorre un número entero de veces en `TOTAL`, así que el loop del video no se rompe.
- Mobs disponibles (modelos del juego hechos de cajas con su textura): `cow`, `pig`, `sheep`, `chicken`, `wolf`, `squid`, `zombie`, `skeleton`, `creeper` y `spider` (con ojos que brillan de noche).
- Por zona: pradera y lomas con vacas, ovejas, cerdos y gallinas; bosques con lobos; agua con calamares; de noche, zombis, esqueletos, creepers y arañas.
- La luz de la hora oscurece el terreno y los mobs, pero no el grupo `stage` del recorrido: de noche los bloques del algoritmo siguen bien iluminados.
- Otro agente cambió `makeLife` para el #60: los mobs pisan alturas enteras y saltan los escalones. #1 a #7 y #124 se renderizaron con la versión anterior (subían los escalones de forma suave); #102 y #60, con la nueva.

## Efectos de sonido

- En cualquier escena: `self.sfx("nombre", gain, delay=0)` agenda un sonido en el momento actual (más `delay`). Cada escena guarda sus sonidos en `media/sfx/<Escena>.json` al renderizarse.
- El paso `mux` de `build.py` mezcla esos sonidos con la voz, sin bajar el volumen de la voz. Los archivos salen de `sounds/<nombre>.ogg` del tema.
- Volúmenes que funcionaron: 0.22 a 0.45. Los sonidos del juego son fuertes y no deben tapar la narración.

## Música de fondo

**Regla de Aldo (2026-10-25): todos los videos y shorts llevan música de fondo**, del OST de Minecraft (C418) que ya tenemos sacado del juego instalado. No se descarga música de internet: sale de los archivos de Minecraft Java de Aldo, igual que las texturas y los sonidos.

### Cómo agregarla

1. Las canciones viven en `herramientas/temas/minecraft-original/music/<pista>.ogg`. Si faltan (PC nueva o carpeta vacía), correr `extraer.py 26.3` en esa carpeta: las copia del índice de assets del juego (`%APPDATA%\.minecraft\assets`) según el diccionario `MUSIC`.
2. En el `video.json` del video:
   ```json
   "musica": {"pista": "subwoofer_lullaby", "volumen": 0.45}
   ```
   Si el video dura más que una canción, una lista (se tocan en orden):
   ```json
   "musica": {"pista": ["subwoofer_lullaby", "mice_on_venus"], "volumen": 0.45}
   ```
3. Correr `build.py` completo, o solo `build.py mux` si el video ya estaba hecho (la imagen no se vuelve a renderizar).
4. Revisar que en la salida diga `music <pistas>` y que la duración del video y del audio coincidan. Escuchar el cambio de canción si hay más de una.

### Canciones disponibles (C418, Minecraft Volume Alpha y Beta)

- `subwoofer_lullaby`: 209 s. **La favorita de Aldo**, la primera opción.
- `mice_on_venus`: 281 s, sin silencios.
- `haggstrom`: 191 s, sin silencios.
- `sweden`: 230 s. Tiene una pausa propia de 10 s a los 127 s.
- `danny`: 255 s.
- `minecraft`: 261 s.
- `clark`: 202 s.
- `living_mice`: 188 s.
- `wet_hands`: 90 s.
- `dry_hands`: 68 s.

Para agregar otra, ponerla en `MUSIC` de `extraer.py` (su ruta es `music/game/<nombre>`; la lista completa está en el índice `assets/indexes/<id>.json`, en las claves `minecraft/sounds/music/game/...`) y volver a correr `extraer.py`.

### Qué hace `build.py` con la música

- La recorta a la duración del video, con 2 s de entrada y 3 s de salida suaves (así el loop no salta), y la mezcla sin bajar la voz.
- Con una lista: cruce de 4 s entre canciones, y a todas menos la última se les quita el silencio del final.
- Iguala cada canción a la media de Subwoofer Lullaby (-34.8 dB) con `volumedetect`, porque entre canciones de C418 hay hasta 7 dB de diferencia. `volumen` se aplica después: con 0.45 la música queda unos 16 dB debajo de la voz.

### Notas

- La música está en `.gitignore` (`music/`). Nunca subir assets de Mojang al repo.
- **Riesgo al publicar:** las canciones de C418 pueden recibir reclamos de derechos de autor en YouTube; no entran en los permisos de Mojang para videos. Aldo ya lo sabe y aun así la quiere en todos los videos. En la descripción del video se pone la línea "🎵 Music: C418 - <canción> (Minecraft Volume Alpha)".
- Videos con música: `trees/0297-serialize-tree` (Subwoofer Lullaby), el largo de árboles (Subwoofer Lullaby + Mice on Venus) y el short `tree-basics/shorts/02-dfs` (Subwoofer Lullaby). Los demás videos ya hechos todavía no la tienen.

## Errores ya cometidos (no repetir)

Aldo los encontró en el #297 o salieron en su revisión. Antes de entregar un video, revisar esta lista uno por uno en las hojas de cuadros.

1. **Varillas encima de los bloques.** Si las líneas de un árbol se animan después de que los bloques ya están en escena, quedan por encima. Solución: `self.add(edges, *blocks)` antes de `Create(edges)` (las líneas primero, los bloques al frente). Lo mismo al mover un grupo con `.animate`: Manim lo vuelve a dibujar en el orden del `VGroup`, así que las varas van primero (`VGroup(edges..., blocks...)`). Pasó en la caída del subárbol del largo de árboles (2026-10-25).
2. **Pixel art pintado de un color.** `Indicate(..., color=...)` sobre bloques, objetos o barreras los vuelve un cuadro sólido. Solución: un pulso de escala (`m.animate(rate_func=there_and_back).scale(1.15)`). `Indicate` solo en texto.
3. **Íconos 3D tapados por el terreno.** Los sprites (barreras, orbes) desaparecen cuando el terreno queda detrás. Solución: `stage.traverse((o) => { if (o.isSprite) o.renderOrder = 10; })`.
4. **Comas que parecen puntos.** Cada pieza de texto se centra por sus píxeles y la coma sube. Solución: piezas con caja de altura de línea completa (`glyphs` en el #297) y `arrange(RIGHT, buff=0)`.
5. **Bloques del inventario que se ven aplastados.** Un número encima del ícono isométrico tapa la cara de arriba y el bloque parece plano. Solución: el valor en la esquina inferior derecha, dentro de la casilla, como la cantidad en el juego (`slot_item` del #297). `item_stack` del tema todavía pone el valor encima: no usarlo así en videos nuevos.
6. **Aviso de logro tapando el 3D.** El `toast` de ancho 5.6 en `TOP_Y` tapaba el bloque de arriba. Revisar qué hay del 3D en esa esquina; en el #297 se usó `w=4.6` en y = 5.5.
7. **Contenido 3D fuera del cuadro.** La cámara de la plantilla no sirve para otra forma (un árbol es más alto que una fila). Probar con cuadros sueltos (`--stills`) antes del clip completo. El contenido 3D debe quedar entre los píxeles 130 y 735 de alto, arriba del inventario.
8. **Linter por eventos muy juntos.** Si dos eventos del recorrido caen a menos de 0.35 s, los `beat` se acumulan y se pasan del tiempo de la línea. Usar `rt` de 0.08 a 0.15 en esos eventos.
9. **Aviso de logro tapando el encabezado.** Con encabezados largos ("WALK BOTH CHAINS") el `toast` los corta. En el recorrido, encabezados de 11 letras o menos y `toast(..., w=4.6)`.
10. **Bloques que se vuelven cuadros blancos.** `set_opacity` sobre un `Block` también rellena su borde invisible. Para atenuar pixel art, poner encima un rectángulo negro semitransparente (`veil` en el #4).
11. **Nombres que tapan los del tema.** Una función propia llamada `level_text` tapó la del tema (el número verde de nivel). No reusar nombres de `prelude.py` ni de `tema.py`.
12. **El linter falla con listas vacías.** El escenario falso del linter devuelve grupos vacíos; indexar una lista hecha de ellos (`flies[k]`) rompe la simulación. Recorrer con `zip` en lugar de índices.
13. **Textos que no caben.** Una cuenta larga en fuente PIXEL (`964632435 > 214748364 overflow!`) o varias cajas `chat` seguidas se salen del cuadro. Cada `chat` agrega 0.56 de relleno: juntar el texto en menos cajas o bajar el tamaño.
14. **Narración que no coincide con el dibujo.** En el #6 la narración decía "most of that grid stays empty" y en la cuadrícula de 3 × 7 solo faltan 7 de 21. Se corrigió a "a third".
15. **La fuente del juego no tiene todo.** No hay `³`, `≠` ni `✓`, y `..` se ve como un punto. Usar `^3`, `!=`, `ok` y palabras ("from 0 to 5").
16. **Silencios muertos al clonar voces lentas con TTS de IA (`Qwen3-TTS`).** Si el audio de referencia tiene pausas de ~1 s entre frases (como pasó en `04_madura_sensual.mp3`), el LLM imita esas pausas y llega a meter silencios de más de 5 s a mitad de una línea (en la línea 2 del #4 metió 5.75 s de silencio antes de `"That's eleven"`). Solución: pasar tanto el audio de referencia como cada clip generado por `silenceremove` de `ffmpeg` (máximo `0.20–0.22 s` por pausa más `0.08 s` de cola con `apad`), como hace `tts_qwen_clone.py`, y verificar con `silencedetect` que no quede ningún silencio mayor a `0.45 s`.
17. **Valores encima de los bloques.** Un orbe con número (`orb_num`) que viaja al centro de un bloque y se queda ahí tapa el número del bloque. Al sumar, que se hunda y desaparezca: `FadeOut(v, target_position=bloque, scale=0.3)`. Cuando espera a un lado, dejar al menos 1.2 unidades del centro de un bloque de 0.95 (con 0.95 tocaba el borde). Pasó en la recursión del largo de árboles (2026-10-25).

## Lista de revisión antes de entregar

- `build.py` imprime la duración del video y la del audio: deben coincidir.
- El video lleva música de fondo: la salida de `build.py` dice `music <pistas>`.
- Hojas de cuadros con `sheet.py` (`python ../../../herramientas/sheet.py hoja.png 3 --video video.mp4 1,5,12,...`) y revisar cada escena: textos que se enciman, letras tapadas, cosas cortadas en los bordes, el código tapado por el 3D.
- Probar el render 3D con cuadros sueltos antes del clip completo:
  ```bash
  node ../../../herramientas/three/render.mjs --page three/walk.html --stills 2,10,25 --outdir review3d
  # con tema: agregar --tema ../../../herramientas/temas/minecraft-original
  ```
- Loop: comparar el primer y el último cuadro (diferencia media menor a 1).
- La narración debe decir exactamente lo que se ve. Si un dato de la narración es falso para el ejemplo, se cambia la narración, no se esconde el dibujo.

## Problemas conocidos

- Los heredocs de Bash corrompen las barras invertidas de TeX (`\t`, `\a`). Escribe esos archivos con Write.
- Renders en paralelo pueden chocar en la caché de texto de Manim. `build.py` reintenta uno por uno las escenas que fallan. Los registros quedan en `media/log_<Escena>.txt`.
- El linter simula las escenas con objetos falsos: en funciones que crean filas, llama `row.move_to(...)` en una línea aparte y luego `return row`.
- Consolas no tiene "⇄": usa "→".
- Etiquetas 3D que deben verse siempre encima: `depthTest: false` en su material.
- Si la memoria del equipo está baja, Claude Code puede cerrar los visores que corren en segundo plano. Los videos no se pierden.
- El linter solo ve los nombres que aparecen en `script.py`. Por eso un tema que hereda de otro se pega completo con `# extends:` y no se carga con `exec`. Además, el escenario falso del linter inventa atributos, así que se usa `self.__dict__.get(...)` y no `getattr`.
- `ImageMobject` falla con el Pillow del venv ("Invalid mode for data type"). El pixel art se dibuja con `pixel_image`, que lo convierte en rectángulos vectoriales.
- Con la fuente del juego, los espacios iniciales no tienen píxeles. Cada línea de código lleva un rectángulo invisible del ancho completo para no perder la sangría.
- La mezcla de audio va en mono. Pasar la voz mono a estéreo la bajaba 3 dB.
- En `mundo.html`, los sprites (barreras, orbes, letreros de texto) pueden quedar tapados por el terreno: sus materiales son transparentes y se ordenan junto con los del terreno. Después de crear todo, usar `stage.traverse((o) => { if (o.isSprite) o.renderOrder = 10; })`.
- Si en una PC faltan texturas de bloques en `mundos/tex/` (el terreno sale con huecos o cuadros sin textura), copiarlas del jar sin volver a exportar, desde `herramientas/temas/minecraft-original`: `python -c "import json,glob,mundo; n=set(); [n.update(json.load(open(f,encoding='utf8')).get('names',[])) for f in glob.glob('mundos/*.json') if 'lugares' not in f]; mundo.block_textures(sorted(n),'mundos/tex')"`. Volver a exportar desde un mundo distinto cambiaría los `.json` de los lugares.
- **Nombres que chocan sin que el linter avise.** Un ayudante `pick()` y la variable local `pick = pickaxe(...)` de una escena: el linter pasa (usa objetos falsos), pero el render real falla. No reusar `pick`, `bar`, `code`, `row`, `idx` como nombres de funciones.
- El `sed` de macOS no entiende `\b`: para cambiar nombres en archivos usar Python con `re`.
- **El linter reescribe los sonidos.** `lint` simula las escenas y llama `self.sfx`, así que deja `media/sfx/<Escena>.json` con menos sonidos (sus objetos falsos tienen otro largo). Si después solo se renderizan algunas escenas, las demás se mezclan con los sonidos del linter (en el #3644 bajaron de 61 a 55). Después de `lint`, renderizar todas las escenas (`build.py render composite sync mux`) o no correr `lint` antes de un `mux` parcial.
- **El linter exige una línea de narración en cada escena.** Si una escena no llama `self.seg()`, sale "Check incomplete. Unchecked scenes" y `build.py` se detiene. Para una escena sin voz (el letrero de los shorts), usar una línea con texto vacío y llamar `self.seg(i)`.
- `sheet.py` hace mosaicos de 360 × 480 (3:4): para 16:9 o 9:16 deforma los cuadros. En la sesión del 2026-10-24 se usó un script aparte con el tamaño correcto.
- ffmpeg 8 o más nuevo ya no tiene `-filter_complex_script`; `build.py` pasa el grafo de audio directo en `-filter_complex`.
- `script.py` lleva `TEMA_DIR` con la ruta absoluta de la PC (con el usuario local). Desde el lote #8–#19 no se sube a git; los anteriores lo tienen con la ruta de la otra PC y cada build lo vuelve a escribir: no subas esos cambios.
- Para renderizar un video que ya tiene el código listo (o retomar un render cortado), ver `RENDER.md`.
- Varios videos a la vez con subagentes: funcionó darles un documento común con las reglas (solo su carpeta, sin commits ni cambios de rama, sin tocar herramientas ni `GUIA.md`, notas en `NOTAS.md`) y el diseño de cada video. Cuatro renders a la vez en la laptop fueron lentos pero terminaron; una caída de red detiene a todos los subagentes y hay que reanudarlos.
- El juego puede estar abierto mientras se lee el mundo, pero solo se ve lo que ya se guardó. Si se construye algo nuevo, hay que guardar (salir al menú) y volver a exportar.
