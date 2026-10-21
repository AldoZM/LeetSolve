# Bitácora de LeetSolve

Registro de lo que se hizo en cada sesión, de la más reciente a la más antigua. El cómo trabajar está en `GUIA.md`.

## 2026-10-21

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
