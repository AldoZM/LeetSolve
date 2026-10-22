# Bitácora de LeetSolve

Registro de lo que se hizo en cada sesión, de la más reciente a la más antigua. El cómo trabajar está en `GUIA.md`.

## 2026-10-21

### Lote #8, #9, #16, #17, #18 y #19 (laptop, con subagentes)

- Aldo pidió seguir desde el #8 con 5 problemas más y uno de linked list Medium a elección. Como #10–#15 ya están en la rama `laptop-videos` (sin unir a `main`), eligió #8, #9, #16, #17 y #18; el de linked list es el #19 Remove Nth Node From End of List. Se trabajó sobre `main`; la unión con `laptop-videos` queda para otra tarea.
- No quedaban lugares libres en `lugares.json`. Se buscaron 6 nuevos en el ClaudeEntorno de la laptop (26.3, más grande que el del zip) con un escáner de heightmaps y bioma, y se eligieron viendo 12 candidatos con la cámara de paseo (detalles en la guía, "Lugares del mundo"). `mundo.py` ahora lee la paleta de 26.3.
- Ejemplos verificados en Python antes de narrar:
  - #8 `"  -042a7"` → -42.
  - #9 12321 → true, invirtiendo solo la mitad.
  - #16 `[-5, 2, 3, 4, 7]`, target 10 → 9. Se buscó un ejemplo con un solo más cercano, sin el target exacto y con movimientos de los dos punteros.
  - #17 "23" → 9 palabras.
  - #18 `[1, 0, -1, 0, -2, 2]`, target 0 → 3 grupos.
  - #19 1→2→3→4→5, n = 2 → 1→2→3→5.
- Narraciones de 18 a 20 líneas y voz de los 6. El #18 duraba 108.3 s y se recortó a 104.5 s.
- El #8 lo empezó el agente principal (`make_walk.py`, `video.json`, `scenes.py`). Aldo pidió repartir el trabajo con subagentes: 4 en paralelo (#8; #9 y #19; #16 y #18; #17), con un documento común de reglas y diseño.
- Una caída de red (`ENOTFOUND`) detuvo a los 4 subagentes antes de terminar:
  - #8, #9, #16 y #17: `video.mp4` completo en la laptop, con la duración del video igual a la del audio (95.2, 91.3, 102.1 y 90.3 s).
  - #18: escenas de Manim renderizadas; falta el resto.
  - #19: escenas y clip 3D renderizados; `sync` se cortó a la mitad.
- Después se terminaron los dos renders que faltaban: #18 con `build.py three composite sync mux` (104.5 s, video = audio) y #19 con `composite sync mux` (84.27 s contra 84.25 s de audio, menos de un cuadro). Los 6 videos del lote quedan con `video.mp4` completo.
- Nueva carpeta `export/` en la raíz con los 17 videos terminados de `main`, nombrados `<Título> #<número>.mp4` para subirlos. No se sube a git (`.gitignore`).
- Nuevo `RENDER.md`: cómo renderizar un video cuyo código ya está listo, cómo retomar un render cortado y el estado de este lote con el comando que le falta a cada video.
- Los `script.py` generados llevan la ruta local con el usuario de la PC: los de este lote no se suben, y el cambio de ruta que el build dejó en el `script.py` del #124 tampoco.
- No verificado en ninguno de los 6: hojas de cuadros, la lista de "Errores ya cometidos", el loop, ver los videos en movimiento y escuchar los volúmenes. Los subagentes no llegaron a escribir sus `NOTAS.md`.

### Render del #1 en la laptop (9:16)

- Se rehizo `arrays-hashing/0001-two-sum` en la laptop desde `main`: 1080×1920 (9:16), 30 fps, 97.2 s (video = audio), 56 efectos de sonido.
- `build.py mux` fallaba con ffmpeg 9 (`Unrecognized option 'filter_complex_script'`, la opción ya no existe desde ffmpeg 8). Ahora el grafo de audio se pasa directo en `-filter_complex`; funciona con versiones viejas y nuevas.
- En la laptop faltaban 6 texturas de bloques de los lugares (`mundos/tex/`). Se copiaron del jar con `mundo.block_textures` sin volver a exportar, porque el ClaudeEntorno de la laptop tiene cambios (pale garden) y exportar cambiaría los `.json` de los lugares.
- README corregido: el formato es 1080×1920 (9:16) y `Three/` también es 9:16 (decía 16:9).
- Verificado: linter sin problemas (20 líneas, 7 escenas), duración igual al audio, hoja de cuadros y un cuadro completo en 9:16, loop con diferencia media de 1.28.
- No verificado: ver el video completo en movimiento ni escuchar los volúmenes.

### Formato 9:16 para Shorts

- Aldo preguntó si los videos estaban en 9:16; estaban en 3:4 (1080×1440). Eligió pasarlos a 9:16.
- Se hizo sin tocar las escenas: el mundo 3D se renderiza a 1080×1920 y las escenas de Manim van centradas encima, a 240 px de arriba.
  - Opción `"formato": "9:16"` en `video.json` (`build.py`).
  - `makeWorld` ensancha la vista para que la franja central quede idéntica; `world.ndcY` para las páginas que usan `unproject`.
- Se comprobó con cuadros sueltos: la franja central del recorrido es idéntica a la de 3:4. En el paseo solo cambia un poco el degradado del cielo.
- Pasaron a 9:16 los 9 videos convertidos y el #297. El #60 no, porque es del otro agente.

### Los 9 videos anteriores al estilo Minecraft, cada uno en su lugar, con mobs y hora del día

- A petición de Aldo, #1 a #7, #102 y #124 se rehicieron en el estilo aprobado. La narración se adaptó a Minecraft, se generó la voz nueva y se hicieron sus escenas y su 3D nuevos.
  - Las versiones neón quedaron como `video_neon.mp4` (fuera de git) y sus fuentes, en el commit `35c573f`.
  - #1 es la plantilla aprobada, con una sola corrección: el valor del inventario pasó a la esquina (error #5 de la guía).
- Duraciones (video = audio en todos): #1 97.2 s, #2 100.5, #3 103.7, #4 103.8, #5 89.2, #6 88.8, #7 94.0, #102 90.2 y #124 98.5.
- Aldo pidió que cada video pasara en un lugar distinto del mundo:
  - Se hizo un mapa de todo ClaudeEntorno y se calificó cada punto (cámara libre, lote plano, algo enfrente). Se eligieron 9 lugares: lago con playa, río ancho, meandro entre colinas, colina en terrazas, bosque de abedules, lomas con arena, loma del sur, bosque de robles y bosque con piedra.
  - La lista está en `mundos/lugares.json`.
  - Nuevo en `makeTerrain`: `clear` quita árboles y plantas donde va la cámara, y `surfaceAt` dice qué bloque hay arriba de cada columna.
  - `mundo.py` ahora tiñe las hojas de abedul (salían grises) y dibuja la hojarasca como una capa plana (salía como cruces blancas).
- Aldo pidió vida en el fondo y eligió "horas variadas, con noche":
  - Nuevo `vida.js`, con modelos de los mobs del juego hechos de cajas con su textura, caminata, horas del día (`day`, `dawn`, `dusk`, `night`, con sol, luna y estrellas) y un planificador de caminos según el terreno.
  - `extraer.py` copia las texturas de los mobs y la luna a `mobs/` (en `.gitignore`).
  - Horas: #1, #3 y #5 de día; #2 y #124 al amanecer; #4 y #6 al atardecer; #7 y #102 de noche, con zombis, esqueletos, creepers y arañas.
  - De noche el recorrido conserva toda su luz.
- Correcciones durante la revisión (todas anotadas en "Errores ya cometidos" de la guía, números 9 a 15):
  - El aviso de logro tapaba encabezados largos.
  - Los bloques atenuados con `set_opacity` se volvían blancos.
  - Una función propia tapaba `level_text` del tema.
  - El linter fallaba al indexar listas vacías.
  - Había textos que no cabían en el cuadro.
  - En el #6 la narración decía "most" y el dibujo mostraba un tercio.
  - Faltaban símbolos en la fuente del juego.
- Verificado:
  - Linter sin problemas en los 9.
  - Duración del video igual a la del audio.
  - Hojas de cuadros de cada video, con sus correcciones.
  - Cuadros sueltos del 3D de cada lugar y del banco de pruebas de los mobs (`mundos/vistas/mobs.html`).
  - Loop: diferencia media de 1.3 a 1.8 entre el primer y el último cuadro. El mapa de diferencias solo muestra bordes (ruido de compresión); el contenido es el mismo.
- No verificado:
  - Ver los videos completos en movimiento y escuchar los volúmenes.
- Otro agente trabajó a la vez en el repositorio (#60 Permutation Sequence):
  - Cambió `makeLife` en `vida.js` para que los mobs salten los escalones. #1 a #7 y #124 se renderizaron antes de ese cambio; #102, después.
  - Su #60 usa la colina en terrazas, que ya era el lugar de #4.

### #60 Permutation Sequence (Hard), segundo video del estilo aprobado

- Carpeta `videos/math/0060-permutation-sequence`, 119.875 s, 20 líneas.
- Metáfora: 4 bloques de mena (`coal`=1, `iron`=2, `gold`=3, `diamond`=4) con letrero de target `k = 9`.
  - Fuerza bruta: generar todas las ramas recursivas por backtracking hasta que el pico se rompe; muestra el crecimiento explosivo de $9! = 362,880$.
  - Truco: sistema factorial. Fijar el primer bloque deja $(n-1)! = 3! = 6$ opciones por grupo. Con $k-1 = 8$, la división $8 // 6 = 1$ salta directamente al segundo bloque (2, hierro) con residuo 2.
  - Recorrido y cofre 3D: cofre centrado al frente en $z = 3.2$; los ítems extraídos saltan en parábola Bézier adentro del cofre abierto mientras su tapa abre y cierra auténticamente, y los bloques van a las casillas del inventario formando "2314".
  - Logro: *Advancement Made! Permutation Sequence solved* con ráfaga de orbes de experiencia multicolores, letrero de chat y código Python sincronizado.
- Correcciones y mejoras aplicadas:
  - **Físicas y comportamiento auténtico de mobs de Minecraft (`vida.js`):**
    - Eliminado el deslizamiento continuo e interpolación flotante. Mobs pisan sobre alturas discretas de vóxeles (`terrain.groundAt`).
    - Al subir un desnivel de 1 bloque, ejecutan un salto parabólico discreto ($\Delta y = 0.52 \cdot \sin(\pi w)$) con pose de salto (patas delanteras extendidas hacia adelante, traseras hacia atrás, cuerpo ligeramente inclinado).
    - Al descender, aplican aceleración de caída por gravedad.
    - Trote cuadrúpedo diagonal alternado auténtico del juego (`cos(s)` para pata delantera izquierda y trasera derecha contra delantera derecha y trasera izquierda).
    - Gallinas con aleteo rápido periódico (`sin(t * 22)`).
    - Ovejas y vacas con ciclo natural de pastoreo (bajada e inclinación de cabeza al suelo).
  - **Splash text ("Minecraft edition!"):**
    - Se reemplazó el updater continuo que acumulaba deriva de rotación por pulsos discretos `animate(rate_func=there_and_back).scale(1.15)` manteniendo el ángulo estrictamente fijo en 18°.
  - **Vista de bloques de inventario:**
    - `iso_block_tall` evita que los cubos se vean achatados o aplastados; números de posición reubicados en la esquina inferior derecha.
- Verificaciones y control de calidad:
  - Linter: 20 subtítulos en 7 escenas sin solapamientos ni desbordes.
  - Sincronización exacta: video `video.mp4` (119.875 s) y audio (119.875 s).
  - Loop continuo: diferencia media de 1.67 entre primer y último cuadro.
  - Hojas de contacto generadas (`sheet_verification_v3.png`, `sheet_mobs.png`) comprobando splash, mobs y trayectoria al cofre.


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

### Video #60 Permutation Sequence (Hard) - Minecraft Original

- Carpeta: `videos/math/0060-permutation-sequence/`
- Algoritmo: Sistema numérico factorial con pop de dígitos en `O(n^2)` para $n=4, k=9 \implies \text{"2314"}$.
- Duración: 119.875 s (20 subtítulos en 7 escenas, 31 efectos de sonido mezclados).
- Mejoras aplicadas según feedback:
  1. **Cubos de inventario desaplastados (`iso_block_tall`)**: Se incrementó la profundidad vertical ($h\_ratio = 0.78$) para coincidir con la proyección isométrica real 16x11 de Minecraft Java, y se reubicó el número indicador a la esquina inferior derecha con escala pequeña (`inv.u * 0.85`), idéntico al HUD del juego.
  2. **Splash pulsante continuo**: En `Scene1_Hook` se implementó un updater continuo con pulso armónico que reproduce la animación de la pantalla de título de Minecraft durante toda la escena inicial.
  3. **Escenario y Vida Ambiental en 3D (`vida.js`)**: Se configuró la ubicación `terraced-hill.json` al amanecer (`dawn`) con iluminación matutina y ciclo de mobs autónomos en bucle cerrado (vacas y ovejas pastando, gallinas y cerdos explorando las terrazas), manteniendo un cierre de loop imperceptible (diferencia de 1.848).

## Pendientes

- Lote #8–#19: revisar los 6 videos (hojas de cuadros, errores conocidos, loop, verlos en movimiento y escuchar los volúmenes). Todos tienen `video.mp4` completo en la laptop.
- Unir la rama `laptop-videos` (#10–#15, #1807, #3863 y su `stash@{0}`) con `main`: 5 conflictos (BITACORA, GUIA, extraer.py, mc.js, mundo.py).
- Subir el ClaudeEntorno de 26.3 al zip (sin `players/` ni `singleplayer_uuid` en `level.dat`) si se quieren volver a exportar los lugares nuevos en otra PC.

- Elegir otro lugar para el #60, que repite la colina en terrazas del #4 (Aldo pidió un lugar por video).
- Si se quieren los mobs iguales en todos, volver a renderizar el 3D de #1 a #7 y #124 con el `makeLife` nuevo (`build.py three composite sync mux`).
- Ver los 9 videos en movimiento.

- Antes de publicar el #297: decidir si se queda Subwoofer Lullaby, por el riesgo de reclamo en YouTube.

- Hacer los siguientes ejercicios en el estilo aprobado, empezando desde la plantilla.
- Si se quiere otro escenario (agua, bosque, montañas), elegir un lugar en ClaudeEntorno u otro mundo y exportarlo con `mundo.py`.
