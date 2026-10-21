# Bitácora de LeetSolve

Registro de lo que se hizo en cada sesión, de la más reciente a la más antigua. El cómo trabajar está en `GUIA.md`.

## 2026-10-21

### Video #3863 Minimum Operations to Sort a String (ejercicio diario)

- Ejercicio diario de LeetCode 3863 (Medium).
- Carpeta `videos/strings/3863-min-ops-sort-string`, 112.2 s, voz `af_heart` (Kokoro), 34 efectos de sonido.
- Demostración de algoritmo voraz en O(n) tiempo y O(1) espacio auxiliar (respuestas posibles: 0, -1, 1, 2, 3).
- Ejemplo `"dbca"` con menas: d→diamond, b→lapis, c→coal, a→iron. Caso de 3 operaciones con selección de subarreglos en Three.js (`dbc`→`bcd`, `cda`→`acd`, `bac`→`abc`).
- Corrección en `three/mundo.html`: se eliminó un `return` temprano fuera del recorrido que impedía invocar `world.draw()`, restaurando el cierre continuo del bucle con el recorrido periódico de cámara.
- Verificado:
  - Linter sin incidencias (20 subtítulos en 7 escenas).
  - Duración exacta: video 112.175 s vs audio 112.175 s (diferencia 0.000011 s).
  - Loop verificado: diferencia media de 1.18 entre primer y último cuadro (ruido de compresión H.264 normal, sin salto visual).
  - Hoja de contacto generada en `review_sheet.png`.

### Video #1807 en el pale garden (laptop)

- Entorno instalado en la laptop: skill de Manim en `~/.manim-skill-src` (venv que reusa el Python 3.12 global), registrada en Claude Code; `npm ci` y Chromium de Playwright; `extraer.py` (tomó la 26.1.2, la única versión con jar en esta PC); texturas de `claude.json` reexportadas. El reexport del spawn dio un `claude.json` idéntico al del repositorio.
- Aldo pidió primero un bioma de nieve. ClaudeEntorno no tiene nieve generada, así que se copió el mundo a `%APPDATA%\.minecraft\saves` para abrirlo en 26.3. Aldo encontró ahí el **pale garden** (el bioma gris) y pidió usarlo.
- `mundos/claude_pale.json`: orilla oeste de la meseta del pale garden, centro (128, 141, 470), radio 64.
- Herramientas compartidas, sin cambiar los videos anteriores (plantilla verificada: cuadro 3D idéntico byte a byte):
  - `mundo.py`: formato de bloques de 26.3, tinte de pasto y follaje por bioma (con el bioma en el nombre del archivo), musgo colgante y eyeblossom como plantas, alfombras delgadas, tinte de hojas de abedul y abeto, `half` por defecto de 26.3.
  - `mc.js`: `makeWorld({ sky })`, `makeTerrain({ clear })` y bloques delgados (`h`).
  - `build.py`: el paso `mux` usa `-/filter_complex` con ffmpeg 7 o más nuevo (ffmpeg 9 ya no tiene `-filter_complex_script`).
- Video `videos/strings/1807-evaluate-bracket-pairs`: 94.0 s, 20 líneas, 60 efectos. Código con `split`: `chest = dict(knowledge)`, un paso por corchete.
- Encontrado: los sprites de texto quedaban tapados por el terreno (ver "Problemas conocidos" en `GUIA.md`).
- Verificado: duración del video igual a la del audio (94.0 s), hojas de cuadros de todas las escenas, cuadros 3D sueltos. Unión del loop: diferencia media 1.66, contra 1.02 entre dos cuadros seguidos (el bosque cercano y desenfocado cambia más por cuadro que la pradera). No se vio el video completo en movimiento.
- Aldo aprobó el video ("Quedó") y pidió música de fondo: C418 - Dry Hands (Minecraft Volume Alpha), excepción a la regla de "sin música" por el riesgo de reclamos en YouTube. Nueva clave `musica` en `video.json` y pista en `extraer.py`; mezcla a 0.3, entrada de 1 s y salida de 3 s. No se escuchó el resultado; solo se midieron niveles (sin saturación, pico −5.8 dB).
- Aldo vio los minerales del inventario "aplastados". `iso_block` tenía los lados a 0.5 del ancho y llenaba la casilla. Se agregaron `ISO_SIDE` e `ISO_FILL` en `tema.py` (por defecto igual que antes); el #1807 usa 0.61 y 0.88, como el icono del juego.
- Bug encontrado al rearmar: el paso `lint` sobrescribía los cues de sonido de todas las escenas. Corregido en `build.py`; los 60 efectos del #1807 se regeneraron con renders reales.
- Pendiente: el `ClaudeEntorno.zip` del repositorio es el de 26.2 y no incluye el pale garden. Para regenerar `mundos/tex/` de `claude_pale.json` en otra PC hace falta el mundo actualizado.

### Repositorio y documento para otros modelos

- La carpeta quedó conectada a `github.com/AldoZM/LeetSolve`, encima de sus 2 commits anteriores (el video de árboles en `Three/` se conserva).
- `INSTRUCCIONES_IA.md`: guía paso a paso para que cualquier modelo de IA haga un video con los mismos parámetros que la plantilla aprobada.
- El mundo ClaudeEntorno se sube como `mundos/ClaudeEntorno.zip` (sin `players/`, que guarda el identificador de la cuenta) junto con `mundos/claude.json`. Las texturas y las renders con texturas del juego siguen fuera del repositorio.
- `render.mjs` se copió a `herramientas/three/` para que el proyecto funcione en otra PC (`npm ci` ahí). `build.py` lo usa desde ahí y acepta `MANIM_SKILL_TOOLS`.
- Se quitaron las rutas con el usuario local de `GUIA.md` y de esta bitácora.

### #297 Serialize and Deserialize Binary Tree (Hard), primer video del estilo aprobado

- **Aprobado por Aldo ("Quedó perfecto")**, con la música de fondo incluida.

- Carpeta `videos/trees/0297-serialize-tree`, 104.3 s, 22 líneas.
- Metáfora: "guardar" escribe el árbol en preorden en el inventario del cofre (9 casillas) y los hijos vacíos son barreras (`#`). "Cargar" rompe el árbol y lo reconstruye leyendo las casillas.
- La trampa: sin marcas, tres árboles distintos dan `5,8,2,7`.
- Nuevo en el tema: textura `barrier` y `writable_book`, sonidos de libro y del "no" del aldeano (`extraer.py`).
- Correcciones:
  - Los sprites 3D quedaban tapados por el terreno: se resolvió con `renderOrder` (anotado en la guía).
  - `Indicate` con color pintaba de un solo color el pixel art: se cambió por un pulso de escala.
  - Las comas del texto se veían como puntos: se usó una caja de línea completa por pieza.
- Verificado:
  - Linter sin problemas y duración igual a la del audio.
  - Hojas de cuadros de todas las escenas.
  - Loop: diferencia media de 1.24 entre el primer y el último cuadro. Es ruido de compresión en los bordes; el contenido es el mismo.
- No verificado: ver el video completo en movimiento y escuchar los volúmenes.
- Aldo encontró las varillas encima de los bloques en "The problem" (y pasaba igual en "The trick"): se agregan antes que los bloques.
- Aldo vio los bloques del inventario aplastados: el número encima del ícono isométrico tapaba la cara de arriba. Se movió a la esquina inferior derecha, dentro de la casilla.
- Todas las correcciones quedaron juntas en `GUIA.md`, "Errores ya cometidos (no repetir)", y `INSTRUCCIONES_IA.md` pide revisarlas antes de entregar.
- A petición de Aldo, música de fondo: C418 - Subwoofer Lullaby (`"musica"` en `video.json`, `MUSIC` en `extraer.py`). Riesgo de reclamos en YouTube anotado en la guía.

## 2026-10-20

### Estilo Minecraft aprobado

- Aldo aprobó la prueba `pruebas/0001-two-sum-minecraft-original` ("Quedó perfecto"). Es el estilo y la plantilla para los videos nuevos.
- Recorrido de las versiones:
  1. `pruebas/0001-two-sum-minecraft`: tema con arte propio (texturas generadas por código, fuentes OFL Press Start 2P y VT323), cielo azul plano.
  2. Aldo pidió los assets originales para que se viera más llamativo y "sacado del juego". Nuevo tema `herramientas/temas/minecraft-original`. `extraer.py` copia de su Minecraft Java 26.3 las texturas, la interfaz (cofre, barra de objetos, experiencia, aviso de logro), la fuente `ascii.png` y 23 sonidos.
  3. Se agregaron efectos de sonido: `self.sfx()` en las escenas y mezcla en el paso `mux` de `build.py` (51 a 56 efectos por video).
  4. Aldo no quería el fondo azul y creó el mundo **ClaudeEntorno** (perfil "YouTube DSA" del launcher, Fabric 26.2, en `%APPDATA%\.minecraft-youtube\saves`). `mundo.py` lee el archivo del mundo y reconstruye la pradera del spawn en 3D (radio 64, unos 40 000 bloques visibles).
  5. Modo `"fondo"` en `video.json`: un solo clip 3D de todo el video. Las escenas 2D van sobre el mundo desenfocado (Aldo eligió desenfocado sobre nítido) y la parte 3D va nítida, en un lote aplanado.
- Correcciones en el camino: sangría del código con la fuente del juego, "²" deforme, objetos del inventario pequeños, voz 3 dB más baja al mezclar en estéreo, cofre tapado por el inventario, nube transparentándose detrás del código.
- Verificado: duración del video igual a la del audio (97.2 s), hojas de cuadros de todas las escenas y unión del loop (0.003 % de píxeles distintos). No se vio el video completo en movimiento.
- Cuidados legales: los archivos del juego no se suben a ningún repositorio (`.gitignore` del tema). Sin logo de Minecraft. Al publicar, poner "Not an official Minecraft product". Sin música del juego, por los reclamos de derechos de autor en YouTube.

### Proyecto movido a LeetSolve

- Todo se movió de `~/.manim-skill` a `D:\Codigo Abierto\LeetSolve`, separado en `videos/<sección>/`, `pruebas/` y `herramientas/`. Se verificó el número de archivos y el tamaño de cada carpeta antes de borrar el original.
- `stage.js` pasó de la carpeta de la skill a `herramientas/three/`. `render.mjs` ahora acepta `--lib` y `--tema`.
- Se crearon `GUIA.md`, `CLAUDE.md` y `AGENTS.md`, y un aviso en el `SKILL.md` de la skill para que use LeetSolve.

### Videos en estilo neón

- Hechos: #1 Two Sum, #2 Add Two Numbers, #3 a #7 y los árboles #102 (Medium) y #124 (Hard). Todos verticales, con código a la par, sección 3D y loop.
- Herramientas compartidas: `prelude.py`, `build.py` (render en paralelo con reintento, 3D, composición, sincronía, mezcla) y `sheet.py`.

## Pendientes

- Antes de publicar el #297: decidir si se queda Subwoofer Lullaby, por el riesgo de reclamo en YouTube.

- Hacer los siguientes ejercicios en el estilo aprobado, empezando desde la plantilla.
- Si se quiere otro escenario (agua, bosque, montañas), elegir un lugar en ClaudeEntorno u otro mundo y exportarlo con `mundo.py`.
