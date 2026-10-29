# Diseño: short "Why video doesn't freeze" (streaming adaptativo), todo en 3D

Estado: borrador para que Aldo lo apruebe (2026-10-28). Nada se construye hasta que lo apruebe. Cuando lo apruebe, se hace **solo el código** (voz y render en otra sesión), como SQL y el servidor.

## Intención

Short de la línea "cómo funcionan las tecnologías": por qué Netflix y YouTube siguen reproduciendo aunque baje tu internet. La respuesta es el **streaming de bitrate adaptativo**: el video se corta en pedazos de pocos segundos, cada pedazo existe en varias calidades, el reproductor guarda pedazos por adelantado (buffer) y en cada pedido elige la calidad según la velocidad y lo lleno del buffer.

Misma forma que los anteriores: cómo funciona (~70 s) y luego lo que ves por eso (~45 s). Todo en 3D, voz madura clonada, música de C418, menos de 3 minutos.

## Metas

- Que se entienda: **pedazos + varias calidades + manifiesto + buffer + elegir calidad en cada pedazo**.
- Que se **vea** el momento clave: el internet baja, el buffer se empieza a vaciar, el reproductor pide pedazos más ligeros y la imagen se pone borrosa pero no se detiene.
- Explicar dos cosas que todos han visto: por qué los videos **empiezan borrosos** y qué es la **rueda de carga**.
- Reutilizar `rieles.js` (vagonetas) del short de paquetes.

## Fuera del alcance

- Códecs y compresión (H.264, AV1, cuadros clave), audio aparte, DRM, transmisiones en vivo.
- Cómo viajan los paquetes (ya tiene su short) y la CDN en detalle (se menciona en una frase; DNS ya la cuenta).

## No debe pasar (aunque técnicamente funcione)

- Logos de Netflix o YouTube, ni su interfaz copiada. Los nombres solo como texto en la narración.
- La rueda de carga con el diseño de una marca: un anillo genérico de cuadros blancos.
- Decir cifras exactas que varían por servicio (largo de los pedazos, tamaño del buffer).
- Que las calidades no se distingan en el celular: la diferencia entre baja y alta debe ser muy obvia (pixelado contra nítido).

## La metáfora

- **La película** = una sucesión de cuadros (pinturas) del juego. Cada **pedazo** es una pintura con su número (1, 2, 3...). Se usan las pinturas del juego (`kebab`, `aztec`, `sunset`, `sea`, `pool`, `creebet`...), sin inventar arte.
- **Calidades** = la misma pintura con más o menos pixeles: 240p muy pixelada (la textura reducida a 1/8), 480p (1/4), 1080p (1/2) y 4K (la original del juego). Se generan en la página reduciendo la textura y volviéndola a ampliar sin suavizado.
- **Peso** = lo que carga la vagoneta: un pedazo en 4K va en una vagoneta llena (4 cofres apilados), uno en 240p en un solo cofre chico. Un letrero dice el peso ("4K: heavy", "240p: light").
- **El servidor** = un almacén al fondo con un estante: filas por calidad, columnas por pedazo.
- **El manifiesto** = un libro en un atril del cine que lista los pedazos y sus calidades.
- **El camino** = una vía de rieles del almacén al cine. **Internet rápido** = rieles propulsados encendidos; **internet lento** = se apagan y las vagonetas avanzan despacio.
- **El reproductor** = el bibliotecario del cine. Mira un reloj (qué tan rápido llegó el último pedazo) y la fila del buffer, y escribe en un papel la calidad del siguiente pedido.
- **El buffer** = una fila de 6 marcos junto a la pantalla. Los pedazos que llegan entran por la derecha; la pantalla toma el de la izquierda.
- **La pantalla** = una pintura grande (marco 4 × 2) frente a Steve, que va mostrando los pedazos en su calidad.
- **La rueda de carga** = la pantalla en negro con un anillo de 8 cuadros blancos que giran.

## Narración (borrador, en inglés)

Unas 330 palabras, ~115 s. En `narration.txt`, "four K", "H L S", "dash".

```
0  Your internet slows down, but the video keeps playing. It just gets a little blurry. How?
1  Because the video never comes as one big file. It's cut into small pieces, a few seconds each.
2  And every piece is ready in several qualities. Low, medium, high, even 4K.
3  Higher quality looks sharper, but it's a heavier piece, with more data to carry.
4  First, your player gets a menu, called a manifest. It lists every piece in every quality.
5  Then it asks for the pieces one by one, and they travel to you from a server, often one close to you.
6  The player doesn't wait for each piece. It keeps a buffer, a line of pieces ready ahead of time.
7  While you watch one piece, the next ones are already on their way.
8  Now the smart part. Before each request, the player checks two things.
9  How fast did the last pieces arrive? And how full is the buffer?
10 Fast rails and a full buffer? Ask for high quality.
11 Then your internet drops. The rails slow down, and the buffer starts to drain.
12 So the player switches to lighter pieces. They arrive in time, and the buffer stops draining.
13 The picture gets a bit blurrier, but the video never stops.
14 When the connection recovers, the quality climbs back up, piece by piece.
15 That's also why videos often start blurry. A light first piece starts playing sooner.
16 And if the buffer ever runs empty? That's the spinning wheel. The player has nothing left to show.
17 This is called adaptive streaming. Formats like HLS and DASH work this way, and big video apps use them.
18 So every video is a line of small pieces, a buffer, and a player choosing, again and again, how heavy the next one can be.
19 That's why video doesn't freeze.
```

### Exactitud (revisar antes de generar la voz)

- **Pedazos (segmentos):** suelen durar de 2 a 10 s según el servicio; la narración dice "a few seconds".
- **Varias calidades:** cada pedazo se codifica en una escalera de calidades (por ejemplo de 144p a 4K en YouTube). La línea 2 no da la lista exacta.
- **Manifiesto:** HLS usa una lista `.m3u8` y DASH un archivo `.mpd`; los dos listan los pedazos y sus calidades. Correcto como "menu".
- **Elegir calidad:** los algoritmos reales usan la velocidad medida de las descargas recientes, el nivel del buffer o los dos. La línea 9 dice exactamente esas dos cosas.
- **El cambio de calidad** pasa entre pedazos, no a la mitad de uno: por eso se ve "piece by piece".
- **Buffer:** de unos segundos a varios minutos según el servicio; no se da cifra.
- **Empezar borroso:** muchos reproductores empiezan con una calidad baja para arrancar rápido y luego suben. "often" en la línea 15.
- **Rueda de carga:** aparece cuando el buffer se vacía (rebuffering). Correcto.
- **Servidor cercano:** los servicios grandes usan CDN; "often one close to you".
- **HLS y DASH:** formatos reales de streaming adaptativo. Netflix usa DASH y YouTube usa DASH (y HLS en algunos dispositivos); por eso la línea 17 no asigna formato a cada marca.

## Datos del ejemplo

- 12 pedazos, cada uno una pintura distinta del juego.
- Calidad de cada pedazo en el recorrido: 1 en 240p (arranque rápido, línea 15 lo explica después), 2 en 480p, 3 a 6 en 1080p/4K (rieles rápidos), 7 y 8 bajan a 480p y 240p (internet lento), 9 y 10 suben a 480p y 1080p, 11 y 12 en 4K.
- El buffer pasa de 4-5 pedazos a 1 en la caída y nunca llega a 0. Para la rueda de carga (línea 16) se muestra aparte: el buffer en 0 y la pantalla en negro.

## Escenas (qué se ve en cada parte)

1. **Gancho (0):** Steve en su cine casero frente a la pantalla grande. Un rayo/nube oscura sobre los rieles y la imagen se vuelve pixelada, pero sigue cambiando.
2. **Pedazos (1):** la película como una tira de pinturas numeradas que se separa en pedazos.
3. **Calidades (2 y 3):** el estante del almacén: la misma pintura en 4 filas (240p a 4K). Vagonetas de prueba: la de 4K con 4 cofres, la de 240p con uno.
4. **Manifiesto (4):** el bibliotecario abre el libro del atril: "1: 240p 480p 1080p 4K / 2: ...".
5. **Viaje (5):** toma aérea: el almacén al fondo, la vía, el cine. Una vagoneta sale con el pedazo 1.
6. **Buffer (6 y 7):** la fila de 6 marcos se llena; la pantalla toma el primero mientras llegan más vagonetas.
7. **Decisión (8 a 10):** el bibliotecario mira el reloj ("last piece: fast") y el buffer ("4 ready"); escribe "4K" en el papel, que vuela al almacén.
8. **Caída (11 a 13):** los rieles propulsados se apagan, las vagonetas van despacio, el buffer baja a 1. El bibliotecario escribe "240p": llegan vagonetas ligeras a tiempo. La pantalla se ve pixelada pero sigue.
9. **Recuperación (14):** los rieles se encienden y la calidad sube pedazo por pedazo (480p, 1080p, 4K).
10. **Arranque borroso (15):** repetición del inicio: el primer pedazo ligero llega primero y la pantalla arranca pixelada.
11. **Rueda de carga (16):** buffer vacío, pantalla negra con el anillo girando.
12. **Nombre (17):** globos "adaptive streaming", "HLS", "DASH" sobre la vía.
13. **Cierre (18 y 19):** repaso (pedazos, buffer, bibliotecario eligiendo) y vuelta a la portada. Loop.

## Cómo se hace

### Decisiones de Claude (Aldo puede cambiarlas)

- **Carpeta:** `videos/tech/streaming/`. Título en pantalla: "WHY VIDEO DOESN'T FREEZE".
- **Rieles:** `rieles.js` (vías, vagonetas, avance por llaves). Los rieles propulsados necesitan las texturas `powered_rail` y `powered_rail_on` en `extraer.py`, y las pinturas del juego (`painting/*`) que se usen.
- **Calidades** generadas en la página desde la textura de cada pintura (reducción a 1/8, 1/4, 1/2 y original, con `NearestFilter`).
- **Lugar:** uno nuevo de `lugares.json`, largo y plano para la vía (unos 40 bloques).
- **Música:** Subwoofer Lullaby, u otra pista de C418 para variar.

### Piezas que hay que construir

1. Cine casero (pared con la pantalla 4 × 2, la fila del buffer de 6 marcos, el atril del manifiesto y el bibliotecario).
2. Almacén con el estante de 4 × 12 pinturas.
3. Vía con rieles propulsados que se encienden y apagan, y vagonetas con 1 a 4 cofres según la calidad.
4. Pinturas en 4 calidades, la pantalla que cambia de pedazo y la rueda de carga.
5. Planificador del recorrido en la página: tiempos de llegada de cada vagoneta según su peso y la velocidad de la vía, y el nivel del buffer en cada momento, para que lo que se ve sea coherente (el buffer nunca muestra algo imposible).

## Forma de trabajo y restricciones

Igual que SQL y el servidor: solo código y revisión de la lógica (el planificador del buffer se comprueba en Node); voz y render en otra sesión. Sin commit ni push hasta que Aldo lo pida. Nunca subir archivos de Mojang. Otra sesión puede estar editando `extraer.py`, `rieles.js` o `lugares.json`: revisar `git status` antes de tocarlos.
