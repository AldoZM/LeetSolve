# Diseño: short "How Kafka works", todo en 3D

Estado: borrador para que Aldo lo apruebe (2026-10-28). Nada se construye hasta que lo apruebe.

## Intención

Short de backend de la línea "cómo funcionan las tecnologías" (`videos/tech/`), aparte del de SQL (decisión de Aldo). Explica **qué es Kafka y cómo funciona por dentro**, con las animaciones 3D de Minecraft haciendo el trabajo: que alguien que nunca lo usó entienda qué problema resuelve y cómo está armado solo con ver el mundo. Misma forma que DNS: primero cómo funciona y luego usos reales.

Aldo aprobó la metáfora de la biblioteca y los cuatro usos (🟢, 2026-10-28).

## Metas

- Un short vertical (1080 × 1920, 30 fps) de **hasta 3 minutos**, sin estirarlo para llenarlos. La narración de abajo da unos 135 a 155 s.
- Que se lleven cinco ideas: Kafka está en medio de los programas; los eventos se guardan en orden y **leerlos no los borra**; cada lector lleva su marcapáginas (offset); los topics se parten en particiones (el orden solo vale dentro de una); hay copias en otros servidores.
- Todo dentro del mundo 3D: letreros, libros, globos de tooltip y objetos. Nada de capas 2D encima.

## Fuera del alcance

- Código, comandos o instalación de Kafka. Nada de código en pantalla.
- ZooKeeper o KRaft, compactación de logs, garantías de entrega (`acks`, exactly-once), Kafka Streams y Connect.
- Comparar con RabbitMQ u otras colas por nombre.
- Publicar, hacer commit o push: lo decide Aldo.

## No debe pasar (aunque técnicamente funcione)

- Que la narración diga algo falso o exagerado de Kafka (ver "Exactitud").
- Que parezca una cola que borra al leer: el libro se queda en el estante cuando alguien lo lee, siempre a la vista.
- Que se vea como un video 2D con fondo 3D. La cámara vive en el mundo y sigue la historia.
- Texto ilegible en el celular, cortado en los bordes o tapado por el terreno.
- Logos de marcas reales o el logo de Minecraft. Los nombres en texto sí ("LinkedIn").
- Subir al repositorio archivos del juego (texturas, sonidos, música).

## La metáfora (aprobada)

- **Kafka** es una biblioteca en medio de la aldea. Los **programas** son edificios alrededor: la tienda, el correo, las estadísticas, el almacén.
- Un **evento** ("Steve bought a sword") es un libro escrito (`written_book`) con su número. El **productor** es el que lo deja (el aldeano de la tienda).
- Los libros se ponen **al final** del estante, numerados en orden: 0, 1, 2... **Leer no saca el libro.**
- Un **consumidor** es un lector con un **marcapáginas** (el offset): una flecha brillante sobre el número del libro donde va. Cada programa lleva el suyo y lee a su ritmo.
- Un **topic** es un pasillo con letrero ("purchases"). Una **partición** es un estante del pasillo. Un **clasificador de tolvas** (el sorter del juego) manda cada libro al estante según el nombre del jugador: los de Steve siempre al mismo.
- Un **grupo de consumidores** son varios lectores que se reparten los estantes: uno por estante.
- Cada biblioteca es un servidor, un **broker**. Cada estante tiene **réplicas** en otras bibliotecas; si una se quema, la copia toma su lugar.
- La **retención**: los libros más viejos se queman solos después de un tiempo (por ejemplo 7 días).

## Narración (borrador, en inglés)

Unas 390 palabras: entre 135 s (2.9 palabras por segundo) y 155 s (2.5). El constructor puede ajustar el texto, pero no los hechos, y debe quedar por debajo de 180 s. Una línea por viñeta en `narration.txt`; en ese archivo los números y siglas van como se dicen.

```
0  Every big app is full of tiny news. Someone buys a sword. Someone logs in. Someone clicks.
1  And lots of programs want that news. The shop, the email sender, the stats page.
2  If every program called every other program directly, you'd get this. A tangle nobody can fix.
3  Kafka puts a library in the middle. Programs drop news in, and other programs read it out.
4  Each piece of news is an event, written in a book. A program that writes them is a producer.
5  Books go to the end of a shelf, numbered in order. And here's the twist. Reading a book doesn't remove it.
6  A program that reads is a consumer. Each one keeps a bookmark, called the offset, so it knows where it left off.
7  The email sender is on book five. The stats page is still on book two. Neither one slows the other down.
8  News about one subject goes in a topic. This aisle is the topic called purchases.
9  One shelf would be too slow, so a topic is split into shelves, called partitions.
10 The player's name picks the shelf. All of Steve's books land on the same one, so his purchases stay in order.
11 But order is only promised inside a shelf, not across the whole aisle.
12 To read faster, consumers team up in a group. Each shelf goes to just one reader of the group.
13 Each library is a server, called a broker. Every shelf has copies in other brokers, called replicas.
14 If one library burns down, a copy takes over, and the books are still there.
15 Books don't stay forever, though. After a set time, often seven days, the oldest ones are cleared.
16 So what do people use it for?
17 First, one event, many readers. Steve buys a sword, and the stock, the receipt and the stats all react. The shop doesn't even know they exist.
18 Second, rush hour. On Black Friday, books arrive faster than anyone can read them. The library keeps them, and the readers catch up.
19 Third, a time machine. A brand new program can start at the oldest book on the shelf and read the whole history.
20 Fourth, live tracking. A taxi sends its location every few seconds, and the map on your phone moves right away.
21 Kafka was born at LinkedIn, and now it runs inside most of the world's biggest companies.
22 A library in the middle, books that stay, and a bookmark for every reader.
23 That's Kafka.
```

### Exactitud (revisar antes de generar la voz)

- Cada partición es un registro que solo crece; el **offset** cuenta dentro de cada partición, no en todo el topic. Por eso los números empiezan en 0 en cada estante.
- Leer no borra: los mensajes se quitan por **retención** de tiempo o tamaño. El valor por defecto de Kafka es 7 días (`log.retention.hours = 168`): de ahí "often seven days".
- El offset se guarda **por grupo de consumidores y por partición**. En las líneas 6 y 7, el correo y las estadísticas son dos programas distintos, o sea dos grupos, y cada uno lleva su marcapáginas. No mostrar dos lectores del mismo grupo con marcapáginas distintos en el mismo estante.
- La llave (el nombre del jugador) elige la partición con un hash: misma llave, misma partición. El clasificador de tolvas lo representa. El orden solo se garantiza dentro de una partición (línea 11).
- En un grupo, cada partición la lee **un solo** consumidor del grupo. Un lector puede tener varios estantes; si hay más lectores que estantes, los que sobran esperan. El video muestra 3 estantes y 3 lectores.
- Réplicas: cada partición tiene un líder y seguidores en otros brokers. Si el broker del líder cae, un seguidor al día pasa a líder. La línea 14 no promete "nunca se pierde nada" (depende de la configuración): dice que la copia toma el lugar y los libros siguen ahí.
- Línea 19: un programa nuevo puede empezar en el offset más antiguo **que todavía exista** (lo que la retención no ha borrado). Por eso dice "the oldest book on the shelf" y no "book zero".
- Línea 21: Kafka nació en LinkedIn (2011, después pasó a Apache). Apache dice que más del 80 % de las Fortune 100 lo usan: alcanza para "most of the world's biggest companies".
- Línea 20: las apps de taxi usan Kafka para las ubicaciones en tiempo real. No se nombra ninguna marca.

## Escenas (qué se ve en cada parte)

1. **Gancho (0–2):** la aldea al día. Steve compra una espada en la tienda y aparecen globos de noticias por todos lados ("Steve bought a sword", "Alex logged in"). Los edificios de los programas (tienda, correo, estadísticas, almacén) tiran **riendas** (`lead`) entre todos: una maraña. Línea 2: la maraña se aprieta y se enreda.
2. **La biblioteca en medio (3–7):** las riendas se cortan; aparece la biblioteca "KAFKA" en el centro y cada edificio queda con un solo camino hacia ella. El aldeano de la tienda deja un libro (productor) que vuela al final del estante con el número 6. Los lectores del correo y de las estadísticas están en el estante con sus marcapáginas sobre el 5 y el 2. El correo lee el 5 y el libro **se queda**. Las estadísticas avanzan despacio sin que el correo espere.
3. **Topic y particiones (8–11):** la cámara entra al pasillo con letrero "purchases": 3 estantes (P0, P1, P2). Los libros pasan por el clasificador de tolvas; los de Steve (con su cabeza) caen siempre en P1 y quedan en orden. Línea 11: los números de los tres estantes se ven desfasados (el 3 de P0 se escribió después que el 4 de P2).
4. **Grupo de consumidores (12):** tres bibliotecarios del grupo "stats" se reparten los estantes, uno en cada uno, y leen a la vez.
5. **Brokers y réplicas (13–14):** toma aérea con 3 bibliotecas; cada estante brilla en una (el líder) y tiene copias en las otras dos. Una biblioteca se incendia (fuego del juego); su estante líder pasa a la copia de otra biblioteca, que se enciende.
6. **Retención (15):** los primeros libros del estante se queman con humo (como un objeto que se quema en lava) y el estante sigue creciendo por el otro lado.
7. **Usos (16–20):**
   - Un evento, muchos lectores: Steve compra; el almacén saca la espada del cofre, el correo manda un papel y las estadísticas suben una barra. La tienda no voltea a verlos.
   - Hora pico: muchos aldeanos llegan con libros a la vez; el estante se alarga y los lectores aceleran hasta alcanzar.
   - Máquina del tiempo: llega un aldeano nuevo y pone su marcapáginas en el primer libro que queda; la cámara recorre el estante hacia el final.
   - Rastreo en vivo: una vagoneta (el taxi, `rieles.js`) deja un libro con coordenadas cada pocos segundos; un mapa (`filled_map`) en la mano de Alex mueve su punto.
8. **Cierre (21–23):** toma aérea de la aldea con la biblioteca en medio; regresa a la portada (letrero "HOW KAFKA WORKS") para el loop.

## Cómo se hace

### Decisiones de Aldo

- Short aparte del de SQL, con la forma del de DNS: qué es y cómo funciona por dentro, con animaciones 3D, y luego usos.
- La metáfora de la biblioteca y los cuatro usos (🟢).
- Hasta 3 minutos, sin la prisa de los 90 s (el límite de Shorts es 3:00).
- Mismas reglas que los otros shorts de tecnología: vertical, todo en 3D con Minecraft, voz madura clonada (Qwen3-TTS), música de C418, loop. **Esta sesión solo hace el código; la voz y el render los hace Aldo en otro momento.**

### Decisiones de Claude (Aldo puede cambiarlas)

- La narración de arriba y el ejemplo de la tienda de espadas.
- **Lugar:** `mac-09` (MacEntorno, loma de abedules con arroyo), libre. Al usarlo se renombra con un nombre descriptivo y se anota en `mundos/lugares.json`. De día.
- **Música:** Mice on Venus, para variar entre shorts (no tiene silencios). Si Aldo prefiere, Subwoofer Lullaby.
- 3 particiones, 3 bibliotecas (brokers) y 3 lectores en el grupo: es lo mínimo que muestra cada idea.
- Carpeta: `videos/tech/kafka/`.

### Piezas que hay que construir

1. **Estante con libros numerados:** fila de libros escritos con su número encima, que crece por la derecha, y un **marcapáginas** (flecha brillante) que avanza libro por libro. Que sirva para otros shorts (registros, colas).
2. **Clasificador de tolvas:** tolvas del juego (`hopper`, ya en `extraer.py`) que desvían cada libro al estante según la cabeza del jugador.
3. **Riendas** entre edificios (la textura `lead` ya está en `extraer.py`): curvas que se enredan y se cortan.
4. **Fuego y humo** del juego para la biblioteca que se quema y los libros que caduca la retención (el fuego ya lo copia `extraer.py`, desde el short del servidor).
5. Reutiliza `aldea.js` (`makeLibrary`, `makeHome`, `makeSite`, `bubble`, `makeItem`, `arc`, `placeUI`), `gente.js` (Steve, Alex, bibliotecarios y el aldeano de la tienda), `rieles.js` (la vagoneta del taxi) y el modo `solo3d` de `build.py`.

## Forma de trabajo y revisiones

1. Código de la página `three/kafka.html`, `narration.txt`, `video.json` y `descripcion.txt` (100 caracteres o menos).
2. Revisión sin render final: `node --check` y la lógica en la página (por ejemplo, que ningún libro se encime y que cada marcapáginas apunte a un libro que existe), con un `three/timestamps.json` **provisional** que se borra antes del render final.
3. Lo que hace Aldo después: voz (`tts_qwen_clone.py videos/tech/kafka`, cuidar "Kafka", "offset" y "LinkedIn"), cuadros fijos, render completo, loop y la lista de revisión de `GUIA.md`.
4. Al terminar el código: entrada en `BITACORA.md` y el lugar en `mundos/lugares.json`. Sin commit ni push hasta que Aldo lo pida.

## Restricciones

- Otras sesiones trabajan en LeetSolve al mismo tiempo (servidor, SQL, paquetes). Revisar `git status` antes de editar archivos compartidos (`aldea.js`, `gente.js`, `extraer.py`, `lugares.json`) y no pisar sus cambios.
- Nunca subir archivos de Mojang.
- Entorno de Windows: `export PATH="$HOME/.manim-skill-src/.venv/Scripts:$PATH" PYTHONUTF8=1`; `python`, no `python3`.
- Código en inglés con comentarios breves; documentos en español.
- Al publicar: "Not an official Minecraft product" y los créditos de la música de C418.

## Estado del código (2026-10-28, laptop): a medias, se cortó por el límite de uso

Aprobado por Aldo (🟢). Hecho:

- `narration.txt` (24 líneas, la narración de arriba con números y siglas como se dicen), `video.json` (solo3d, 9:16, Mice on Venus) y `descripcion.txt` (92 caracteres).
- `extraer.py` copia ahora `iron_sword` (la espada de Steve); ya se corrió en la laptop.

Falta:

1. **`three/kafka.html`**, la página completa (no existe todavía). Plan de distribución pensado: los estantes van **a lo largo de z** (el offset 0 al fondo, en z ≈ -15, y crecen hacia la cámara 0.95 por libro), las particiones lado a lado en x = -3, 0 y 3, porque en 9:16 el ancho es poco. La sala no tiene techo; las tolvas del clasificador van al frente (z ≈ 3). Los programas (`makeSite`: SHOP, MAIL, STATS, STOCK) quedan alrededor. Los brokers 2 y 3 (`makeLibrary`) van detrás y solo aparecen en las líneas 13 a 15. La sala y los libros suben en la línea 3 y bajan antes de la portada, para que el loop no se rompa. Reusar `makeHopper` y `modelBox` de `server.html` y el letrero de portada que baja de `packets.html`.
2. Lugar: renombrar `mundos/mac-09.json` (radio 64) y anotarlo en `lugares.json`.
3. Un `three/timestamps.json` provisional, `node --check` y revisar la lógica (libros sin encimarse, marcapáginas sobre libros que existen).
4. Entrada en `BITACORA.md`.

## Estado (2026-10-29, PC de Windows)

- `three/kafka.html` escrita completa. Lugar: `mac-09` renombrado a `birch-creek` y anotado en `lugares.json`.
- Distribución final: la biblioteca (sala abierta sin techo, x ±5, z −17 a 3) sube del suelo en la línea 3 y baja al volver a la portada; 3 estantes a lo largo de z en x = −2.4, 0 y 2.4 (libro o en z = −15.5 + 0.95·o, 19 lugares); clasificador de tolvas al frente; programas (SHOP, MAIL, STATS, STOCK) a los lados en x = ±9; brokers 2 y 3 como copias más chicas detrás (z −26 y −42), solo en las líneas 13 a 15; vía del taxi en x = 7.
- Exactitud cuidada en la página: P1 tiene los libros 0 a 5 desde el inicio, el 6 en la línea 4, el 7 y el 8 de Steve en la línea 10, la retención quita el 0, 1 y 2 en la línea 15; la app nueva de la línea 19 empieza en el 3 (el más viejo que queda). Cada marcapáginas es de un grupo distinto (correo, estadísticas, app nueva) y apunta a un libro que existe.
- Cuadros revisados con un `three/timestamps.json` provisional y corregidos.
- Falta: la voz (se estaba generando al cerrar), revisarla, borrar el provisional, cuadros con la voz real, render, descripciones y "Videos hechos".

## Terminado (2026-10-29, PC de Windows)

- Voz completa (24 líneas, 147.7 s). La línea 20 decía "ourth": el recorte del silencio inicial a -40 dB se comía la "F"; ahora es -50 dB y se generó otra toma. Revisada con `whisper-small.en`.
- `three/timestamps.json` provisional borrado. Globos corregidos: "a tangle" sobre las dos filas, "KAFKA" sobre "news in, news out", "the player name" más alto, "gold: the leader shelf" y "P2: a copy takes over" lejos de las etiquetas de los brokers, "receipt sent" cede a "the shop only writes" y el título de live tracking se va antes de que suba el globo del taxi.
- Render con subtítulos y Mice on Venus. `How Kafka Works.mp4` en la carpeta y en `export/`, con su bloque en `export/descripciones-tecnologia.md`.
