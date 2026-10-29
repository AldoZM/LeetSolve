# Diseño: short "What a server does inside" (Request → Response y APIs REST), todo en 3D

Estado: aprobado por Aldo el 2026-10-28 (🟢), con las recomendaciones: misma aldea que SQL y el gólem agregado a `extraer.py` por esta sesión. Código escrito; **voz y render en otra sesión**. Ver "Estado del código" al final.

## Intención

Segundo short de **backend** de la línea "cómo funcionan las tecnologías" (después de "How SQL works"). Explica qué pasa dentro de un servidor desde que llega una petición hasta que sale la respuesta, y qué es una API REST. Sin redes: la petición ya llegó a la puerta (eso lo cuentan los shorts de DNS, HTTPS y paquetes).

Misma forma que DNS y SQL: primero el recorrido completo de una petición (~70 s) y luego REST (~50 s). Todo en 3D, voz madura clonada, música de C418, menos de 3 minutos.

## Metas

- Un short vertical (1080 × 1920, 30 fps) de **menos de 3 minutos**.
- Que se entienda que una petición tiene **verbo, ruta, encabezados y a veces cuerpo**, y que la respuesta tiene **código de estado y cuerpo** (JSON).
- Que se vea el camino dentro del servidor: **router → middleware → handler → base de datos → respuesta**.
- Que REST quede como: **recursos con ruta + pocos verbos + códigos de estado + sin estado**.
- Continuidad con el short de SQL: el handler baja a **la misma sala de la tabla `players`** por la fila de Ren.

## Fuera del alcance

- Redes, puertos, TLS, DNS (ya tienen sus shorts).
- GraphQL, gRPC, WebSockets, frameworks concretos (Express, Spring), hilos y asincronía.
- Caché, colas y escalar en detalle: solo se menciona que, por no guardar estado, un servidor puede volverse diez iguales.

## No debe pasar (aunque técnicamente funcione)

- Decir algo falso de HTTP o REST (ver "Exactitud").
- Códigos o rutas ilegibles en el celular. Las notas llevan **una sola línea** grande (`GET /players/ren`).
- Que parezca diagrama 2D: la petición es un objeto que viaja por tolvas dentro de un taller.
- Caracteres que la fuente del juego no tiene (`→`, `✓`). `{`, `}`, `"`, `:` y `/` sí existen; confirmar en la hoja de cuadros.

## La metáfora

- **Servidor** = un taller de la aldea (edificio de piedra y madera) con una ranura en la puerta.
- **Petición** = una nota (papel) con una línea: verbo y ruta (`GET /players/ren`). Pegada, una **etiqueta de nombre** (encabezado de autorización). Si lleva datos, un **libro** (el cuerpo).
- **Recorrido interno** = una cadena de **tolvas** que lleva la nota de estación en estación.
- **Router** = un **clasificador de objetos** (tolvas con filtro): cada salida tiene un letrero con su ruta (`/players`, `/orders`, `/messages`) y la nota cae por la suya.
- **Middleware** = estaciones de revisión en la cadena:
  - Un aldeano revisa la etiqueta de nombre. Sin etiqueta válida, la nota regresa sellada **401**.
  - Un **gólem de hierro** cuenta las notas de cada quien. Si son demasiadas, la detiene: **429**.
- **Handler** = el trabajador de la ruta (el bibliotecario de `/players`). Baja a la sala de SQL y saca la fila de Ren.
- **Respuesta** = un libro escrito con el JSON (`{"name": "Ren", "emeralds": 25}`) y un **sello** grande con el código (`200 OK`), que regresa por la ranura.
- **REST:**
  - Cada **recurso** es un cofre/estante con su ruta en un letrero.
  - Los **verbos** son notas de cuatro colores: GET (verde) lee, POST (azul) crea, PUT/PATCH (amarillo) cambia, DELETE (rojo) borra.
  - **Sin estado**: el trabajador no recuerda a nadie; Steve muestra su etiqueta en **cada** nota. Por eso al final aparecen diez talleres idénticos y cualquiera puede contestar.

## Narración (borrador, en inglés)

Unas 370 palabras, ~128 s. En `narration.txt` los números y las rutas van como se dicen ("four oh one", "slash players slash Ren").

```
0  You tap a button, and somewhere a server gets a note. What happens inside before you get an answer?
1  That note is a request. It says what you want to do, and to what.
2  Like this: GET /players/ren. GET is the verb. The path names the thing.
3  It can also carry headers, like your name tag, and sometimes a body with data.
4  Picture the server as a workshop. The note drops into a line of hoppers.
5  First, the router reads the verb and the path, and sends the note to the right worker.
6  On the way, it passes checkpoints called middleware.
7  One checks your name tag. No valid tag, and the note bounces back: 401, unauthorized.
8  Another counts your notes. Too many, too fast, and the golem stops you.
9  Then the handler, the worker who does the real job. He asks the database for Ren's row.
10 He writes the answer as JSON, a simple text format: name Ren, emeralds 25.
11 He stamps a status code on top, 200 OK, and sends it back. Often in a few milliseconds.
12 Now, REST. It's a common way to design these notes, so apps talk to servers the same way.
13 Everything is a resource with its own path. Players, orders, messages.
14 And a few verbs do the work. GET reads. POST creates. PUT or PATCH changes. DELETE removes.
15 Same path, different verb, different job.
16 The status code says what happened. 200, it worked. 201, created. 404, not found. 500, the server broke.
17 And the server doesn't remember you between notes. Each request brings everything it needs, name tag included.
18 That's what lets one server become ten identical ones, and any of them can answer.
19 So every tap is a note: a verb, a path, a few checkpoints, a worker and a stamped answer.
20 That's what a server does inside.
```

### Exactitud (revisar antes de generar la voz)

- **Petición HTTP:** método, ruta (URL), encabezados y cuerpo opcional. GET normalmente no lleva cuerpo; POST, PUT y PATCH sí. La etiqueta de nombre representa el encabezado `Authorization` (un token).
- **Router:** elige el handler por **método y ruta**, no solo por la ruta (la línea 5 lo dice).
- **Middleware:** funciones que corren antes del handler, en orden, y pueden cortar la petición. Autenticación y límite de peticiones son ejemplos reales.
- **401 Unauthorized** = falta autenticación o no es válida. (403 sería "sé quién eres pero no puedes"; no se menciona.) El gólem devuelve **429 Too Many Requests**: se muestra en el sello, la voz no lo dice.
- **JSON** es texto; el ejemplo `{"name": "Ren", "emeralds": 25}` es JSON válido. Es el formato más común en APIs REST, no el único.
- **"Often in a few milliseconds"**: verdadero para peticiones simples; no decir "siempre".
- **REST:** estilo de diseño (Roy Fielding), no un protocolo. Recursos identificados por rutas, operaciones con los métodos de HTTP. PUT reemplaza el recurso completo y PATCH cambia una parte: la línea 14 los junta como "changes", que es correcto.
- **Códigos:** 200 OK, 201 Created (después de un POST que crea), 404 Not Found, 500 Internal Server Error.
- **Sin estado (stateless):** es una restricción de REST: cada petición trae lo necesario para entenderla. Gracias a eso, cualquier copia del servidor puede atender cualquier petición (escalar horizontalmente). Los datos sí viven en la base de datos; lo que no guarda el servidor es la conversación.

## Datos del ejemplo

- Recurso `players`, la misma tabla del short de SQL (Steve 12, Alex 30, Noor 4, Kai 18, Zuri 9, Ren 25).
- Línea 2 y 9 a 11: `GET /players/ren` → `200 OK`, `{"name": "Ren", "emeralds": 25}`.
- Línea 15 (mismo recurso, cuatro verbos sobre la fila de Ren o sobre la tabla):
  - `GET /players/ren`: la fila de Ren brilla.
  - `POST /players` con el libro `{"name": "Mia"}`: aparece una fila nueva, sello `201`.
  - `PATCH /players/ren` con `{"emeralds": 30}`: el número cambia de 25 a 30, sello `200`.
  - `DELETE /players/ren`: la fila se rompe (sonido de romper), sello `200` (o `204`; se usa 200 para no explicar otro código).
- Línea 16: `GET /players/bob` → cofre vacío, sello `404`; una nota que hace explotar el horno del trabajador → `500`.

## Escenas (qué se ve en cada parte)

1. **Gancho (0 y 1):** Steve en la aldea frente al taller (letrero "WHAT A SERVER DOES INSIDE" o "INSIDE A SERVER"). Toca un botón de piedra y una nota sale volando a la ranura de la puerta.
2. **La nota (2 y 3):** toma cercana de la nota: `GET /players/ren`. La palabra GET se ilumina, luego la ruta. Se pega la etiqueta de nombre (headers) y aparece un libro a un lado (body), con globos.
3. **El taller (4):** la cámara entra: cadena de tolvas que recorre el taller, con la nota cayendo dentro.
4. **Router (5):** el clasificador con tres salidas y letreros (`/players`, `/orders`, `/messages`). La nota cae por `/players`.
5. **Middleware (6 a 8):** un aldeano con lupa/libro revisa la etiqueta (brillo verde, sigue). Una nota de un ilusionista sin etiqueta regresa con sello rojo `401`. Después el gólem de hierro: un montón de notas del mismo jugador llega de golpe y el gólem detiene las últimas (sello `429`).
6. **Handler (9):** el bibliotecario de `/players` recibe la nota y baja por una escalera a **la sala de SQL**: la fila de Ren brilla en la tabla.
7. **JSON (10):** el bibliotecario escribe en un libro; globo con `{"name": "Ren", "emeralds": 25}`.
8. **Respuesta (11):** sello grande verde `200 OK` cae sobre el libro, que sale por la ranura y llega a Steve. Un reloj del juego marca que fue rápido.
9. **REST (12 y 13):** toma aérea del taller: tres estaciones con su recurso en un letrero (players, orders, messages).
10. **Verbos (14 y 15):** cuatro notas de colores llegan a `/players` una tras otra y cada una hace su trabajo en la tabla (leer, fila nueva Mia, 25 → 30, romper la fila).
11. **Códigos (16):** cuatro sellos en fila: `200` verde, `201` azul, `404` amarillo (cofre vacío), `500` rojo (el horno del trabajador echa humo y fuego).
12. **Sin estado (17 y 18):** Steve manda dos notas seguidas y el trabajador lo mira como si no lo conociera; las dos llevan la etiqueta. La cámara sube y aparecen diez talleres idénticos; las notas caen en cualquiera.
13. **Cierre (19 y 20):** repaso rápido (nota, tolvas, revisión, trabajador, sello) y vuelta a la portada. Loop.

## Cómo se hace

### Decisiones de Claude (Aldo puede cambiarlas)

- **Continuidad con SQL:** el taller y la sala de la tabla `players` están en el mismo lugar. Lo más simple: copiar la sala de `videos/tech/sql/three/sql.html` a este video (no compartir código entre páginas todavía) o mover la sala a `aldea.js` si Aldo quiere más shorts de backend en la misma aldea.
- **Gólem de hierro:** se arma con `entityPart` y `skinMat` como el creeper del short de SQL. Hace falta su textura en `extraer.py` (`entity/iron_golem/iron_golem`); se agrega cuando la otra sesión termine con ese archivo.
- **Tolvas:** bloque de tolva con su modelo (no es cubo): hacerlo con las texturas del juego (`hopper_outside`, `hopper_top`, `hopper_inside`), sin inventar la forma (regla de `model_icon`).
- **Sellos:** globos grandes del estilo tooltip, de color por código (verde 2xx, amarillo 4xx, rojo 5xx).
- **Música:** Subwoofer Lullaby, o otra pista de C418 para variar.
- **Carpeta:** `videos/tech/server/`. Lugar nuevo de `lugares.json` (o el mismo de SQL si se quiere la misma aldea).

### Piezas que hay que construir

1. Taller con ranura, cadena de tolvas, clasificador con tres salidas y estaciones de revisión.
2. Notas de papel con texto legible (una línea grande) y de cuatro colores; sellos de código.
3. Gólem de hierro (modelo del juego) y el aldeano revisor.
4. La sala de la tabla (del short de SQL) y una escalera que baja a ella.
5. Diez copias del taller para la toma de "sin estado" (instanciadas o a lo lejos con niebla).

## Forma de trabajo y revisiones

Igual que SQL: primero solo el código y la revisión de la lógica; en otra sesión, voz, cuadros fijos para Aldo, render completo, loop y la lista de revisión de `GUIA.md`. Sin commit ni push hasta que Aldo lo pida.

## Restricciones

- Otra sesión trabaja en LeetSolve (`gente.js`, `extraer.py`, `rieles.js`, `lugares.json`): no tocar sus archivos sin coordinar.
- Nunca subir archivos de Mojang.
- Código en inglés con comentarios breves; documentos en español.
- Al publicar: "Not an official Minecraft product" y los créditos de la música de C418.

## Estado del código (2026-10-28, laptop)

Hecho, sin voz ni render:

- `narration.txt` (21 líneas, 317 palabras, unos 115 s), `video.json` (solo3d, 9:16, Subwoofer Lullaby) y `descripcion.txt` (97 caracteres).
- `three/server.html`: toda la página. Revisada con `node --check`; el JSON que sale en pantalla se validó en Python.
- `three/timestamps.json`: **provisional** (palabras / 2.9 por segundo). **Borrarlo antes del render final.**
- `extraer.py`: tolva (`hopper_outside`, `hopper_top`, `hopper_inside`), horno (`furnace_*`), fuego (`fire`, tira de 32 cuadros), gólem (`mobs/iron_golem.png`, 128 × 128) y los sonidos `golem_hit`, `anvil_land` y `fire`. Se corrió `extraer.py 26.3` en la laptop y todos existen.

Cómo quedó:

- **Lugar:** el mismo de SQL (`mac-02` de prueba). La sala de la tabla `players` se copió de `sql.html` (con una fila más de espacio para Mia). El taller va enfrente de la sala (z 30 a 43), con una ranura en el frente y una puerta atrás hacia la sala.
- **Tolvas** con la forma de `block/hopper.json` (piso, 4 bordes, centro y pico) y las UV automáticas del juego (`modelBox`). Una entrada de 4, una fila de 9 que hace de router y 3 carriles de 5.
- **Notas:** papel con una línea (el verbo en su color y la ruta) y la etiqueta dibujada en la nota cuando la lleva. Mantienen su tamaño en pantalla con `placeUI`; las del montón del gólem y las de las diez copias son sprites chicos.
- **Gólem** armado con `entityPart`/`skinMat` según `IronGolemModel` (cabeza con nariz, cuerpo, brazos que golpean, piernas).
- El bibliotecario va de su mesa a la puerta trasera y aparece en la sala cuando la cámara corta a la tabla (línea 9); en las líneas 14 y 15 está en la tabla mientras llegan las cuatro notas de REST.
- Línea 16: los cuatro sellos apilados sobre la mesa; el cofre del 404 se abre vacío y el horno se enciende con fuego y humo (500).
- Línea 18: diez talleres a escala 0.55 detrás de la sala.

Falta, para la sesión del render: elegir el lugar (y anotarlo en `lugares.json` junto con SQL), la voz (`tts_qwen_clone.py videos/tech/server`), cuadros fijos para ajustar las cámaras (calculadas a mano), borrar el `timestamps.json` provisional y el render.
