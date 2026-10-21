# Instrucciones para un modelo de IA: cómo hacer un video de LeetSolve

Este documento es para cualquier modelo de IA (Claude, GPT, Gemini u otro) que vaya a crear un video nuevo en este repositorio. Si lo sigues al pie de la letra, el video sale con el mismo formato, estilo, ritmo y calidad que la plantilla aprobada.

- `GUIA.md` tiene el contexto completo y los problemas conocidos. Léela también.
- `BITACORA.md` dice qué se hizo en cada sesión.
- Si algo de este documento choca con `GUIA.md`, manda `GUIA.md`.

## 1. Qué vas a producir

Un video vertical que explica un problema de LeetCode, ambientado en Minecraft:

- **La plantilla aprobada es `pruebas/0001-two-sum-minecraft-original`.** Antes de escribir nada, lee completos sus archivos `narration.txt`, `video.json`, `make_walk.py`, `scenes.py` y `three/mundo.html`. Tu video debe parecer un episodio más de esa serie.
- **Formato:** 1080×1920 (9:16), 30 fps, con `"formato": "9:16"` en `video.json`. Las escenas de Manim se hacen en 1080×1440 con un frame de 9 × 12 unidades (x de -4.5 a 4.5, y de -6 a 6) y van centradas sobre el mundo 3D, que llena el resto (ver "Formato fijo" en `GUIA.md`).
- **Duración:** de 85 a 105 segundos. La plantilla dura 97.2 s.
- **Narración:**
  - En inglés, con la voz Kokoro `af_heart` (local).
  - Unas 20 líneas a unas 2.5 palabras por segundo.
- **Fondo:** todo el video pasa dentro de un mundo real de Minecraft, el mundo ClaudeEntorno, en la pradera del spawn.
  - Las escenas 2D van encima del mundo desenfocado: blur gaussiano sigma 5 y brillo al 82 %.
  - La escena del recorrido del algoritmo va en 3D y nítida.
- **Interfaz:** texturas, interfaz, fuente y sonidos del juego (tema `minecraft-original`).
- **Código:** se muestra a la par de la solución. Una barra resalta la línea que se está ejecutando.
- **Loop:** el último cuadro es igual al primero. La portada `cover()` abre y cierra el video.
- **Efectos de sonido:** sonidos del juego mezclados bajo la voz, sin taparla.
- **Música:** opcional. Se pone solo si Aldo la pide para ese video (ver "Música de fondo" en `GUIA.md`).

## 2. Preparar la PC (una sola vez)

Necesitas:

- **Python 3.12** en un venv con:
  - `manim==0.22.*`
  - `kokoro>=0.9.4`
  - `soundfile`
  - `pygments`
  - Pillow
- **Una distribución de LaTeX** (MiKTeX o TeX Live).
- **ffmpeg y ffprobe** en el PATH.
- **Node 18 o más nuevo.** En `herramientas/three` corre `npm ci` y luego `npx playwright install chromium`.
- **Las herramientas de la skill** `github.com/Yusuke710/manim-skill`: `tts-generate.py`, `lint-subtitles.py` y `video_viewer.py`, que están en su carpeta `skills/manim-skill/tools/`.
  - `build.py` las busca en `~/.manim-skill-src/skills/manim-skill/tools`.
  - Si están en otro lugar, define la variable de entorno `MANIM_SKILL_TOOLS`.
- **Minecraft Java Edition** instalado y abierto al menos una vez, en la versión 26.2 o más nueva.

Antes de cada comando:

```bash
export PYTHONUTF8=1   # obligatorio en Windows: las herramientas imprimen "→"
# y el venv de Python 3.12 primero en el PATH; usa `python`, nunca `python3`
```

Assets del juego y mundo:

1. Copia los assets del juego instalado:
   ```bash
   python herramientas/temas/minecraft-original/extraer.py
   ```
   Copia texturas, interfaz, fuente y 23 sonidos a `tex/`, `gui/`, `font/` y `sounds/`.
2. El mundo viene en el repositorio:
   - `herramientas/temas/minecraft-original/mundos/ClaudeEntorno.zip` es el mundo completo. Descomprímelo en la carpeta `saves` de Minecraft si quieres recorrerlo en el juego.
   - `mundos/claude.json` son los bloques visibles alrededor del spawn, ya exportados.
3. Faltan las texturas de esos bloques (`mundos/tex/`), que no se suben. Para crearlas, vuelve a exportar desde el mundo descomprimido:
   ```bash
   python herramientas/temas/minecraft-original/mundo.py export "<saves>/ClaudeEntorno" -11 71 -9 64 herramientas/temas/minecraft-original/mundos/claude.json
   ```
   El centro es (-11, 71, -9) y el radio es 64.

## 3. Paso a paso de un video nuevo

### 3.1 Carpeta

`videos/<seccion>/<numero de 4 dígitos>-<nombre-corto>/`. Ejemplos: `videos/arrays-hashing/0217-contains-duplicate`, `videos/two-pointers/0011-container-with-most-water`.

- Secciones existentes: `arrays-hashing`, `linked-list`, `sliding-window`, `binary-search`, `strings`, `math`, `trees`.
- Si el problema no encaja, crea una sección en inglés y en kebab-case.

Copia de la plantilla `video.json`, `scenes.py`, `make_walk.py` y `three/mundo.html`. **No copies** `media/`, `timestamps.json`, `voiceover.mp3`, `.tts-cache/`, `script.py` ni `video.mp4`.

### 3.2 Ejemplo

- Elige un ejemplo **pequeño**: de 5 a 7 valores, para que quepan en la fila de bloques y en las 9 casillas del inventario.
- El ejemplo debe mostrar la idea clave: un descarte, una actualización del mejor, un caso que rompe la solución ingenua.
- **Calcula la respuesta con Python antes de escribir la narración.**
- Cada valor del arreglo es un bloque de mena. Asigna una mena distinta a cada uno de esta lista: `coal`, `iron`, `redstone`, `lapis`, `gold`, `diamond`, `emerald`.

### 3.3 Narración (`narration.txt`)

Escríbela con una herramienta de escritura de archivos, no con un heredoc de Bash, porque los apóstrofos lo rompen. El formato es exacto:

```
subtitles:
- Primera línea.
- Segunda línea.
```

Estructura de la plantilla, con 20 líneas y sus índices:

- **0 · Scene1_Hook.** Gancho: "<Nombre>, Minecraft edition. LeetCode problem number N, and ...".
- **1 y 2 · Scene2_Problem.** El enunciado contado con el mundo: la fila de bloques es el arreglo, el letrero es el target.
- **3 a 6 · Scene3_Brute.** La idea directa, cómo funciona, cuánto cuesta en el ejemplo (el pico se gasta) y cómo crece con n grande.
- **7 y 8 · Scene4_Idea.** El truco y su nombre: complemento, ventana, dos punteros...
- **9 a 15 · Scene5_Walk.** Presentar la estructura (el cofre es el hash map), la pregunta de cada paso y el recorrido valor por valor hasta el logro: "Advancement made. The answer is ...".
- **16 y 17 · Scene6_Complexity.** Tiempo y espacio, y la comparación con la idea directa.
- **18 y 19 · Scene7_Outro.** El código completo y la lección en una frase.

Reglas:

- Frases cortas, en inglés natural, con números escritos como palabras ("twenty three").
- **La narración dice exactamente lo que se ve.** Si un dato dicho es falso para el ejemplo, se corrige la narración, no se esconde el dibujo.
- Puedes cambiar el número de líneas por escena según el problema. Ajusta los índices en `video.json` y en `scenes.py`.

### 3.4 Voz

```bash
python "$MANIM_SKILL_TOOLS/tts-generate.py" --narration narration.txt
```

Confirma que el número de clips es igual al de líneas. Lee `timestamps.json`: cada `duration_s` es el presupuesto exacto de esa línea.

### 3.5 `video.json`

```json
{"tema": "minecraft-original",
 "groups": [["Scene1_Hook", [0]], ["Scene2_Problem", [1, 2]], ["Scene3_Brute", [3, 4, 5, 6]], ["Scene4_Idea", [7, 8]],
            ["Scene5_Walk", [9, 10, 11, 12, 13, 14, 15]], ["Scene6_Complexity", [16, 17]], ["Scene7_Outro", [18, 19]]],
 "fondo": {"page": "three/mundo.html", "sharp": ["Scene5_Walk"]}}
```

Puedes cambiar los nombres de `Scene3_*` y `Scene4_*` (por ejemplo `Scene3_DFS`). `Scene1_Hook`, `Scene5_Walk` y `Scene7_Outro` se llaman siempre así.

### 3.6 `make_walk.py` y `walk.json`

`make_walk.py` calcula el algoritmo sobre el ejemplo y escribe `walk.json`. Ese archivo tiene los datos (`nums`, `target`, `ores`), los pasos y el momento de cada evento. Lo usan tanto Manim como Three.js, así que los dos quedan sincronizados.

- Cada evento es `[línea, segundos dentro de la línea]`.
- Ánclalos a frases de la narración con `at(línea, "frase")`: así el bloque se ilumina cuando la voz lo nombra.
- `first` y `last` son los índices de la primera y la última línea de `Scene5_Walk`.

### 3.7 `scenes.py`

Conserva las 7 clases y su estilo. **Nunca edites `script.py`**: `build.py` lo genera pegando `prelude.py`, el tema y `scenes.py`.

Reglas de tiempo (de `prelude.py`):

- `self.seg(i)` al empezar la línea i de narración y `self.close_seg()` al terminarla.
- Anima solo con `self.beat(*anims, rt=s)` y espera con `self.until(u)`, donde u son los segundos dentro de la línea actual, o con `self.hold(t)`.
- `self.clear_all()` limpia la pantalla. `self.finish(anim, rt=s)` hace que algo termine justo al cerrar la línea.
- Nunca pongas `until(DUR - 0.5)` antes de `clear_all()`: se pasa del presupuesto.
- `self.sfx("nombre", gain, delay=0)` agenda un sonido en el momento actual.
- Todo está cuantizado a cuadros. No uses `self.play` ni `self.wait` directamente.

Componentes del tema:

- **Texto:**
  - `MT(s, size, color, font)`: fuente del juego con sombra dura. `font=PIXEL` para números y títulos, `font=TERM` para texto.
  - `chat(s, color, size)`: texto con la caja translúcida del chat.
- **Títulos:**
  - `stone_title("TITLE", 60, width=7.8)` en y = 4.0.
  - `splash("...", 21)` amarillo y girado, en (2.25, 2.75).
  - `hdr(texto, color)` es el encabezado de escena: `chat` de tamaño 42 en `TOP_Y = 5.4`, pegado a la izquierda.
- **Datos:**
  - `block_row(values, y, size=1.05, gap=0.2)`: bloques de mena con el número en la cara.
  - `index_row` pone los índices debajo.
- **Estructuras:**
  - `Inventory(9, "Chest")`: pantalla del cofre, ancho 8.6. Tiene `.item(k, valor, cantidad)` y `.title_for(texto)`.
  - `Hotbar(9)`: barra de objetos, con `.item` y `.selector`.
  - `sign(["target", "23"], ...)`: letrero de madera.
  - `chest_icon`, `pickaxe`, `iso_block`.
- **Logro:** `toast("Advancement Made!", "<Problema> solved")`. Entra desde la derecha a la altura de `TOP_Y`.
- **Complejidad:**
  - `xp_bar(7.4)`: barra de experiencia que se llena con `Restore`.
  - `level_text("O(n)", 1.05)`: número verde de nivel.
  - `big_o_pow("n", 2, size, MC_RED)`.
- **Código:**
  - `code_panel(src, y, width=8.4, max_h=...)`: colores del chat del juego y fondo negro al 86 %.
  - `line_bar(code, k0, k1, color)` es la barra de línea activa.
- **Marcos:** `outline(m, color, width)` es el contorno pixelado.
- **Colores:**
  - `MC_WHITE`, `MC_GRAY` y `MC_DGRAY` para texto y apoyos.
  - `MC_YELLOW` para lo activo.
  - `MC_GOLD` para el truco y la respuesta.
  - `MC_GREEN` para lo correcto.
  - `MC_AQUA` y `MC_RED` para lo que falla o cuesta.
  - `MC_PINK` está disponible.
- **Portada:** `cover()` dibuja título, splash, fila de bloques con índices, pico, cofre y etiquetas. Las etiquetas son `chat` de tamaño 46 en y = -3.05: "LeetCode #N", la dificultad y el tema. Se usa en `Scene1_Hook` y al final de `Scene7_Outro`.

Medidas aprobadas:

- **`Scene5_Walk`:** inventario en y = -1.15, código en y = -4.3 con `max_h=3.25` y respuesta en y = 4.3. El letrero del target va a escala 0.6, arriba a la derecha.
- **`Scene3_*`:** fila en y = 3.0 y código en y = -3.7 con `max_h=2.9`.
- **`Scene7_Outro`:** código en y = 1.6 y la lección en y = -2.3.
- **Bordes:** nada a menos de 0.3 del borde del frame.

### 3.8 `three/mundo.html`

Cambia **solo** el contenido del recorrido: los objetos dentro del grupo `stage` y sus animaciones en `renderAt(t)`.

**Elige para tu video (ver "Lugares del mundo" y "Vida en el fondo" en `GUIA.md`):**
- Un lugar de `mundos/lugares.json` que ningún otro video use: `makeTerrain('/vendor/tema/mundos/<lugar>.json', { turn, plot: [-5, 5, -2, 7], clear: [-10, 10, 7, 24] })`. Anota tu video en `lugares.json`. No repitas lugares: Aldo pidió que cada video tenga el suyo.
- Una hora (`setTime`) y los mobs de esa zona (`loadMobs`, `planLife`, `makeLife` y `life.update(t)` en `renderAt`). Copia el bloque de un video del 2026-10-21, por ejemplo `trees/0102-level-order/three/mundo.html`.
- `walkPose`, para que tu contenido 3D quepa entre los píxeles 130 y 735 de alto y no se corte por los lados. Pruébalo con `--stills`.

**No cambies:**
- El mundo: `makeWorld({ fov: 40, offset: 0.34, fog: [55, 120] })` y las nubes.
- La cámara de paseo (`roamPose`) y su mezcla con la del recorrido (`k`), con entrada en `W0 - 1.6 → W0 - 0.1` y salida en `W1 + 0.1 → W1 + 1.6`.
- El desplazamiento vertical, que va de 0.12 a 0.34.

Medidas y reglas:

- **Posiciones:** fila de bloques en z = 0 con separación 1.2. El cofre o la estructura principal en z = 3.6.
- **Ayudantes de `mc.js`:** `makeBlock`, `makeChest`, `makeFrame`, `makeSign`, `pixelSprite`, `makeOrb`, `makeClouds`. De `/vendor/lib/stage.js`: `prog`, `easeInOut`, `easeOut`, `easeOutBack`, `lerp`, `V`, `bezier`, `pose`, `mixPose`.
- **Sprites:** después de crear todo, `stage.traverse((o) => { if (o.isSprite) o.renderOrder = 10; })`. Si no, el terreno los tapa.
- **Render determinista:** todo depende de `t`. Nada de relojes ni de `Math.random`; usa el generador con semilla de la plantilla.
- **Loop:** el clip dura todo el video y la cámara de paseo es periódica en `TOTAL`, por eso el loop cierra.

### 3.9 Efectos de sonido

Sonidos disponibles:

- `chestopen` y `chestclosed`: abrir y cerrar el cofre.
- `pop`: guardar un objeto o un dato que aparece.
- `orb`: acierto, se repite 4 veces con 0.2 s de separación.
- `levelup`: complejidad lineal.
- `challenge`: logro.
- `break`: el pico se rompe.
- `click` y `toast_in`.
- `stone_dig1` a `stone_dig4`: golpes y bloques que caen; alterna los números.
- `stone_step1` a `stone_step6`.
- `wood_dig1` a `wood_dig4`: el letrero, el cofre que aparece.
- `book_flip1` a `book_flip3` y `book_put`: libro (guardar o leer texto).
- `villager_no1` a `villager_no3`: el "no" del aldeano, para una idea que falla.

Texturas extra para 2D (`pixel_art`) y 3D (`loadTheme`): `barrier` (marca de vacío o nulo) y `writable_book` (libro y pluma).

Volúmenes de 0.22 a 0.45. `challenge` va en 0.32. La plantilla tiene 56 efectos en 97 s. No pongas más sonidos que eventos visibles.

### 3.10 Armar

Desde la carpeta del video:

```bash
python ../../../herramientas/build.py
```

Pasos: `script lint render three composite sync mux`. Puedes correr pasos sueltos, por ejemplo `python ../../../herramientas/build.py script lint render Scene4_Idea sync Scene4_Idea mux`.

Si el linter falla, el tiempo de alguna línea se pasa de su presupuesto. Corrige los `until` y los `rt`, no la narración.

### 3.11 Verificar (obligatorio antes de entregar)

1. **Duración:** `build.py` imprime la duración del video y la del audio, y deben coincidir.
2. **Cuadros:**
   - Haz hojas de cuadros de cada escena:
     ```bash
     python ../../../herramientas/sheet.py hoja.png 3 --video video.mp4 1,5,12,...
     ```
   - Mira cada imagen y busca textos encimados, letras tapadas, cosas cortadas en los bordes y código tapado por el 3D.
3. **3D en cuadros sueltos:** prueba la parte 3D antes del clip completo:
   ```bash
   node ../../../herramientas/three/render.mjs --page three/mundo.html --tema ../../../herramientas/temas/minecraft-original --stills 2,40,60 --outdir review3d
   ```
4. **Errores conocidos:** recorre la lista "Errores ya cometidos (no repetir)" de `GUIA.md` contra tus hojas de cuadros: varillas encima de bloques, pixel art pintado de un color, íconos 3D tapados, comas, números encima de íconos, avisos tapando el 3D y contenido 3D fuera del cuadro.
5. **Loop:** la diferencia media entre el primer y el último cuadro debe ser menor a 1. Si queda un poco arriba, revisa el mapa de diferencias: si solo hay bordes, es ruido de compresión.
6. **Visor:** ábrelo con `video_viewer.py video.mp4 --order concat.txt --script script.py --port 80NN`.
7. **Reporte:** di qué verificaste y qué no. Por ejemplo, si no viste el video en movimiento, dilo.

Al terminar:

- Agrega el video a la lista "Videos hechos" de `GUIA.md`.
- Agrega una entrada con fecha a `BITACORA.md`.

## 4. Reglas que no se rompen

- **No subas archivos del juego** a ningún repositorio: `tex/`, `gui/`, `font/`, `sounds/`, `mundos/tex/`, ni las renders que los contienen. Ya están en `.gitignore`; no los saques de ahí.
- **Al publicar:**
  - Sin el logo de Minecraft.
  - Si el video lleva música del juego, avisar antes de publicar: las canciones de C418 reciben reclamos de derechos de autor en YouTube.
  - En la descripción, "Not an official Minecraft product".
- **Código:** en inglés, con comentarios breves. Los `.md` del proyecto van en español.
- **Commits:** sin firmas de IA ni `Co-Authored-By`.
- **Cambios fuera de la carpeta del video:** no cambies las herramientas compartidas (`prelude.py`, `build.py`, `tema.py`, `mc.js`) para un solo video. Si hace falta, agrega un ayudante nuevo sin romper los videos anteriores y anótalo en `GUIA.md`.
- **Archivos con barras invertidas** (TeX, `\n` dentro de cadenas de Python): escríbelos con la herramienta de archivos, no con heredocs de Bash.
