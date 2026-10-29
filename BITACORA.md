# Bitácora de LeetSolve

Registro de lo que se hizo en cada sesión, de la más reciente a la más antigua. El cómo trabajar está en `GUIA.md`.

## 2026-10-29 (PC de Windows): los temas de la laptop, con voz y render

- Aldo trabajó en la laptop los shorts de paquetes, SQL, servidor y Kafka (y un borrador de streaming) y pidió traerlos con `git pull` y terminarlos como DNS y HTTPS. Streaming sigue como borrador sin aprobar: no se tocó.
- En esta PC: `extraer.py 26.3` (assets nuevos) y las texturas de los lugares nuevos con `mundo.py`'s `block_textures` (`mundos/tex/` está en `.gitignore`, así que cada PC las genera).
- **Arreglo compartido:** `loadMobs` de `vida.js` fallaba con una textura sin modelo en `vida.js` (el gólem del servidor). Ahora la carga igual.
- **Paquetes: terminado.** Voz clonada (23 líneas, 105.9 s), toma del TTL abierta para que la vagoneta no quede pegada abajo, render con 37 efectos, loop con diferencia 0.66. `How Packets Work.mp4` en la carpeta y en `export/`.
- **SQL:** cuadros revisados y corregidos (la consulta flota sobre la pared y no tapa la tabla, la cámara de la tabla sube, la toma del pago se abre y los cofres se acercan, en la bóveda la consulta va sobre el techo y el formulario se quita cuando se abren los cofres). Voz lista (21 líneas, 115.1 s; Whisper sin problemas). `three/timestamps.json` provisional ya borrado. **Terminado:** render con 45 efectos, 115.1 s, loop con diferencia 0.98. `How SQL Works.mp4` en la carpeta y en `export/`, con su bloque en `export/descripciones-tecnologia.md`.
- **Servidor:** cuadros revisados y corregidos (la portada ahora está al centro y baja al suelo como en paquetes, la toma de la nota ya no queda tapada por la cabeza de Steve, la respuesta se ve desde arriba, los códigos de estado salen de uno en uno, la leyenda de los verbos sube sobre la tabla). Falta: la voz (se estaba generando al cerrar), borrar `three/timestamps.json`, revisar los cuadros con la voz real y el render.
- **Kafka:** página `three/kafka.html` escrita completa en esta sesión con el diseño aprobado. Lugar `mac-09` renombrado a `birch-creek` y anotado en `lugares.json`. Cuadros revisados con un `three/timestamps.json` provisional y corregidos (tomas aéreas más cerca, globos que se enciman). Falta: la voz, borrar el provisional, revisar con la voz real y el render.
- La voz del servidor y de Kafka se quedó generándose en segundo plano: `tts_qwen_clone.py` reanuda desde `.tts-cache/`, así que si se cortó, basta con volver a correrlo en cada carpeta.
- **Descripciones:** `export/descripciones-tecnologia.md` (como `descripciones-arboles.md`, local) con título y descripción para YouTube de DNS, HTTPS y paquetes. Faltan las de SQL, servidor y Kafka al terminar cada uno. Los `descripcion.txt` de cada carpeta ya estaban.

## 2026-10-28 (laptop): short del servidor (Request → Response y REST), solo el código

- Segundo short de backend, pedido por Aldo después del de SQL. Diseño aprobado en `videos/tech/server/DISENO.md`: el servidor es un taller; la petición, una nota que viaja por tolvas (router → middleware con el aldeano de la etiqueta y el gólem → handler → base de datos → libro con JSON y sello `200 OK`). Luego REST: recursos, cuatro verbos sobre la tabla de SQL, códigos de estado y "sin estado" con diez talleres iguales.
- Hecho: `narration.txt` (21 líneas, ~115 s), `video.json`, `descripcion.txt` (97 caracteres) y `three/server.html` (mismo lugar y misma sala que SQL). `extraer.py` copia ahora la tolva, el horno, el fuego, el gólem de hierro y sus sonidos (se corrió en la laptop). Verificado: `node --check`. **No verificado:** nada renderizado.
- Correcciones en `sql.html`: la pared del fondo sube a 6 bloques (el letrero `players` quedaba en el aire) y la vagoneta se coloca antes que la cámara (la toma que la sigue leía la posición del cuadro anterior, y un cuadro suelto salía mal).

## 2026-10-28 (laptop): short de SQL, solo el código

- Aldo pidió explicar el **backend** sin enfocarse en redes, con SQL como ejemplo, y eligió **un solo short** ("How SQL works") con la forma del de DNS: cómo funciona (tabla, consulta y orden real de ejecución) y tres usos (índice, transacción e inyección SQL). Diseño aprobado en `videos/tech/sql/DISENO.md`.
- Metáfora: la tabla es un estante de letreros en una sala de piedra; la consulta, globos que lee el bibliotecario; el índice, un árbol de rieles hasta una pared de un millón de cajones; la transacción, un pago de esmeraldas que un creeper interrumpe; la inyección, el texto del ilusionista pegado en la consulta que abre todos los cofres.
- Hecho: `narration.txt` (21 líneas, ~125 s), `video.json`, `descripcion.txt` (91 caracteres) y `three/sql.html`. Verificado: `node --check`, la lógica del índice en Node y el resultado de la consulta en Python. **No verificado:** nada se ha visto renderizado; las cámaras están calculadas a mano.
- Aldo pidió **no renderizar todavía**: la voz se detuvo después de la primera línea (queda en `.tts-cache/`). `three/timestamps.json` es provisional y se borra antes del render final. Pasos que faltan al final de `DISENO.md`.
- Usa `rieles.js` y `entityPart`/`skinMat` de `gente.js`, de la sesión de paquetes (sin commit todavía). `lugares.json` no se tocó: el lugar (`mac-02` de prueba) se anota al elegirlo.

## 2026-10-28 (laptop): short de paquetes, solo el código

- Tercer short de la línea de tecnología (`videos/tech/`), después de DNS y HTTPS. Aldo eligió **paquetes** entre varios temas de redes (puertos y NAT, TCP contra UDP, VPN) y pidió hacerlo igual que DNS, pero **primero el código; la voz y el render en otro momento**.
- Metáfora: la foto es el cuadro `bust` del juego (2 × 2), cada bloque es un paquete en una vagoneta con cofre, los rieles son la red y cada cruce es un router (puesto con cartógrafo y libro de rutas). El paquete 2 va por el camino largo y espera en fila, el 3 se tira en un router lleno, Alex los ordena por número y pide el 3 otra vez (TCP). Después, el TTL (una vagoneta atrapada en un lazo) y el ping. Diseño en `videos/tech/packets/DISENO.md`; estado y pasos en `PLAN.md`.
- Nuevo en el tema: `rieles.js` (rieles, vagoneta del juego, estación y avance por llaves), `entityPart` y `skinMat` exportados en `gente.js` (la textura puede ser de 64 × 32) y assets nuevos en `extraer.py` (rieles, vagoneta, cuadro, sonidos de vagoneta, `fizz`, cuadro, marco y campana).
- Lugar: `mac-13` renombrado a `birch-terraces` y anotado en `lugares.json`.
- Hecho: `narration.txt` (23 líneas, ~118 s), `video.json`, `descripcion.txt` (93 caracteres) y `three/packets.html`. Verificado: sintaxis con `node --check` y la lógica de los rieles en Node (largos de las rutas 72 y 92 bloques, giro de las 4 curvas, pasadas del TTL). **No verificado:** nada se ha visto renderizado; en esta laptop falta correr `extraer.py 26.3` y copiar las texturas de `birch-terraces`.
- Siguiente tema que pidió Aldo: cómo funciona el backend, qué es Kafka y cómo funciona. Otra sesión dejó un diseño de "How SQL works" en `videos/tech/sql/DISENO.md`.
- **Continuación, primeros cuadros (otra sesión, misma noche):**
  - Se corrió `extraer.py 26.3` y se copiaron las texturas de `birch-terraces`.
  - Se renderizaron 26 cuadros fijos con un `three/timestamps.json` **provisional** (130.4 s, hay que borrarlo antes del render final).
  - Se corrigieron 5 fallas, detalladas en `PLAN.md`, paso 8:
    - Globos gigantes fuera del cuadro.
    - El globo más ancho que el 9:16.
    - Rieles invisibles en las tomas lejanas.
    - El texto de la portada que no cabía.
    - El letrero de la portada tapando la toma de Steve.
  - Dos de las fallas se corrigieron en herramientas compartidas, así que también benefician a DNS, HTTPS y SQL:
    - `placeUI` de `aldea.js` usa la profundidad, oculta los globos cuya ancla queda muy fuera del cuadro y achica los que no caben.
    - Los rieles de `rieles.js` son recorte opaco.
  - Ambas cosas quedaron anotadas en `GUIA.md`.
  - Verificado con cuadros: loop con diferencia 0.01.
  - Choques de vagonetas, revisados en la lógica de la página. Los paquetes no chocan y llegan en el orden de la narración. El tráfico de las tomas aéreas se atravesaba de frente; ahora va en un solo sentido.
  - Aldo pidió que esta sesión solo haga código: la voz y el render los hace él.
  - Falta: la voz, el render y que Aldo vea los cuadros (`review3d/hoja1.png`, `hoja2.png`, `hoja_rieles.png`).

## 2026-10-28 (PC de Windows)

### Línea nueva: shorts de tecnología, todo en 3D

- Aldo quiere explicar cómo funcionan las tecnologías, no solo ejercicios. Le gustan más las partes 3D que las 2D, así que estos shorts son **100 % 3D** y todo se cuenta con Minecraft. Carpeta `videos/tech/`.
- Prueba de 15 s aprobada ("Se ve muy bien"): `pruebas/dns-3d/`.
- Luz verde total de Aldo para DNS y luego HTTPS/TLS sin supervisión, con commit y push al terminar cada sección.
- Piezas nuevas (ver "Videos solo 3D" en `GUIA.md`):
  - `gente.js`: aldeanos con capas de bioma y oficio, jugadores (Steve, Alex), illagers y el vendedor ambulante. También `moveAlong`.
  - `aldea.js`: construcciones por código, libros de atril, globos tipo tooltip con `placeUI`, objetos que vuelan y `cameraAt`.
  - Modo `"solo3d"` en `build.py` y `--cues` en `render.mjs`. Comprobado que el short 02-dfs sale con el mismo audio (MD5 igual).
  - `extraer.py` copia personajes (`gente/`), bloques, objetos y sonidos nuevos.
- **Voz madura en esta PC:** venv `.venv-tts` con torch de CPU; `tts_qwen_clone.py` tarda unos 4 minutos por línea. Nuevo `pruebas/voces_demo/check_voice.py`: transcribe cada línea con Whisper y la compara con el guion.

### DNS (`videos/tech/dns`)

- Diseño en `DISENO.md` (revisado por un subagente: se corrigió la exactitud de unbound, DNSSEC y CDN). Lugar nuevo `flower-plain`.
- 26 líneas, 155.6 s, 27 efectos, Subwoofer Lullaby. Loop: diferencia media 0.52.
- Voz: ningún silencio de más de 0.45 s; Whisper oye el guion en todas las líneas. En la 19, Whisper no oía el "The" del inicio; con 0.3 s de margen sí estaba (Whisper pierde palabras átonas sin contexto). Aun así se cambió a "Here's the fix: D N S SEC.", que arranca más claro.
- Correcciones en el camino: globos enormes y cortados (ahora tamaño fijo en pantalla y dentro del cuadro), la toma aérea no mostraba toda la aldea (cámara a 78 de altura y nombres flotantes), sendero enterrado, casa tapando la cámara, destello cuadrado, la barra del TTL orientada con la cámara del cuadro anterior y el final bajando de golpe a la portada.

### HTTPS y TLS (`videos/tech/https-tls`)

- Metáfora: certificado = etiqueta de nombre sellada por un clérigo (la CA); intercambio de llaves = mezclar tintes (amarillo público, rojo y azul secretos, los dos llegan a café); después, cofres cerrados con el café. El candado no prueba que el sitio sea honesto ("myb4nk.com").
- Lugar nuevo `south-plain`. 21 líneas, 119.7 s. Voz: sin silencios largos; las líneas 7, 15, 19 y 20 parecían sin la primera palabra para Whisper, pero con margen se oyen completas y el inicio no está recortado (medido en los primeros 120 ms).
- 27 efectos, Subwoofer Lullaby. Loop: diferencia media 0.42.
- Correcciones con la hoja del video: la cabeza de Steve en la portada (ahora empieza detrás de la cámara), la toma inicial lo sigue, cortes directos entre el caldero de Steve y el del banco (la mezcla de cámara pasaba junto al espía) y una toma desde atrás del camino para ver pasar los cofres.

## 2026-10-25 (PC de Windows)

- Aldo aprobó la muestra `shorts/02-dfs`.
- Aldo avisó que la voz falla en algunos videos (falta saber cuáles y qué tipo de falla): revisar la voz con cuidado antes de entregar.
- **Música de fondo obligatoria** en todos los videos y shorts (regla de Aldo), con el OST de Minecraft que ya tenemos copiado del juego (C418, no se descarga nada). Short 02-dfs: Subwoofer Lullaby (la eligió Aldo; aprobado). Largo: Subwoofer Lullaby y luego Mice on Venus (Aldo pidió varias canciones). Cambios en el pipeline: `"pista"` acepta una lista (cruce de 4 s y sin el silencio final de cada canción), `build.py` iguala el volumen de cada canción a Subwoofer Lullaby, y `extraer.py` copia 10 canciones de C418. Solo se corrió `build.py mux`.
- En `export/`: el largo y el short con música, `How Trees Really Work - thumbnail.jpg` (primer cuadro, 1280 × 720) y `descripciones-arboles.md` (título, descripción con capítulos y emojis, y el texto del short en menos de 100 caracteres).
- Errores que Aldo encontró con capturas en el largo (y corregidos también en `corto/`, que comparte el código):
  - En la caída del subárbol del 3, las varas quedaban encima de los bloques (el `VGroup` movido con `.animate` listaba las varas al final).
  - En la recursión, el 10 y el 37 se quedaban sobre el bloque 8 al final (y el 1 y el 6 sobre el 3). Ahora se hunden en el bloque, y cuando esperan a un lado van a 1.2 unidades.
  - Se rehicieron solo `Scene04_Subtree` y `Scene09_Recursion` (`script render composite sync mux` de esas escenas). Revisado con cuadros. Ambos errores van en la lista de `GUIA.md` (1 y 17).
- Subir a Drive: la conexión de Drive no acepta archivos tan grandes (417 MB y 71 MB); Aldo los arrastra a `DevSteve/export`.
- Subido a GitHub en 8519099 (música, las dos correcciones y la documentación).
- `GUIA.md`, sección "Música de fondo" reescrita como guía paso a paso: de dónde salen las canciones (el juego instalado, con `extraer.py`), cómo ponerlas en `video.json`, la lista de las 10 canciones con su duración, qué hace `build.py` y la línea de créditos para la descripción. La lista de revisión ahora pide confirmar que el video lleva música.

## 2026-10-24 (noche, PC de Windows)

### El largo de la guía de árboles, terminado

- La PC de Windows trajo de Google Drive la copia de `tree-basics` (zip de 1.67 GB, íntegro). El código era idéntico al de git (solo cambiaban los finales de línea); se copiaron `largo/media/`, `largo/voiceover.mp3` y las dos `.tts-cache/`.
- `fondo.mp4` (11 499 cuadros) y las escenas 1 a 4 ya compuestas estaban completas. Se corrió `build.py script composite Scene05_DFS … Scene11_Outro sync mux` (sin `lint`, como dice `PARA_AGY.md`).
- En Windows faltaban los sonidos `shear` y `lead_tie`: `extraer.py 26.3` (la misma versión de la Mac). También faltaban 20 texturas de lugares de MacEntorno en `mundos/tex/`: se copiaron del jar con el comando de "Problemas conocidos".
- Resultado: 383.3 s (audio 383.291 s), 151 efectos. Hojas de cuadros revisadas en 16:9 (con un script propio de 640 × 360; `sheet.py` hace mosaicos verticales).
- Corrección de Aldo: en la escena del árbol de búsqueda, "balanced: O(log n)" y "staircase: O(n)" no tenían caja y un mob pasaba detrás del "O(n)". Nuevo ayudante `boxed(row)` en `largo/scenes.py` (la misma caja de `entry`); se rehízo solo `Scene07_BST`.
- El número de nivel "2" de la anatomía parecía tapado en la hoja reducida, pero en tamaño completo se lee: no se cambió (habría que renderizar todo el 3D).
- Loop: diferencia media 1.86 entre el primer y el último cuadro; el mapa muestra solo bordes (compresión), dos ovejas un cuadro adelante y el pulso del splash. La portada es la misma.
- Exportado como `How Trees Really Work.mp4` en `largo/` y en `export/`. El `.gitignore` ahora ignora los `.mp4` de `tree-basics` (no llevan `#`), `script.py` y `hoja*.png`.
- Falta que Aldo lo vea en movimiento y escuche la mezcla.

### Shorts verticales que llevan al largo (`videos/trees/tree-basics/shorts/`)

- Aldo quiere cortar el largo en varios Shorts 9:16 para enganchar y mandar al video completo. Se compararon tres formas con cuadros reales (recorte directo, cuadro 16:9 en medio con fondo borroso, escenas nuevas en 9:16) y eligió **escenas nuevas en 9:16**: en las otras dos el texto se corta o no se lee en el celular.
- Reglas de Aldo para estos shorts:
  - **Sin voz nueva:** se usa la voz del largo, cortada en el tramo de cada short.
  - **Se cortan a la mitad de la explicación**, justo antes de la revelación.
  - **Al final, todo se oscurece y aparece un letrero de Minecraft** que dice que el video completo está en YouTube. La voz no lo dice.
  - **Una entrada ligera, sin esperar:** la portada aparece desde el cuadro 0 mientras la voz ya está narrando (3 s de portada sola era mucho).
- Los cinco cortes aprobados:
  1. Tijeras: líneas 12 a 18 (~43 s), corta antes de "Every child is the root of its own subtree".
  2. DFS: líneas 20 a 25 (~45 s), corta después del preorden. **Hecho como muestra** (`shorts/02-dfs`).
  3. Por niveles: líneas 29 a 31 (~19 s), termina en "How do we know whose turn it is?". La línea 31 sigue con "With a queue…": hay que cortar el audio a mitad de línea.
  4. Árbol de búsqueda: líneas 35 a 41 (~40 s), corta antes de la escalera.
  5. Recursión y el secreto: líneas 49 a 57 (~50 s), corta después de contar los bloques.
- El `corto/` que ya existía (tráiler de 74 s con voz nueva) queda aparte.
- Cómo se arma un short (ver "Shorts recortados de un video largo" en `GUIA.md`):
  - `shorts/make_short.py FIRST LAST [CARD_S]` escribe `timestamps.json` con las 63 líneas del largo desplazadas (la línea FIRST empieza en 0) más una línea vacía de 3.5 s para el letrero, corta `voiceover.mp3` del largo con `atrim` y copia `walk.json`. Así `at()`, `words_at()` y `walk.json` funcionan sin cambios.
  - `three/mundo.html`: copia de la parte del largo que toca, con el árbol ya armado, cámara para 9:16 (`CAM = {y: 4.25, z: 17.5, lookY: 2.45}`, niebla `[26, 80]`) y un plano negro pegado a la cámara que oscurece todo el cuadro en el letrero (la capa de Manim solo cubre la franja central).
  - `scenes.py`: la escena del tramo y `Scene2_Full` (redibuja el último estado, lo desvanece, cae el letrero `wood_sign` y aparece "How Trees Really Work"). La portada (`intro_cover`) va en la mitad de abajo, debajo del árbol, y se va en "At eight".
- Muestra `02-dfs`: 48.27 s (audio 48.253 s), 21 efectos, linter limpio, hojas revisadas. Falta que Aldo lo vea y lo escuche.
- Errores de la sesión, para no repetir: el linter marca "Check incomplete" si una escena no llama `self.seg()` (la del letrero usa `self.seg(CARD)` con texto vacío); la portada encimada sobre las barreras del 13 (revisar el cuadro 0).

## 2026-10-24

### Guía de árboles en dos formatos (`videos/trees/tree-basics/`), sin terminar

- AGY escribió el guion visual `GUION_VISUAL_ARBOLES.md`. En la revisión:
  - Los datos estaban bien (recorridos y búsqueda verificados a mano).
  - Era demasiado largo para un Short (5 a 7 min).
  - El resumen del #124 estaba mal.
  - El código estaba en español.
  - Faltaba el gancho.
  - Varios objetos eran inventados.
- Aldo pidió dos formatos:
  - Uno **horizontal (16:9) para YouTube**, completo.
  - Uno **vertical (9:16)** como gancho, con partes del largo, que invite a ver el video completo.
- Nuevo en el pipeline:
  - `"formato": "16:9"` en `video.json`: escenas de 1920 × 1080 con cuadro de 16 × 9 (120 px por unidad, igual que el vertical) y el mundo 3D del mismo tamaño. `TOP_Y = 3.95`.
  - `"comun": ["../comun.py"]` pega código compartido antes de `scenes.py`. Lo usan los dos formatos: el árbol, `Tree2D`, `TokenLine`, `words_at` y `orb_num`.
  - `mc.js`: color `MC.pink`.
  - `extraer.py`, objetos reales del juego: `shears`, `lead`, `hopper`, `oak_sapling` y `compass`.
  - `extraer.py`, sonidos: `shear` (trasquilar) y `lead_tie` (rienda).
  - Lugar nuevo `birch-grove` (era `mac-10`, MacEntorno), de día, con ovejas, vacas, gallinas y un lobo.
- **Largo** (`largo/`, 63 líneas, 6:23):
  - Voz generada (sin silencios de más de 0.45 s), linter sin problemas en 11 escenas y escenas de Manim renderizadas.
  - Tres partes en 3D nítido:
    - La anatomía: el árbol de menas se arma y un glosario se llena a la derecha.
    - El DFS: un orbe amarrado con la rienda rodea el árbol y repite los recorridos preorden, inorden y postorden al ritmo de la voz.
    - El árbol de búsqueda: el 6 cae por la tolva y el árbol se vuelve escalera.
  - Para que el árbol resalte sobre el bosque, la niebla se acerca en esas partes.
  - Revisado con hojas de cuadros y corregido: todo estaba chico para 16:9, había etiquetas fuera del cuadro y el subárbol se caía de la pantalla.
- **Corto** (`corto/`, 13 líneas, unos 74 s):
  - Hechos: narración, `video.json`, `scenes.py` y `three/mundo.html` (paseo con mobs).
  - Falta la voz: 8 de sus líneas son iguales a las del largo y ya están en su `.tts-cache` (copiado).
- Las dos `descripcion.txt` están escritas (100 y 97 caracteres).
- **Se detuvo a petición de Aldo**, en la composición. En esta Mac ya están el clip 3D completo (`largo/media/three/fondo.mp4`) y la composición de las escenas 1 a 4. Los siguientes pasos están en `videos/trees/tree-basics/PARA_AGY.md`.

### `descripcion.txt` en todos los videos

- Aldo pidió que todos los videos tengan su descripción. Se escribió `descripcion.txt` en los 18 que no la tenían (#1 a #9, #16 a #19, #60, #102, #124, #297 y #2089), con el mismo formato y el título exacto de LeetCode. Ahora los 22 la tienen.
- Todas miden 100 caracteres o menos (límite de Shorts). A #3, #297 y #2089 se les quitó `#coding` para caber; #17 queda justo en 100.

## 2026-10-23

### Entorno en la Mac (MacBook Air M2, 8 GB)

- Repositorio clonado en `~/Documents/Codigo Abierto/LeetSolve`.
- Minecraft: launcher oficial instalado en `/Applications/Minecraft.app`; Aldo inició sesión y abrió la 26.3. En Mac los archivos del juego están en `~/Library/Application Support/minecraft`.
- `extraer.py` tenía fija la ruta de Windows; ahora elige `%APPDATA%\.minecraft`, `~/Library/Application Support/minecraft` o `~/.minecraft` según el sistema. Se extrajo de la 26.3 (19 texturas de bloques, 12 de interfaz, 13 de mobs, fuente, 31 sonidos y música) y se copiaron del jar las texturas de los 74 bloques de los lugares a `mundos/tex/`.
- `uv` instalado; venv `~/.manim-skill-src/.venv` (Python 3.12, solo Pillow por ahora: falta manim, kokoro y LaTeX para renderizar) y `~/.manim-skill-src/.venv-tts` (Python 3.12, torch 2.14.1 con MPS, `qwen-tts`, `soundfile`). En Mac el venv usa `bin/`, no `Scripts/`.
- Homebrew reparado (permisos de `/opt/homebrew` y `brew update`) e instalado ffmpeg 9.0.2.
- `tts_qwen_clone.py` ahora usa CUDA, MPS (Apple Silicon) o CPU (`pick_device`). Probado en MPS con la voz joven: el modelo `0.6B-Base` carga en ~58 s y genera 7 s de audio en 19.5 s (unos 5 minutos por video de 20 líneas). El aviso de SoX no afecta porque el script pasa un `.wav`.
- Aldo eligió la **voz madura** (`04_madura_sensual.mp3`). `tts_qwen_clone.py` ahora recibe la carpeta del video y la referencia como argumentos.
- Entorno completo para renderizar: manim 0.22, kokoro, TinyTeX, Playwright (Chromium con ANGLE Metal; `render.mjs` elige `metal` en Mac y `d3d11` en Windows) y el repo de la skill en `~/.manim-skill-src`. Todo anotado en `GUIA.md`, "Entorno (Mac con Apple Silicon)".
- Aldo cambió la regla de duración: menos de 3 minutos, sin estirar el video para llenarlos. Ya no aplica el rango de 85 a 105 s.

### #3644 Maximum K to Sort a Permutation (Medium), problema diario

- Carpeta `videos/bit-manipulation/3644-max-k-sort-permutation` (sección nueva). 112.9 s (video 112.87, audio 112.85), 21 líneas, 61 efectos, 9:16.
- Solución: el AND de los valores fuera de su lugar (0 si ya está ordenado). Se comprobó contra fuerza bruta (unión de valores con `a & b == k`) en todas las permutaciones de hasta 7 y en 3000 al azar de hasta 40. Ejemplo `[0, 3, 2, 5, 4, 1, 6]` → 1; la fuerza bruta prueba k = 6..1 antes de encontrarlo.
- Metáfora: cada bit es una lámpara de redstone (texturas nuevas en `extraer.py`). Un panel de 3 lámparas grandes, en lugar del cofre, guarda el AND; las lámparas del bloque mal colocado vuelan al panel y este pasa de 111 a 011 y a 001.
- Voz madura clonada en MPS: 397 s para 21 líneas, sin reintentos y sin silencios de más de 0.45 s.
- Lugar nuevo `forest-edge`, al atardecer, con lobos, ovejas, vacas y gallinas.
- `scenes.py` ancla los `until` a frases con `ph(línea, "frase")` (anotado en `INSTRUCCIONES_IA.md`).
- Correcciones en la revisión:
  - El `return 1` iba en y = 4.3, encima de la fila 3D: ahora reemplaza la lectura del panel.
  - `k` y `checks` de la fuerza bruta no se leían sobre los abedules: ahora tienen caja de chat.
  - "n values of k / n^2 pairs each" era muy chico.
  - "already sorted -> 0" duraba medio segundo y la pantalla quedaba vacía 2 s antes de la portada.
  - El linter había reescrito los sonidos de las escenas no renderizadas (61 → 55); anotado en "Problemas conocidos".
- Verificado: linter sin problemas, duración igual al audio, cuadros sueltos del 3D, hojas de cuadros de todas las escenas, loop con diferencia media de 1.17.
- No verificado: ver el video completo en movimiento ni escuchar los volúmenes y la pronunciación de la voz.
- Copiado a `export/Maximum K to Sort a Permutation #3644.mp4`. A petición de Aldo, el `video.mp4` de la carpeta se renombró igual: los videos finales nunca se quedan como `video.mp4` (regla nueva en `GUIA.md`).

### #3942 Minimum Operations to Sort a Permutation (Medium), diario del 22 de octubre

- Carpeta `videos/arrays-hashing/3942-min-ops-sort-permutation`. 120.3 s (video 120.30, audio 120.29), 20 líneas, 52 efectos.
- El plan de AGY (`DIARIOS_2_SEMANAS.tex`) usaba dos ejemplos distintos para este problema; se dejó uno solo, `[1, 2, 3, 4, 5, 0]` → 3, que muestra el truco (rotar 5 veces pierde contra invertir, rotar e invertir). El código corto del video se comprobó contra BFS en todas las permutaciones de hasta 7.
- Lugar nuevo `west-hills` (−130, 70, 30), con el lote alargado hasta la cámara para que no se vea la pared de tierra.
- Correcciones en la revisión: la palanca se veía como un palito; primero se armó a mano y Aldo pidió usar la del juego, así que ahora se dibuja el modelo real (`model_icon("lever")`, y `lever_on` al jalarla; ver `GUIA.md`), los letreros tapaban los índices (sin poste y en el pasto; índices encima de los bloques), los bloques se amontonaban al invertir (cruzan por delante y por detrás) y "forwards" tocaba el círculo.
- Verificado: linter, duración igual al audio, cuadros sueltos del 3D, hojas de cuadros de todas las escenas, loop 1.01. No verificado: verlo en movimiento ni escucharlo.
- `Minimum Operations to Sort a Permutation #3942.mp4` en su carpeta y en `export/`, con `descripcion.txt`.

### #2409 Count Days Spent Together (Easy), diario del 24 de octubre

- En LeetCode el diario cambia a la medianoche UTC (18:00 en CST); a las 18:52 ya era el del 24.
- Carpeta `videos/math/2409-count-days-together`. 101.2 s (video = audio), 20 líneas, 39 efectos.
- Solución comprobada contra un recorrido de los 365 días en 20 000 rangos al azar; los ejemplos de LeetCode dan 3 y 0. Ejemplo propio que cruza de mes (Alice 10-28 → 11-03, Bob 10-30 → 11-05 → 5).
- Lugar nuevo `tall-meadow` (−110, 69, −110), del zip. Textura nueva `clock` en `extraer.py`.
- Correcciones en la revisión: la fila se salía por los lados (bloques más chicos y cámara más atrás), "OCT"/"NOV" y el letrero se tapaban, los días del año chocaban con el conteo, el código salía muy chico (nombres de parámetros cortos) y había un segundo vacío antes de la portada final (el mensaje ahora se cruza con la portada).
- Verificado: linter, duración, cuadros sueltos del 3D, hojas de cuadros, loop 1.64. No verificado: verlo en movimiento ni escucharlo.

### Narración sin fechas, y los tres videos otra vez

- Aldo pidió que los videos no digan "today", "yesterday" ni "last week", como los primeros. Se cambiaron la primera y la última línea de #3644, #3942 y #2409 (por ejemplo "…with only two levers." y "That's the big lesson of this problem."). Regla en `INSTRUCCIONES_IA.md` 3.3.
- Se regeneró la voz solo de esas líneas (caché) y se rehicieron los tres, en fila y uno a la vez, con un script que borra el `video.mp4` anterior y se detiene si el build falla (la primera vez tomó por bueno un video viejo del #2409 cuando falló el linter).
- Duraciones nuevas: #3644 112.8 s, #3942 116.5 s, #2409 101.2 s; los tres con video = audio. Loops: 1.23, 1.03 y 1.64.

### #3886 Sum of Sortable Integers (Hard), diario del 20 de octubre

- Carpeta `videos/arrays-hashing/3886-sum-of-sortable-integers`. 129.8 s (video = audio), 20 líneas, 39 efectos, loop 1.16.
- El ejemplo de AGY solo tenía un k válido; con fuerza bruta se vio que con 6 valores distintos nunca sirven dos k, así que se usó `[1, 2, 3, 3, 4, 3]` → 5. El código corto se comprobó contra todos los arreglos de hasta 7 con valores 1 a 3.
- Lugar `east-meadow` (−54, 76, 34), el último bueno del mundo del zip.
- Correcciones: la fila con k = 1 tocaba las orillas, el código salía muy chico (líneas más cortas) y el veredicto y la suma del 3D no se leían (más grandes).

### Lugares: mundo nuevo MacEntorno

- El mundo del zip ya no tenía lugares buenos (20 usados). Aldo creó en la Mac un mundo nuevo, **MacEntorno** (26.3, otra semilla, 971 chunks, unos 512 × 512 bloques), en `~/Library/Application Support/minecraft/saves/MacEntorno`. ClaudeEntorno quedó intacto en `saves` y en el zip.
- El escáner de heightmaps encontró 16 candidatos en MacEntorno. Los lugares de ahí llevan `"mundo": "MacEntorno"` en `lugares.json`.
- Biomas: casi todo playa, bosque de abedules, mar y río (se pintan bien con el tinte de llanura de `mundo.py`). Se descartaron 2 de bosque oscuro (pasto más oscuro, saldría mal pintado) y 3 playas repetidas. Quedan exportados `birch-flowers` (ya asignado al #2089) y `mac-01`, `mac-02`, `mac-03`, `mac-05`, `mac-07`, `mac-09`, `mac-10`, `mac-11`, `mac-12`, `mac-13` para los siguientes videos (ver "Lugares del mundo" en `GUIA.md`). Varios son costa parecida: variar la hora y los mobs.

### #2089 Find Target Indices After Sorting Array (Easy), diario del 19 de octubre: listo para renderizar

- Carpeta `videos/binary-search/2089-find-target-indices`. `[5, 2, 1, 2, 3, 2]`, target 2 → `[1, 2, 3]` contando menores (`less`) e iguales (`equal`), sin ordenar. Comprobado en 20 000 casos al azar.
- Hechos: narración (99.5 s, voz madura generada), `make_walk.py`, `video.json`, `scenes.py` (linter sin problemas) y `three/mundo.html` revisado con cuadros sueltos. Lugar `birch-flowers` (MacEntorno), de día.
- El 3D se rehizo: las pilas de bloques detrás de la fila se salían del cuadro y se perdían entre los árboles; ahora los bloques contados suben en su lugar con marco aqua (menores) o dorado (iguales) y al final bajan al frente en orden.
- Errores de la sesión, para no repetir: indexar listas sacadas de grupos de la escena rompe el linter (error #12; se usa `take(lista, índices)`), y un ayudante llamado `pick` chocaba con la variable local `pick` (el pico): el linter no lo ve y el render real fallaría. El `sed` de macOS no entiende `\b`: para reemplazos con límites de palabra usar Python.
- **Falta:** el render (se detuvo a petición de Aldo para cerrar la sesión). Retomar con `python ../../../herramientas/build.py script lint render three composite sync mux` desde la carpeta, renombrar a `Find Target Indices After Sorting Array #2089.mp4`, copiar a `export/` y revisar con hojas de cuadros (su `descripcion.txt` ya está escrita).

### Reglas nuevas de Aldo

- Los videos finales se llaman `<Título> #<número>.mp4`, nunca `video.mp4`.
- Cada video lleva `descripcion.txt` (100 caracteres o menos, se sube a git).
- Un render a la vez en la Mac (ni dos `build.py` ni voz y render juntos).
- Sin fechas relativas en la narración.
- Objetos del juego con sus assets reales (`model_icon` para modelos como la palanca), nunca inventados.

## 2026-10-22

### Investigación y pruebas de voz más humana (Qwen3-TTS / Chatterbox)

- Aldo pidió buscar un TTS con IA que suene humano para reemplazar o complementar `af_heart` de Kokoro-82M (que lee plano línea por línea y corre en CPU).
- Se revisaron las opciones actuales que caben en la RTX 3060 Laptop (6 GB VRAM):
  - **Chatterbox TTS (Resemble AI, 350M/500M):** clonación zero-shot con 5–15 s de referencia y control de expresividad (`exaggeration`, `cfg_weight`).
  - **Qwen3-TTS (`1.7B-VoiceDesign` y `0.6B/1.7B-Base`):** permite diseñar una voz desde cero con descripción en texto (`VoiceDesign`) y luego fijar esa muestra de ~10 s con el modelo `Base` (o con Chatterbox) para mantener el mismo timbre en todas las líneas de `narration.txt`.
- Se detectó que `~/.manim-skill-src/.venv` tenía `torch 2.14.1+cpu`. Se creó un entorno separado `~/.manim-skill-src/.venv-tts` (Python 3.12) con PyTorch CUDA 12.6 y `qwen-tts` para no tocar el venv de Manim.
- Aldo eligió crear una voz femenina desde cero y pidió una demo con 4 perfiles en `pruebas/voces_demo/` leyendo el gancho y el truco de Two Sum:
  - `01_joven_youtuber.mp3` (11.8 s): joven, enérgica, estilo YouTuber/gamer.
  - `02_calida_storyteller.mp3` (15.3 s): cálida, suave, estilo storytelling.
  - `03_clara_directa.mp3` (10.6 s): clara, rápida y directa.
  - `04_madura_sensual.mp3` (17.6 s): mujer madura con voz profunda, aterciopelada y sensual.
- Scripts de prueba en `pruebas/voces_demo/gen_demos.py` (local con CUDA), `pruebas/voces_demo/gen_demos_fast.py` y `pruebas/voces_demo/tts_qwen_clone.py` (clonación local en la RTX 3060 con `Qwen/Qwen3-TTS-12Hz-0.6B-Base`).
- Prueba completa en el ejercicio #4 (Median of Two Sorted Arrays, 19 líneas, 62 efectos de sonido) con las dos voces finalistas:
  - `pruebas/0004-joven-youtuber` (copiado a `pruebas/voces_demo/0004_joven_youtuber.mp4`): 93.12 s (video = audio), linter sin errores.
  - `pruebas/0004-madura-sensual` (copiado a `pruebas/voces_demo/0004_madura_sensual.mp4`): inicialmente salió de 123.68 s porque el audio de referencia tenía pausas largas (~1 s) y el modelo metió un silencio de 5.75 s en la línea 2; se corrigió con `silenceremove` a máx. 0.22 s por pausa (`fix_madura_silences.py` y `tts_qwen_clone.py`), quedando en **103.73 s** (video = audio) sin silencios muertos y linter sin errores.
- Pendiente: que Aldo vea los dos videos del #4 y elija cuál voz se queda para integrarla en `tts-generate.py`.

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

- **Música en los videos ya hechos:** con la regla nueva, a los videos sin música (#1 a #9, #16 a #19, #60, #102, #124, #2089, #3644, #3942, #2409, #3886 y los de la rama `laptop-videos`) hay que agregarles `"musica"` y correr `build.py mux`. Preguntar a Aldo qué canción lleva cada uno.

- **Guía de árboles (`videos/trees/tree-basics/`):** el largo está terminado (falta que Aldo lo vea y lo escuche). Siguiente: que Aldo apruebe la muestra `shorts/02-dfs` y hacer los otros 4 shorts (1, 3, 4 y 5). El tráiler `corto/` sigue sin voz. Estado en `videos/trees/tree-basics/PARA_AGY.md`.
- Escribir `descripcion.txt` de cada short (100 caracteres o menos).
- **Nether (siguiente paso, idea de Aldo):** agregar lugares del Nether para tener más variedad en el mundo. `mundo.py` ya conoce la carpeta `dimensions/minecraft/the_nether` (el zip la trae); falta: que `export` lea esa dimensión, las texturas propias (netherrack, basalto, soul sand, lava, hongos, nether wart blocks), el cielo/niebla del Nether en `setTime` (sin sol ni nubes, niebla roja) y mobs del Nether (piglins, hoglins, ghasts, strider) en `vida.js`. La lava y los bloques brillantes necesitan luz propia. Luego buscar lugares con el escáner (sin heightmaps de superficie útiles: hay techo de bedrock, así que hay que buscar el piso por columnas).
- **Videos del plan de AGY que faltan** (uno a la vez): #2089 (listo para renderizar), #1569, #3551, #2916, #2913, #3723, #3727, #2897, #2778, #2333 y #1541. #3863 ya está en la rama `laptop-videos`. El plan con el contenido de cada uno está en `DIARIOS_2_SEMANAS.tex`/`.pdf` (de AGY); revisar con fuerza bruta cada código antes de usarlo y corregir lo que se vio en la revisión (narración, código largo, ejemplos).
- Subir `MacEntorno` comprimido a `mundos/MacEntorno.zip` (sin `players/`) para poder volver a exportar sus lugares en otra PC.
- Ver en movimiento y escuchar #3644, #3942, #2409 y #3886 antes de subirlos.

- Lote #8–#19: revisar los 6 videos (hojas de cuadros, errores conocidos, loop, verlos en movimiento y escuchar los volúmenes). Todos tienen `video.mp4` completo en la laptop.
- Unir la rama `laptop-videos` (#10–#15, #1807, #3863 y su `stash@{0}`) con `main`: 5 conflictos (BITACORA, GUIA, extraer.py, mc.js, mundo.py).
- Subir el ClaudeEntorno de 26.3 al zip (sin `players/` ni `singleplayer_uuid` en `level.dat`) si se quieren volver a exportar los lugares nuevos en otra PC.

- Elegir otro lugar para el #60, que repite la colina en terrazas del #4 (Aldo pidió un lugar por video).
- Si se quieren los mobs iguales en todos, volver a renderizar el 3D de #1 a #7 y #124 con el `makeLife` nuevo (`build.py three composite sync mux`).
- Ver los 9 videos en movimiento.

- Antes de publicar el #297: decidir si se queda Subwoofer Lullaby, por el riesgo de reclamo en YouTube.

- Hacer los siguientes ejercicios en el estilo aprobado, empezando desde la plantilla.
- Si se quiere otro escenario (agua, bosque, montañas), elegir un lugar en ClaudeEntorno u otro mundo y exportarlo con `mundo.py`.
