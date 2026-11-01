# Diseño: shorts de Docker ("How Docker Works" y "How Teams Really Use Docker"), todo en 3D

Estado: **aprobado por Aldo (2026-10-31)**; Parte 1 terminada el 2026-11-01 (`export/How Docker Works.mp4`); Parte 2 terminada el 2026-11-01 (`export/How Teams Really Use Docker.mp4`, página `videos/tech/docker-teams/three/docker2.html`; cambios en "Parte 2: lo que cambió al construirla", al final). Lo que cambió al construir la Parte 1:
- Lugar: `mac-03`, renombrado `docker-coast` (giro 0, así la escena usa las coordenadas de la exportación). La plataforma de Steve (x −1..13, z −3..5), la isla del servidor (x −38..−29, z −2..5) y el lote de la máquina virtual (x 8..12, z 16..20) se hacen por código.
- El Dockerfile del video tiene 4 pasos: `FROM python:3.12` (cajas gris y azul), `RUN pip install flask` (amarilla), `COPY . .` (verde) y `CMD python app.py` (sin caja). Se quitó `COPY requirements.txt` para que cada paso que agrega archivos tenga su caja.
- La imagen viaja en un bote sin cofre: la pila (a la mitad del tamaño) va encima, así se ve qué se manda.
- Los cuartos de vidrio miden 4 × 4 y 2 de alto, abiertos arriba para ver el puesto, con un bloque de separación entre ellos (3 adelante y 3 atrás).
- La capa propia del contenedor es una lámina azul clara sobre el cuarto.

## Intención

Dos shorts de la línea "cómo funcionan las tecnologías" (`videos/tech/`), con la misma forma que los de Git:

- **Parte 1, `videos/tech/docker/` ("How Docker Works"):** qué hace Docker por dentro. Parte del problema "en mi máquina sí funciona" y explica imagen, capas, Dockerfile, caché, contenedor, aislamiento y por qué un contenedor no es una máquina virtual.
- **Parte 2, `videos/tech/docker-teams/` ("How Teams Really Use Docker"):** cómo se usa en un equipo real. Cubre registry, volúmenes, Docker Compose, redes y puertos, y despliegue con la misma imagen probada.

Los dos van en el mismo lugar y con los mismos personajes, y la Parte 2 empieza donde termina la Parte 1. Todo pasa en el mundo 3D de Minecraft: alguien que nunca usó Docker debe entender qué es una imagen y un contenedor solo con ver el mundo.

Lo que decidió Aldo (2026-10-31):
- Dos shorts, como Git: por dentro y luego uso en equipo.
- Los temas de cada parte, tal como están en "Metas".

Lo demás (metáfora, lugar, música, narración) es propuesta de Claude y está marcado así: **(propuesta)**.

## Metas

- Dos shorts verticales (1080 × 1920, 30 fps) de **hasta 3 minutos cada uno**, sin estirarlos. Los borradores de narración dan unos 120 a 135 s cada uno.
- **Parte 1:** que se lleven seis ideas:
  1. "En mi máquina sí funciona" pasa porque la app no viaja sola: depende de lo que tiene instalado cada máquina.
  2. Una **imagen** es la app empacada con todo lo que necesita, y no cambia una vez construida.
  3. La imagen se arma por **capas**, a partir de los pasos de un **Dockerfile**.
  4. Las capas se **comparten** y se guardan en **caché**: si solo cambias tu código, solo se reconstruye la capa de arriba.
  5. Un **contenedor** es una imagen corriendo, aislada en sus propias paredes. De una imagen salen muchos contenedores iguales.
  6. Un contenedor **no es una máquina virtual**: comparte el kernel de la máquina, por eso arranca rápido y caben muchos.
- **Parte 2:** que se lleven cinco ideas:
  1. Un **registry** (como Docker Hub) guarda y comparte imágenes: `push` sube, `pull` baja y las capas que ya tienes no se vuelven a bajar.
  2. Lo que un contenedor escribe se pierde al borrarlo; los datos van en un **volumen**, fuera del contenedor.
  3. Una app real son varios contenedores, y **Docker Compose** los describe en un archivo y los levanta con un comando.
  4. Compose los pone en una **red privada** donde se encuentran por nombre, y solo entra de fuera lo que pasa por un **puerto publicado**.
  5. En producción la imagen se construye **una vez**, se prueba, se sube al registry y el servidor corre **esa misma**. Volver atrás es correr la imagen anterior.
- Loop en cada short: en la última línea todo vuelve al estado del cuadro 0 detrás de la portada, y los subtítulos se ocultan mientras sube (`"ocultar"`).
- Todo dentro del mundo 3D: letreros, globos de tooltip y objetos, sin capas 2D encima. Los comandos (`docker build`, `docker run`...) aparecen como globos de tooltip cortos.

## Fuera del alcance

- Instalar Docker, Docker Desktop y que en Mac o Windows corre sobre una máquina virtual con Linux.
- Kubernetes y otros orquestadores (se puede nombrar en una frase si hace falta, no se explica).
- Detalles de namespaces y cgroups por nombre: se dice qué hacen, no cómo se llaman.
- Construcciones en varias etapas (multi-stage), `.dockerignore`, `ENTRYPOINT` contra `CMD`, imágenes para varias arquitecturas.
- Seguridad de contenedores (permisos de root, escapes) y manejo de secretos.
- Publicar, hacer commit o push al repo de LeetSolve: lo decide Aldo.

## No debe pasar (aunque técnicamente funcione)

- Que la narración diga algo falso de Docker (ver "Exactitud").
- Que parezca que un contenedor es una máquina virtual o una computadora aparte.
- Que parezca que el contenedor modifica la imagen: la pila de capas nunca cambia después del build.
- El logo de Docker (la ballena), el de Docker Hub o el de Minecraft. "Docker" y "Docker Hub" en texto sí.
- Texto ilegible en el celular, cortado en los bordes o tapado por el terreno. Globos que se enciman y el letrero de la portada cruzando los subtítulos (errores 18 y 19 de `GUIA.md`).
- Animaciones inventadas cuando el juego ya tiene una para eso.
- Subir al repositorio archivos del juego.
- Repetir la metáfora de Git: aquí no hay maquetas ni estandartes.

## La metáfora (propuesta)

**La app** es un **puesto de mercado** de Steve (`shop`): un mostrador con un aldeano que vende y clientes que llegan. Cuando corre bien, los clientes compran y salen partículas de esmeralda. Cuando se rompe, el puesto echa humo, el aldeano niega con la cabeza y nadie compra.

**Lo que la app necesita** son bloques con su globo: `python 3.12` (un bloque azul) y `flask` (una linterna). En la máquina de Steve están. En el servidor hay un `python 3.8` y falta la linterna, y por eso se rompe.

**La imagen** es una **pila de cajas de shulker**, una encima de otra. La caja de shulker es la del juego que guarda todo lo que tiene dentro aunque la rompas y la cargues, igual que una imagen. Cada caja es una capa, con su color y su globo:
- Gris: `debian` (el sistema base).
- Azul: `python 3.12`.
- Amarilla: `flask` (las librerías).
- Verde: `shop code` (tu código).

**El Dockerfile** es un **libro y pluma** abierto junto a la pila, con los pasos: `FROM python:3.12`, `COPY requirements.txt`, `RUN pip install`, `COPY . .`, `CMD`. Cada paso que agrega archivos hace aparecer una caja nueva encima de la anterior. `FROM` trae juntas las dos de abajo, porque la imagen oficial de Python ya trae su base.

**Capas compartidas:** otra imagen de Alex (`blog`) usa la misma base. Sus dos cajas de abajo son las mismas cajas que las de Steve: brillan juntas y una rienda las une, y no hay dos copias.

**Caché:** Steve cambia su código. Solo la caja verde se rompe y se reemplaza; las de abajo brillan con el aviso `cached`.

**El contenedor** es un **cuarto de vidrio** que aparece sobre un piso de piedra. Al correr la imagen (`docker run shop`), el puesto se arma dentro del cuarto y empieza a vender. La pila de cajas se queda afuera, sin cambiar.

**Aislamiento:** cada cuarto tiene sus cosas (sus archivos, sus procesos y su dirección de red). Los aldeanos de un cuarto no ven lo que hay en el de al lado.

**Muchos contenedores:** de la misma pila salen tres cuartos iguales, uno al lado del otro.

**La capa propia del contenedor:** lo que el puesto escribe (un letrero con los pedidos) queda en una tapa delgada de vidrio tintado arriba del cuarto, no en la pila.

**Máquina virtual contra contenedor:**
- La máquina virtual es una **casa completa con sus propios cimientos**: su propia capa de piedra y su propio `kernel`. Se construye lenta, bloque por bloque.
- Los contenedores son **cuartos de vidrio sobre un mismo piso de piedra**, con el globo `kernel` en el piso. Aparecen en un segundo, y caben muchos donde cabía una casa.

**El servidor** es un edificio de piedra al otro lado del agua (`server`). La pila viaja en un **bote con cofre** del juego. Allí aparece un cuarto de vidrio y el puesto vende igual que en casa de Steve.

**En la Parte 2:**
- **El registry** es un **puerto**: un muelle con un almacén de estantes donde se guardan pilas con su nombre y etiqueta (`shop:1.2`), con un aldeano encargado. `docker push` es el bote que lleva la pila al puerto, y `docker pull` es el bote que la lleva a Alex o a un servidor. Las cajas que el destino ya tiene brillan y no se suben al bote.
- **El volumen** es un **barril** afuera del cuarto de vidrio, conectado por una **tolva** del juego. Los pedidos bajan por la tolva al barril. Al borrar el contenedor, el cuarto se rompe y la tapa con los pedidos desaparece, pero el barril se queda. El cuarto nuevo se conecta al mismo barril y los pedidos siguen ahí.
- **Varios contenedores:** tres cuartos de vidrio. Uno es `shop` (el puesto), otro `db` (estantes con libros y cofres) y otro `cache` (un cofre pequeño junto a la puerta).
- **Compose** es un segundo libro y pluma (`compose.yaml`) con los tres nombres. `docker compose up` hace aparecer los tres cuartos al mismo tiempo.
- **La red** es una vía con una vagoneta entre los tres cuartos, dentro de una cerca (se reutiliza `rieles.js`). El letrero `db` en la estación es el nombre con el que `shop` lo encuentra.
- **El puerto** es la única puerta en la cerca, con el globo `8080`. Los clientes de afuera solo entran por ahí; la cerca no deja pasar a nadie a `db`.
- **El pipeline** es una línea de trabajo en el puerto. Un aldeano constructor arma la pila una vez, un gólem de hierro la revisa (`tests ok`) y la deja en el almacén. El servidor la baja tal cual.
- **Volver atrás:** la versión `1.3` rompe el puesto en el servidor, el bote trae la pila `1.2` del almacén y el puesto vuelve a vender.

## Lugar, hora y luz (propuesta)

- Un lugar de playa de MacEntorno, porque los botes y el puerto necesitan agua: `mac-03` (dunas frente al mar) o `mac-11` (mar abierto). Se elige entre los dos con cuadros sueltos; al usarlo, se renombra (por ejemplo `docker-coast`) y se anota en `lugares.json` para los dos shorts.
- Las construcciones se hacen por código encima del terreno, como DNS y Kafka: la casa y el puesto de Steve en la orilla, el piso de los cuartos de vidrio a un lado, el servidor al otro lado del agua y el puerto (en la Parte 2) en la orilla.
- De día, con `makeWorld({ shaders: true })`, como Git.
- Mobs de la zona: calamares en el agua (ya están en `mobs/`), gallinas y vacas en la orilla.
- Música: `haggstrom` (191 s, sin silencios) en la Parte 1 y `clark` (202 s) en la Parte 2, para no repetir las dos que ya usaron todos los shorts de tecnología.

## Animaciones (todas del juego)

- **Puesto que se rompe:** humo (`smoke` del juego), el aldeano niega con la cabeza (`shakeNo` de `objetos.js`) y el sonido `villager_no`.
- **Puesto que vende:** el aldeano asiente, partículas verdes de comercio (`happy_villager`) y el sonido `villager_yes`.
- **Cajas de shulker:** la tapa se abre y se cierra con su modelo, con los sonidos `shulker_box_open` y `shulker_box_close`. Se colocan con el sonido de colocar.
- **Caja reemplazada (caché):** las grietas del bloque (`makeCracks`), la caja cae como objeto y la nueva se coloca.
- **Capas compartidas:** la rienda del juego (`makeLead`) y el brillo, como en Git.
- **Cuarto de vidrio:** los bloques de vidrio se colocan uno a uno con el sonido de vidrio; al borrarlo, se rompen con el sonido `glass_break` y sus partículas.
- **Casa de la máquina virtual:** bloques que se colocan uno a uno, despacio.
- **Bote con cofre:** el modelo del juego, que avanza por el agua con su sonido de remo.
- **Tolva y barril:** los objetos bajan por la tolva como en el juego, y el barril se abre y se cierra con su sonido.
- **Gólem de hierro:** sostiene la pila y la entrega, como cuando el gólem da una flor.
- **Listo o aprobado:** orbes de experiencia y el aviso "Advancement Made!".

Faltan en el tema y se revisan en el jar y en la wiki antes de dibujarlos: caja de shulker (modelo y texturas de colores), bote con cofre, tolva, barril, partículas de humo y de comercio, y los sonidos de shulker, vidrio, bote y aldeano que diga sí.

## Narración, Parte 1 (borrador en inglés)

Unas 300 palabras (entre 115 y 125 s). Una línea por viñeta en `narration.txt`; los comandos se escriben como se dicen.

```
0  Steve's shop app works perfectly on his computer. On the server, it crashes. Sound familiar?
1  "It works on my machine" is one of the oldest problems in programming. Docker fixes it. Here's how.
2  The code didn't change. The machine did. The server has an older Python, and one library is missing.
3  Docker packs the app together with everything it needs to run. That package is called an image.
4  An image is built in layers. At the bottom, a small base system. Then Python. Then the libraries. Then your code.
5  The steps live in a file called a Dockerfile. Each step that adds files makes one more layer.
6  Once it's built, an image never changes. Same image, same files, on any machine.
7  Layers are shared. If Alex's image starts from the same base, it's stored only once.
8  Change your code, and Docker rebuilds only from the change up. The layers below come from the cache.
9  To run an image, Docker starts a container. That's docker run. The app comes to life inside its own walls.
10 Inside, it has its own files, its own processes and its own network address. It can't see into the others.
11 One image can start many containers. Each one is a fresh copy, all exactly the same.
12 The image stays read only. Anything a container writes goes on a thin layer of its own.
13 So is a container just a virtual machine? No. A virtual machine brings a whole operating system, kernel and all.
14 Containers share the kernel of the machine they run on. That's why they start in a second, and dozens fit on one machine.
15 Now Steve ships the image to the server. Docker runs it there, and the shop works exactly like at home.
16 That's the idea. Don't install the app on every machine. Ship the box it already works in.
17 An image built in layers, containers that run it in their own walls, all sharing one machine.
18 That's Docker.
```

## Narración, Parte 2 (borrador en inglés)

Unas 330 palabras (entre 125 y 135 s).

```
0  Steve's image works. But his whole team, and every server, needs that same image. How do they get it?
1  Through a registry, like Docker Hub. Think of it as a harbor where images are stored and shared.
2  docker push sends Steve's image there, with a name and a tag, like shop, version one point two.
3  Anyone on the team runs docker pull and gets the exact same layers. Layers they already have are skipped.
4  Now, a problem. The shop saves its orders inside the container. Steve deletes the container, and the orders are gone.
5  A container's own layer is thrown away with it. Containers are meant to be replaced, not kept.
6  So the data goes in a volume, storage that lives outside the container. The container uses it, but doesn't own it.
7  Delete the container, start a new one, connect the same volume, and every order is still there.
8  Real apps aren't one container. The shop also needs a database and a cache, each in its own container.
9  Starting them one by one gets old fast. With Docker Compose, you describe all of them in one file.
10 Then one command, docker compose up, starts the whole set together.
11 Compose also puts them on a private network. The shop finds the database just by its name, D B.
12 From outside the machine, nothing gets in, unless you publish a port, like eighty eighty. That's the only door.
13 Last step, shipping to production. The team never builds images by hand on the server.
14 When code is merged, a pipeline builds the image once, runs the tests, and pushes it to the registry.
15 The servers pull that exact image and run it. What was tested is exactly what runs.
16 And if the new version breaks? Run the previous tag. The old image is still in the registry.
17 Build once, share through a registry, keep data in volumes, and start everything with Compose.
18 That's how teams really use Docker.
```

## Exactitud (lo que los guiones afirman)

**Parte 1:**
- Una imagen trae el sistema de archivos que la app necesita (sistema base, runtime, librerías y código). Correcto.
- Una imagen es una pila de capas de solo lectura; `RUN`, `COPY` y `ADD` crean capas, y las otras instrucciones solo guardan datos. "Each step that adds files makes one more layer" es correcto.
- `FROM python:3.12` trae las capas de la imagen oficial, que incluyen su propia base. Por eso, en el dibujo, `FROM` trae dos cajas.
- Una imagen no cambia después de construida; se identifica por el hash de su contenido. "Same files, on any machine" es correcto (no se dice "mismo resultado", porque la configuración y el hardware pueden cambiar).
- Las capas iguales se guardan una vez y se comparten entre imágenes. Correcto.
- Caché del build: Docker reutiliza las capas hasta el primer paso que cambió y reconstruye desde ahí. "Rebuilds only from the change up" es correcto. Como `COPY . .` va al final del Dockerfile del video, solo cambia la de arriba.
- Un contenedor tiene su vista propia de archivos, procesos y red (namespaces), y la máquina limita lo que usa (cgroups). "Can't see into the others" se refiere a sus archivos y procesos: en la red de Docker sí se pueden hablar, y eso lo cuenta la Parte 2.
- Cada contenedor agrega una capa propia de escritura encima de la imagen; la imagen no cambia. Correcto.
- Una máquina virtual corre un sistema operativo completo con su kernel; los contenedores comparten el kernel del anfitrión. Correcto en Linux. En Mac y Windows, Docker usa una máquina virtual con Linux por debajo; queda fuera del alcance y la narración no dice lo contrario.
- "Start in a second": un contenedor normalmente arranca en menos de un segundo a unos pocos segundos. Es una simplificación honesta.

**Parte 2:**
- Un registry guarda imágenes por nombre y etiqueta; Docker Hub es el público más conocido. `push` y `pull` mandan solo las capas que faltan. Correcto.
- La capa de escritura se borra con el contenedor (`docker rm`); los volúmenes viven aparte y se pueden conectar a otro contenedor. Correcto.
- Compose describe varios servicios en `compose.yaml` y `docker compose up` los crea y arranca. "Together" es correcto (no se dice "en orden", porque `depends_on` ordena el arranque pero no espera a que el servicio esté listo).
- Compose crea una red para el proyecto, y los servicios se encuentran por su nombre (DNS interno). Correcto.
- Sin `-p` / `ports`, nada de fuera de la máquina llega al contenedor; publicar `8080` abre ese puerto. Correcto.
- Construir una vez, probar y desplegar la misma imagen es la práctica recomendada. "Never builds images by hand on the server" describe lo que hacen los equipos, no una regla de Docker.
- Volver a la etiqueta anterior funciona mientras la imagen siga en el registry y los datos sean compatibles. "The old image is still in the registry" es correcto para el ejemplo.

## Pasos después de aprobar

1. Revisar en el jar y la wiki los assets que faltan (caja de shulker, bote con cofre, tolva, barril, partículas y sonidos) y agregarlos al tema sin romper los videos anteriores.
2. Elegir entre `mac-03` y `mac-11` con cuadros sueltos y fijar dónde van la casa, el piso de los cuartos, el servidor y el puerto.
3. Parte 1: `narration.txt`, `video.json` (`solo3d`, `formato` 9:16, música) y `descripcion.txt`.
4. Parte 1: `three/docker.html` con un `three/timestamps.json` provisional; muestra de unas líneas para que Aldo la apruebe y luego cuadros a la mitad de cada línea.
5. Parte 1: voz clonada (`tts_qwen_clone.py`) y revisión con Whisper. Luego borrar el provisional, correr `palabras.py` y agregar los subtítulos. La voz y el render van uno después del otro, no en paralelo.
6. Parte 1: render, hojas de cuadros al 20, 55 y 90 % de cada línea, loop, `How Docker Works.mp4` en `export/`.
7. Parte 2: los mismos pasos en `videos/tech/docker-teams/` (`three/docker2.html`), con `How Teams Really Use Docker.mp4`.
8. Descripciones en `export/descripciones-tecnologia.md` y entrada en `BITACORA.md`.

## Parte 2: lo que cambió al construirla

- Carpeta `videos/tech/docker-teams/`, mismo lugar (`docker-coast`) y música `clark`.
- **El registry** es un muelle de tablas sobre pilotes en el mar (x −26..−17, z 20..28) con una pared al fondo; las pilas `blog:2.0`, `shop:1.2` y `shop:1.3` van frente a la pared con su letrero. Sin aldeano encargado (no cabía en las tomas).
- **Alex** tiene su máquina más atrás en la playa (z 17), para no tapar las tomas de la plataforma. En el `pull` solo viajan las dos capas que le faltan; las dos que ya tiene aparecen translúcidas, unidas con riendas a las de su imagen `blog`.
- **El volumen** es un barril con una tolva encima, en el hueco entre el cuarto de `shop` y el de `db`. Los pedidos bajan por la tolva; al abrir el barril salen flotando.
- **Compose:** el libro `compose.yaml` en un atril en la arena; `db` (estantes, bibliotecario) y `cache` (lámpara de redstone, cartógrafo) se levantan juntos y el cuarto de `shop` brilla con ellos.
- **La red** son rieles frente a los cuartos con letreros `cache`, `shop` y `db`; la vagoneta con cofre va de `shop` a `db`. La cerca está al frente, con la única puerta en x = 5 (`8080`). Un aldeano de fuera choca con la cerca frente a `db` (barrera) y el cliente entra por la puerta.
- **El pipeline** está al frente del muelle: un albañil arma la pila (caja cyan = versión 1.3), el gólem la revisa (`tests ok`) y la pila pasa a su lugar. Dos botes salen del lado sur del muelle hacia la isla: uno lleva la 1.3 y el otro la 1.2 al volver atrás.
- Caja de shulker cyan y barril agregados a `extraer.py`.

