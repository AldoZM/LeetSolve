# Diseño: short "How DNS works", todo en 3D

Estado: borrador para que Aldo lo apruebe (2026-10-28). Nada se construye hasta que lo apruebe.

## Intención

Es una línea nueva y experimental de LeetSolve: shorts que explican **cómo funcionan las tecnologías**, no ejercicios de LeetCode. El primero es DNS.

Por qué así: a Aldo le gustan más las partes 3D de los videos anteriores que las explicaciones en 2D con Manim. Este short es **100 % 3D**, sin escenas de Manim, y **todo se cuenta con Minecraft**: la metáfora hace entendible el concepto.

Ya existe una prueba de 15 s aprobada por Aldo ("Se ve muy bien"): `pruebas/dns-3d/prueba.html`, con su `prueba.mp4` y su `hoja.png`. Es la referencia visual: el aldeano bibliotecario, Steve, la casa hecha por código, el atril con libro y los globos de texto con el estilo del tooltip del juego. Es código desechable: se puede copiar y mejorar, pero no es la base obligatoria.

## Metas

- Un short vertical (1080 × 1920, 30 fps) de **menos de 3 minutos** que explique qué es DNS y cómo funciona, con 4 aplicaciones reales.
- Todo dentro del mundo 3D: textos en letreros, libros, globos de tooltip y objetos. Nada de capas 2D encima.
- Que alguien sin conocimientos técnicos entienda el recorrido de una consulta solo con ver la aldea.
- Dejar el camino para más shorts de tecnología, con piezas reutilizables (personajes y paso de voz sin Manim).

## Fuera del alcance

- Los tipos de registro (A, MX, CNAME): quedan para otro short si este funciona.
- Escenas de Manim, código en pantalla y subtítulos quemados.
- Publicar, hacer commit o push: lo decide Aldo.

## No debe pasar (aunque técnicamente funcione)

- Que la narración diga algo falso o exagerado de DNS (ver "Exactitud").
- Que se vea como un video 2D con fondo 3D. La cámara vive en el mundo y sigue la historia.
- Texto ilegible en el celular, cortado en los bordes o tapado por el terreno.
- Logos de marcas reales (Google, bancos) o el logo de Minecraft. Los nombres en texto sí ("google.com").
- Subir al repositorio archivos del juego (texturas, sonidos, música).

## Contenido aprobado por Aldo

1. **Cómo funciona** (~65 s): el jugador, los bibliotecarios, las coordenadas y el libro de la caché.
2. **Bloquear anuncios y distracciones** (~25 s): Pi-hole y el control parental juntos.
3. **Suplantación** (~25 s): el impostor, la trampa y el sello que no se puede falsificar.
4. **Quién ve tus preguntas** (~25 s): privacidad, DNS cifrado y unbound juntos.
5. **Mismo nombre, distinto lugar** (~20 s): CDN.

## La metáfora (aprobada)

- Steve es tu computadora. El nombre (google.com) es el lugar al que quiere ir. La IP son las coordenadas.
- El **resolvedor** es el bibliotecario de la biblioteca del proveedor de internet, en la aldea (con un letrero "PROVIDER" o parecido).
- **google.com, el lugar**, es un edificio aparte (no la biblioteca de google): a él camina Steve con la brújula. El cuarto de barreras y el banco falso también son lugares.
- Si no sabe la respuesta, pregunta en orden: el bibliotecario de la **raíz**, luego el de **.com** y luego el de **google.com**, que tiene las coordenadas reales en su atril.
- La **caché** es el libro donde el bibliotecario anota la respuesta. El **TTL** es un reloj junto a la anotación: cuando se acaba, la anotación se borra.

## Narración (borrador, en inglés)

Unas 400 palabras. Kokoro y la voz clonada hablan a ~2.9 palabras por segundo, así que sale en unos 135 s; está bien así, no se estira para llenar 3 minutos (regla de Aldo). El constructor puede ajustar el texto, pero no los hechos, y debe mantener el total por debajo de 180 s. Una línea por viñeta en `narration.txt`.

```
0  Every time you open a website, your computer asks a question you never see.
1  Computers don't find each other by name. They use numbers, like coordinates in a Minecraft world.
2  google.com is a name for people. Your computer needs something like 142.250.190.46.
3  Turning names into numbers is the job of DNS, the Domain Name System. Think of it as the village librarians.
4  Steve wants google.com, so he asks a librarian called the resolver. Usually, your internet provider runs this one.
5  First, the librarian checks his notebook. Nothing there yet, so he starts asking around.
6  He asks the root library. The root doesn't know google, but it knows who runs every dot com.
7  The dot com library doesn't know the address either, but it knows which library belongs to google.
8  And google's own library has the real coordinates, written on its lectern.
9  The answer travels back, and the librarian hands Steve the coordinates.
10 He also writes them in his notebook, with a timer called the TTL.
11 So when Alex asks for google.com a minute later, the answer is instant. No trip at all.
12 When the timer runs out, the note is erased, so old addresses don't stay forever.
13 That simple question and answer powers some clever tricks.
14 First, blocking ads. Ads come from their own names, like ads.tracker.com.
15 A blocker like Pi-hole gives the librarian a blacklist. Ask for an ad, and he sends you to a room of barrier blocks.
16 The ad never loads. The same list can block any site you choose, for kids or for your own focus.
17 Second, the dangerous one: spoofing. A fake librarian jumps in with the wrong coordinates.
18 Your bank's name, but a fake bank, full of TNT.
19 The fix is DNSSEC. Signed names carry an enchanted seal that nobody can forge, so a fake answer gets thrown out.
20 Third, privacy. Normally your questions travel open, and your internet provider can read every one.
21 Encrypted DNS locks each question in a chest. And with your own resolver, like Unbound, you stop using the provider's librarian and ask the source libraries yourself.
22 Last, speed. google.com isn't one place. There are copies of it all over the world.
23 So the librarian points you to the closest copy. That's why it loads fast here and in Tokyo.
24 So every link you click starts with a librarian, a notebook and a few trips around the village.
25 That's DNS.
```

### Exactitud (revisar antes de generar la voz)

- 142.250.190.46 es una IP real de Google; se puede usar.
- Pi-hole contesta por defecto con 0.0.0.0 a los dominios bloqueados: el "cuarto de barreras" representa eso.
- DNSSEC firma los registros y el resolvedor que valida rechaza las respuestas de nombres firmados cuyo sello falta o no es válido: es el "sello encantado" (el brillo de encantamiento del juego). **La mayoría de los nombres no están firmados, google.com tampoco**: en el acto 1 la respuesta de google.com no brilla. El ejemplo del acto 7 es un banco ficticio ("mybank.com") que sí está firmado.
- La suplantación ataca el viaje de la pregunta entre bibliotecas (el resolvedor), que es el tramo que protege DNSSEC; no ataca a Steve directamente.
- El DNS cifrado (DoH, DoT) oculta las preguntas al proveedor de internet, pero el resolvedor que las recibe sí las ve. **Unbound no cifra**: pregunta directo a la raíz, a .com y al servidor de google en lugar de pasar por el resolvedor del proveedor. La línea 21 dice solo eso. No afirmar ni mostrar que unbound esconde las preguntas: en su viaje el libro va abierto y el que mira en el camino todavía lo puede leer.
- El resolvedor del acto 1 es el del proveedor de internet (lo normal en casa), por eso en el acto 8 hay un "bibliotecario de en medio" que unbound evita.
- La CDN copia el sitio (el lugar), no la biblioteca de DNS: la línea 22 dice "isn't one place".
- La línea 23 es cierta para Google (respuestas por ubicación y anycast).

## Escenas (qué se ve en cada parte)

Las líneas indican la narración que cubre cada escena.

1. **Portada y gancho (0 a 3):** la aldea al amanecer o de día, un letrero de madera grande en la entrada con "HOW DNS WORKS". Steve camina hacia un letrero de sendero que dice "google.com" y no sabe a dónde ir. Aparecen unas coordenadas flotando, al estilo de la pantalla de depuración del juego (F3), junto a un globo con "142.250.190.46".
2. **El resolvedor y su libro (4 y 5):** como en la prueba: Steve llega a la biblioteca, globo "Where is google.com?". El bibliotecario abre su libro y la página está vacía (cuaderno sin anotaciones).
3. **El recorrido (6 a 9):** la pregunta es un libro y pluma que vuela de biblioteca en biblioteca, y la cámara lo sigue:
   - La **raíz**: una torre alta de piedra en una loma, con su bibliotecario. Contesta con un globo que apunta a ".com".
   - **.com**: otra biblioteca con un letrero ".com". Apunta a "google.com".
   - **google.com**: una biblioteca con su atril y la respuesta escrita. Sin logo; el nombre en un letrero.
   - El libro regresa con la respuesta (sin brillo: google.com no usa DNSSEC) y el bibliotecario le da la brújula a Steve (la de la prueba, más grande). Steve camina hacia el lugar google.com.
4. **La caché y el TTL (10 a 12):** el bibliotecario escribe en su libro "google.com = 142.250.190.46" con un reloj del juego al lado. Llega Alex, pregunta lo mismo y la respuesta sale de inmediato, sin que vuele ningún libro. El reloj avanza y la anotación se borra.
5. **Transición (13):** la cámara sube y muestra la aldea completa.
6. **Bloqueo de anuncios (14 a 16):** Steve pide "ads.tracker.com". El bibliotecario tiene un libro con una lista negra (nombres tachados en rojo) y lo manda a un cuarto cerrado de bloques barrera. El anuncio (un cuadro o estandarte colgado) nunca aparece.
7. **Suplantación (17 a 19):** Steve pide "mybank.com". Mientras la pregunta viaja entre bibliotecas, un illager disfrazado (el modelo de illager; puede ser el ilusionista) intercepta el libro y regresa coordenadas falsas a un banco falso lleno de TNT, que explota o casi explota sin lastimar a Steve. Después, con DNSSEC: la respuesta real llega con el brillo morado de encantamiento y la falsa no brilla, así que el bibliotecario la tira (el "no" del aldeano).
8. **Privacidad (20 y 21):** el libro viaja abierto de Steve a la biblioteca del proveedor y alguien lo lee al pasar (se sugiere un vendedor ambulante). Con DNS cifrado el libro va en un cofre cerrado y el que mira no ve nada. Al final, Steve tiene su propia bibliotequita en casa (unbound; puede ser un atril junto a su casa) y su bibliotecario hace el recorrido a la raíz, a .com y a google sin pasar por la biblioteca del proveedor. En ese viaje el libro va abierto (unbound no cifra).
9. **CDN (22 y 23):** la cámara se aleja mucho y se ven varias copias del lugar google.com en distintas partes del mundo (o del mapa del juego). Se resalta la más cercana a Steve y a ella apuntan las coordenadas.
10. **Cierre (24 y 25):** repaso rápido del recorrido y la cámara vuelve a la toma de la portada. El último cuadro es igual al primero (loop).

## Cómo se hace

### Decisiones de Aldo

- Short vertical de hasta 3 minutos, todo en 3D, todo con Minecraft.
- Contenido y metáfora de arriba.
- Primero una prueba antes del render completo (ya hecha y aprobada).
- Los videos se le muestran abriéndolos en el navegador (Edge), no en el reproductor.
- Música de fondo de C418, obligatoria en todos los videos y shorts (regla del 2026-10-25).
- **Voz madura clonada** (`pruebas/voces_demo/04_madura_sensual.mp3` con Qwen3-TTS 0.6B Base), la de los videos recientes, **generada en esta PC de Windows** (Aldo, 2026-10-28).

### Decisiones de Claude (Aldo puede cambiarlas)

- **Aldea hecha por código** sobre un lote natural del mundo, no una aldea real del juego: `mundo.py` dibuja como cubo completo todo lo que no es natural (escaleras, puertas, atriles) y así las bibliotecas quedan donde la cámara las necesita.
- **Música:** `["subwoofer_lullaby", "mice_on_venus"]` si el video pasa de 209 s; si no, solo Subwoofer Lullaby.
- **Loop:** sí, como los shorts de LeetCode (último cuadro igual al primero), y sin el letrero "FULL VIDEO" de los shorts recortados.
- **Lugar:** uno nuevo, que ningún video use (`mundos/lugares.json`), sacado de los mundos de esta PC (MacEntorno solo vive en la Mac). Los lugares buenos de ClaudeEntorno ya se usaron: buscar otra zona del mundo (generar más terreno volando en el juego si hace falta) o aplanar con `plot` una zona amplia. Bioma de llanura o abedul por el tinte del pasto. Debe caber la aldea, la torre de la raíz y la toma lejana de la CDN.
- **Carpeta:** `videos/tech/dns/` (sección nueva `tech`).

### Piezas que hay que construir

1. **Personajes**, en un módulo nuevo del tema (por ejemplo `herramientas/temas/minecraft-original/gente.js`), sin tocar `vida.js`, que comparte otro agente:
   - Aldeano con capas (base + bioma + profesión): bibliotecario y otros oficios para las otras bibliotecas.
   - Jugador de brazos anchos: Steve y Alex (hay `alex.png` en `player/wide/`).
   - Illager para el impostor.
   - Animaciones: caminar, girar la cabeza, mirar abajo y el gesto de "no".
   - Los modelos de la prueba ya funcionan y se pueden llevar tal cual.
2. **Texturas y sonidos nuevos** copiados del juego por `extraer.py` (no a mano, para que otra PC los pueda volver a sacar): aldeano, profesiones, jugador, illager, atril, librero, tablones, troncos, piedra, cristal, sendero, TNT, cofre y reloj. Sonidos útiles: aldeano (`villager_no` ya existe; agregar el de aceptar), páginas de libro (ya existen), TNT y explosión, cofre (ya existe).
3. **Construcciones** por código: biblioteca (como la prueba, con techo de verdad y sin el cuadro rojo bajo el atril), torre de la raíz, bibliotecas de .com y de google.com, el cuarto de barreras y el banco falso con TNT.
4. **Voz sin Manim:** `pruebas/voces_demo/tts_qwen_clone.py` ya escribe `voiceover.mp3` y `timestamps.json` a partir de `narration.txt`, sin Manim. La página 3D toma los tiempos de ahí (`/timestamps.json`, como la plantilla del short 02-dfs).
   - Esta PC no tiene GPU NVIDIA (RX 6600) ni el venv `.venv-tts`. Hay que crearlo con torch de CPU y `qwen-tts` (sin el índice `cu126`); el script ya cae a CPU en `float32`. La PC tiene 12 hilos y 32 GB de RAM.
   - **Primer paso del trabajo:** clonar una sola línea para medir la velocidad en CPU y que Aldo escuche que es la misma voz. Si es demasiado lento, avisarle antes de seguir.
   - Kokoro (`af_heart`) queda solo como respaldo si Aldo lo pide.
5. **Un modo "solo 3D" en `build.py`**: renderizar la página a 1080 × 1920 por la duración del audio y mezclar voz, efectos y música con el paso `mux` que ya existe. Los efectos de sonido se marcan desde la página (hoy salen de `self.sfx()` de Manim). El cambio debe sumar sin romper los videos que ya existen: ningún `video.json` anterior debe cambiar de comportamiento.
6. **Cámara:** una lista de tomas por línea de narración (`poseTrack` de `stage.js` ya lo hace), con tomas abiertas para las transiciones y cercanas para los globos y libros.

### Lo que queda a criterio del constructor

- Cómo se organizan los archivos dentro de `videos/tech/dns/`.
- El diseño exacto de cada construcción y la posición de las bibliotecas, mientras quepan en el cuadro y se lean.
- El nombre y la forma del modo "solo 3D" en `build.py` y de las marcas de efectos.
- La hora del día y los mobs de fondo, mientras se vean bien y no distraigan.
- Ajustes pequeños de la narración (sin cambiar hechos ni pasar de 180 s).

## Forma de trabajo y revisiones

1. Antes del render completo, **cuadros fijos de cada escena** (`render.mjs --stills`) en una hoja 9:16 para que Aldo los vea. El render completo va después de su visto bueno. Tarda unos 3 minutos: la prueba hizo 450 cuadros en 27 s.
2. **La voz se revisa línea por línea** (Aldo notó fallas de TTS en otros videos): duración de cada línea contra lo esperado, `silencedetect` para silencios raros y, si se puede, transcribir el audio y compararlo con el guion. Las líneas sospechosas se le avisan a Aldo, no se dan por buenas.
3. Revisar la lista "Errores ya cometidos (no repetir)" de `GUIA.md`. Las que más aplican aquí:
   - Sprites tapados por el terreno (renderOrder).
   - Contenido fuera del cuadro.
   - Textos que no caben.
   - La fuente del juego no tiene `→`, `³`, `≠` ni `✓`.
   - La narración debe decir exactamente lo que se ve.
4. Antes de entregar: la duración del video igual a la del audio, la música presente, el loop (diferencia media del primer y el último cuadro menor a 1) y verlo en movimiento.
5. Al terminar: entrada en `BITACORA.md`, el lugar en `mundos/lugares.json`, una sección en `GUIA.md` sobre los videos solo 3D, `descripcion.txt` (100 caracteres o menos) y el video abierto en Edge para Aldo. **Sin commit ni push** hasta que Aldo lo pida, y sin firma de IA en los commits.

## Restricciones

- Nunca subir archivos de Mojang. Las texturas nuevas van en carpetas del tema que ya están en `.gitignore`, o en una nueva que se agregue a él.
- Otro agente puede trabajar en LeetSolve al mismo tiempo: revisar `git status` antes de editar archivos compartidos (`build.py`, `stage.js`, `mc.js`, `vida.js`, `GUIA.md`, `BITACORA.md`).
- Entorno de Windows: `export PATH="$HOME/.manim-skill-src/.venv/Scripts:$PATH" PYTHONUTF8=1`; `python`, no `python3`.
- Código en inglés con comentarios breves; documentos en español.
- Al publicar: "Not an official Minecraft product" en la descripción y los créditos de la música de C418.
