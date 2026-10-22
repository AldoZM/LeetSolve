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
9. Si Aldo pide música: agregar `"musica"` a `video.json` y correr solo `build.py mux`.

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
- Narración en inglés con la voz `af_heart` (Kokoro, local). Duración típica: 85 a 105 segundos.
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

Secciones (por tema de LeetCode): `arrays-hashing`, `linked-list`, `sliding-window`, `binary-search`, `strings`, `math`, `trees`, `two-pointers`, `backtracking`. Crea una sección nueva cuando el problema no encaje, con nombre en inglés y en kebab-case (`graphs`, `dynamic-programming`, `two-pointers`...). La carpeta del video lleva el número del problema con 4 dígitos: `videos/trees/0102-level-order`.

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
- `pruebas/0001-two-sum-horizontal`: primera prueba en 16:9, sin código a la par.
- `pruebas/0001-two-sum-minecraft`: Two Sum con el tema de Minecraft. Se arma con `python ../../herramientas/build.py` (está a dos niveles, no a tres).
- `pruebas/0001-two-sum-minecraft-original`: **plantilla del estilo aprobado**. Two Sum con los assets y sonidos del juego, en el mundo ClaudeEntorno.

Al terminar un video nuevo, agrégalo a esta lista.

Los videos terminados se copian a `export/` en la raíz con el nombre `<Título> #<número>.mp4` (por ejemplo `4Sum #18.mp4`), listos para subir. Esa carpeta no se sube a git.

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

## Lugares del mundo

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

- Opcional, en `video.json`: `"musica": {"pista": "subwoofer_lullaby", "volumen": 0.45}`. El archivo sale de `music/<pista>.ogg` del tema; `extraer.py` lo copia del juego (diccionario `MUSIC`, con la ruta del índice de assets, por ejemplo `music/game/subwoofer_lullaby`).
- `build.py` la recorta a la duración del video, con 2 s de entrada y 3 s de salida suaves (así el loop no salta), y la mezcla sin bajar la voz.
- Con `volumen` 0.45, Subwoofer Lullaby queda unos 16 dB debajo de la voz.
- La música está en `.gitignore` (`music/`).
- **Riesgo al publicar:** las canciones de C418 (Subwoofer Lullaby, Sweden, Wet Hands...) reciben reclamos de derechos de autor en YouTube; no entran en los permisos de Mojang para videos. Se usa solo cuando Aldo lo pide, y antes de publicar se le recuerda.
- Primer video con música: `trees/0297-serialize-tree` (Subwoofer Lullaby, a petición de Aldo).

## Errores ya cometidos (no repetir)

Aldo los encontró en el #297 o salieron en su revisión. Antes de entregar un video, revisar esta lista uno por uno en las hojas de cuadros.

1. **Varillas encima de los bloques.** Si las líneas de un árbol se animan después de que los bloques ya están en escena, quedan por encima. Solución: `self.add(edges, *blocks)` antes de `Create(edges)` (las líneas primero, los bloques al frente).
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

## Lista de revisión antes de entregar

- `build.py` imprime la duración del video y la del audio: deben coincidir.
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
- ffmpeg 8 o más nuevo ya no tiene `-filter_complex_script`; `build.py` pasa el grafo de audio directo en `-filter_complex`.
- `script.py` lleva `TEMA_DIR` con la ruta absoluta de la PC (con el usuario local). Desde el lote #8–#19 no se sube a git; los anteriores lo tienen con la ruta de la otra PC y cada build lo vuelve a escribir: no subas esos cambios.
- Para renderizar un video que ya tiene el código listo (o retomar un render cortado), ver `RENDER.md`.
- Varios videos a la vez con subagentes: funcionó darles un documento común con las reglas (solo su carpeta, sin commits ni cambios de rama, sin tocar herramientas ni `GUIA.md`, notas en `NOTAS.md`) y el diseño de cada video. Cuatro renders a la vez en la laptop fueron lentos pero terminaron; una caída de red detiene a todos los subagentes y hay que reanudarlos.
- El juego puede estar abierto mientras se lee el mundo, pero solo se ve lo que ya se guardó. Si se construye algo nuevo, hay que guardar (salir al menú) y volver a exportar.
