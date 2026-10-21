# Bitácora de LeetSolve

Registro de lo que se hizo en cada sesión, de la más reciente a la más antigua. El cómo trabajar está en `GUIA.md`.

## 2026-10-21

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

- Hacer los siguientes ejercicios en el estilo aprobado, empezando desde la plantilla.
- Si se quiere otro escenario (agua, bosque, montañas), elegir un lugar en ClaudeEntorno u otro mundo y exportarlo con `mundo.py`.
