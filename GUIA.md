# LeetSolve: guía para hacer los videos

Videos que explican problemas de LeetCode con Manim, voz Kokoro y una sección 3D en Three.js. Esta guía es el contexto completo: léela antes de crear o modificar un video. Lo que pasó en cada sesión está en `BITACORA.md`.

## Estilo aprobado (desde 2026-10-20)

Los videos nuevos se hacen con el **estilo Minecraft con assets del juego y su mundo de fondo**. Aldo lo aprobó con "Quedó perfecto". La plantilla es `pruebas/0001-two-sum-minecraft-original`.

- Tema `minecraft-original`: texturas, interfaz, fuente y sonidos del juego instalado (ver "Temas visuales").
- Todo el video pasa en el mundo **ClaudeEntorno**, en la pradera del spawn: un solo clip 3D de punta a punta (ver "Fondo con un mundo real").
- Escenas 2D sobre el mundo **desenfocado y oscurecido**. La parte 3D va nítida, en un lote de pasto aplanado con la montaña detrás.
- Efectos de sonido del juego mezclados bajo la voz (ver "Efectos de sonido").
- Los 9 videos de la lista hechos antes usan el estilo neón original y se quedan así.

### Receta para un video nuevo en este estilo

1. **Una sola vez por PC:** `python herramientas/temas/minecraft-original/extraer.py`, y si `mundos/claude.json` no existe:
   `python herramientas/temas/minecraft-original/mundo.py export "%APPDATA%\.minecraft-youtube\saves\ClaudeEntorno" -11 71 -9 64 herramientas/temas/minecraft-original/mundos/claude.json`
2. Crear `videos/<seccion>/<numero>-<nombre>/` y copiar de la plantilla `video.json`, `scenes.py`, `make_walk.py` y `three/mundo.html`. No copiar `media/`, `timestamps.json`, `voiceover.mp3` ni `.tts-cache/`.
3. Escribir `narration.txt` del problema nuevo y generar la voz (paso 4 del flujo general).
4. Ajustar `video.json`: los grupos de escenas según las líneas nuevas, con `"tema": "minecraft-original"` y `"fondo": {"page": "three/mundo.html", "sharp": ["Scene5_Walk"]}`.
5. Reescribir `make_walk.py`: los datos del ejemplo, la mena de cada valor (`ores`), los eventos anclados a frases con `at(línea, "frase")` y `first`/`last` (las líneas del recorrido). Correrlo para generar `walk.json`.
6. Reescribir `scenes.py` con las mismas 7 escenas y los ayudantes del tema: `block_row`, `Inventory`, `Hotbar`, `toast`, `xp_bar`, `level_text`, `chest_icon`, `pickaxe`, `chat`, `MT`, `big_o_pow`. Agregar `self.sfx(...)` en los momentos clave.
7. En `three/mundo.html`, cambiar solo la parte del recorrido (objetos y eventos) según el algoritmo. El terreno, la cámara de paseo y la mezcla de cámaras (`W0`, `W1`) se quedan igual.
8. `python ../../../herramientas/build.py`, hojas de cuadros con `sheet.py`, revisar el loop y abrir el visor.

### Medidas que funcionaron (pantalla de 9 × 12)

- Encabezado (`hdr`) en `TOP_Y = 5.4` a la izquierda; letrero del target (`target_sign(0.6)`) arriba a la derecha.
- Recorrido: inventario del cofre (`Inventory(9)`, ancho 8.6) en y = -1.15; código en y = -4.3 con `max_h=3.25`; respuesta (`chat("return [...]")`) en y = 4.3.
- En `mundo.html`, el desplazamiento vertical de la vista va de 0.12 en el paseo (más cielo) a 0.34 en el recorrido, para que la fila y el cofre queden arriba del inventario. Con eso, el cofre va en z = 3.6 y la fila en z = 0, con bloques separados 1.2.
- Fondo de las escenas 2D: `gblur` sigma 5 y brillo al 82 %.
- Volumen de efectos: 0.22 a 0.45; el sonido de logro (`challenge`) en 0.32.

## Formato fijo de cada video

- Vertical 1080×1440 (3:4), 30 fps. Frame de Manim 9×12.
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

Secciones (por tema de LeetCode): `arrays-hashing`, `linked-list`, `sliding-window`, `binary-search`, `strings`, `math`, `trees`. Crea una sección nueva cuando el problema no encaje, con nombre en inglés y en kebab-case (`graphs`, `dynamic-programming`, `two-pointers`...). La carpeta del video lleva el número del problema con 4 dígitos: `videos/trees/0102-level-order`.

## Videos hechos

- `arrays-hashing/0001-two-sum`: Two Sum, Easy. Hecho antes de `build.py`, usa su propio `sync.py`.
- `linked-list/0002-add-two-numbers`: Add Two Numbers, Medium. Primer video con 3D, también usa su propio `sync.py`.
- `sliding-window/0003-longest-substring`: Longest Substring Without Repeating Characters, Medium. Ejemplo "abcbdea".
- `binary-search/0004-median-two-arrays`: Median of Two Sorted Arrays, Hard. Mediana 11.
- `strings/0005-longest-palindrome`: Longest Palindromic Substring, Medium. Ejemplo "abaracecar".
- `strings/0006-zigzag-conversion`: Zigzag Conversion, Medium. PAYPALISHIRING con 3 filas.
- `math/0007-reverse-integer`: Reverse Integer, Medium. 1463 y el desbordamiento de 1534236469.
- `trees/0102-level-order`: Binary Tree Level Order Traversal, Medium.
- `trees/0124-max-path-sum`: Binary Tree Maximum Path Sum, Hard. Mejor camino 42.
- `pruebas/0001-two-sum-horizontal`: primera prueba en 16:9, sin código a la par.
- `pruebas/0001-two-sum-minecraft`: Two Sum con el tema de Minecraft. Se arma con `python ../../herramientas/build.py` (está a dos niveles, no a tres).
- `pruebas/0001-two-sum-minecraft-original`: **plantilla del estilo aprobado**. Two Sum con los assets y sonidos del juego, en el mundo ClaudeEntorno.

Al terminar un video nuevo, agrégalo a esta lista.

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

## Efectos de sonido

- En cualquier escena: `self.sfx("nombre", gain, delay=0)` agenda un sonido en el momento actual (más `delay`). Cada escena guarda sus sonidos en `media/sfx/<Escena>.json` al renderizarse.
- El paso `mux` de `build.py` mezcla esos sonidos con la voz, sin bajar el volumen de la voz. Los archivos salen de `sounds/<nombre>.ogg` del tema.
- Volúmenes que funcionaron: 0.22 a 0.45. Los sonidos del juego son fuertes y no deben tapar la narración.

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
- El juego puede estar abierto mientras se lee el mundo, pero solo se ve lo que ya se guardó. Si se construye algo nuevo, hay que guardar (salir al menú) y volver a exportar.
