# Diseño: short "How packets work", todo en 3D

Estado (2026-10-28): Aldo eligió el tema ("nos vamos por lo que son los paquetes") y pidió aplicar lo mismo que en DNS, empezando por el código y dejando la voz y el render para otro momento. El código está escrito; la voz y el render no se han hecho. Es el tercer short de la línea "cómo funcionan las tecnologías" (`videos/tech/`), después de DNS y HTTPS/TLS.

## Intención

Explicar cómo viaja algo por internet: no va entero, se corta en paquetes que cruzan una red de routers paso a paso. Todo pasa en Minecraft: los paquetes son vagonetas con cofre sobre rieles y cada cruce es una estación con un cartógrafo que solo sabe el siguiente tramo. Igual que DNS y HTTPS: 100 % 3D, sin Manim, voz madura clonada, música de C418, menos de 3 minutos.

## Metas

- Que alguien sin conocimientos técnicos se lleve tres ideas: los datos viajan en pedazos, ningún router conoce el camino completo y los pedazos pueden perderse o llegar en desorden (y TCP lo arregla).
- De paso: el time to live (por qué un error en la red no la tapa para siempre) y qué es el ping y el lag.
- Reusar las piezas de DNS y HTTPS (`gente.js`, `aldea.js`, modo `solo3d`) y dejar los rieles como pieza nueva para otros shorts (`rieles.js`).

## Fuera del alcance

- UDP, la comparación con TCP, el saludo de tres pasos de TCP y el control de congestión: quedan para otro short.
- Direcciones IP a fondo, máscaras, NAT y puertos.
- Escenas de Manim, código en pantalla y subtítulos quemados.
- Publicar, hacer commit o push: lo decide Aldo.

## No debe pasar (aunque técnicamente funcione)

- Que la narración diga algo falso o exagerado (ver "Exactitud").
- Que parezca un diagrama 2D con fondo 3D: la cámara vive en el mundo y sigue a las vagonetas.
- Texto ilegible en el celular, cortado o tapado por el terreno.
- Que el número de cada paquete no se lea: es lo que hace entender el desorden y el hueco.
- Subir al repositorio archivos del juego (texturas, sonidos, música).

## La metáfora

- **La foto** es el cuadro del juego `bust` (2 × 2 bloques). Cada bloque del cuadro es un paquete: 4 paquetes. La narración aclara que en la realidad son miles.
- **El paquete** es una vagoneta con cofre (el modelo del juego). Lleva su pedazo del cuadro flotando encima y un número (1 a 4). La etiqueta se muestra una vez en un globo: `packet 2 of 4`, `to: 198.51.100.7`, `from: 203.0.113.5`.
- **La red** son rieles. **Cada cruce es un router**: un puesto con techo, un atril con el libro de rutas y un aldeano cartógrafo.
- **La tabla de rutas** es el libro del atril: `198.51.100.* -> right`, `anything else -> left`. Solo dice el siguiente tramo.
- **Otras vagonetas vacías** son el tráfico de otras personas. Hacen la fila en el router ocupado.
- **El paquete perdido**: la fila del router R está llena, así que el 3 se encoge y desaparece (sonido `fizz`) y queda una barrera donde estaba.
- **TCP**: Alex pone los pedazos en una repisa en el orden en que llegan (1, 4, 2), luego los acomoda en el marco por número, ve el hueco del 3 (barrera en el marco) y manda un papel a Steve: "Got everything up to 2. Send 3 again!". Llega una copia nueva del 3 y el cuadro se completa.
- **Time to live**: una vagoneta vacía queda atrapada en un lazo entre L y LB. El globo `TTL 4` baja uno en cada estación y en 0 la vagoneta se quita.
- **Ping**: una vagoneta va y un papel regresa; un reloj del juego sobre Steve y el globo `ping: 40 ms`. Luego una fila larga en R y `ping: 180 ms`.

## Narración

En `narration.txt`: 23 líneas, 306 palabras, unos 118 s a 2.6 palabras por segundo. Las siglas van escritas como se dicen ("T C P"). Las direcciones IP solo aparecen en globos, no se dicen.

## Exactitud (revisar antes de generar la voz)

- Un paquete IP típico lleva hasta unos 1500 bytes (la MTU de Ethernet). Una foto de unos MB son miles de paquetes: "thousands" es correcto.
- El encabezado IP lleva la dirección de destino y la de origen. **El número de orden no es de IP**: es el número de secuencia de TCP (en bytes, no en paquetes). La línea 2 lo junta todo en "a label"; es una simplificación aceptable, pero no decir que el router usa el número.
- Los routers deciden por paquete con su tabla de rutas y solo eligen el siguiente salto: líneas 4 a 6, correctas.
- Los paquetes de una misma conexión suelen ir por el mismo camino, pero **pueden** ir por caminos distintos (balanceo de carga, cambios de ruta) y llegar en desorden. La línea 7 dice "don't always", no "never".
- Un router con la cola llena tira los paquetes que llegan (tail drop): línea 9, correcta.
- El reordenamiento y el reenvío los hace TCP en las computadoras de los extremos, no los routers. La línea 13 es un ACK acumulado: después de 1, 4 y 2, Alex confirma "todo hasta el 2" y Steve reenvía el 3. Correcto.
- TTL (IPv4) o hop limit (IPv6): cada router le resta uno y en 0 descarta el paquete (y avisa con ICMP Time Exceeded). En la realidad empieza en 64 o más; el video empieza en 4 para que se vea. La narración no dice el número inicial.
- Ping: el tiempo de ida y vuelta. Lo suben la distancia, los saltos y las filas: línea 20, correcta. 40 ms y 180 ms son ejemplos razonables.
- Las IP son de los rangos reservados para documentación (198.51.100.0/24 y 203.0.113.0/24, RFC 5737): no son de nadie.

## Escenas

Las líneas indican la narración que cubre cada escena.

1. **Portada (cuadro 0):** letrero "HOW PACKETS / WORK" frente a la casa de Steve.
2. **La foto (0 y 1):** Steve junto a su pared con el cuadro. Globo "Send this photo to Alex". El cuadro se separa en 4 bloques y se vuelve a juntar ("1 photo = thousands of packets / (here: 4)").
3. **Las vagonetas (2):** cuatro vagonetas con cofre en fila sobre la vía de Steve. Una copia de cada pedazo vuela a su cofre (el cuadro se queda con Steve). Globo con la etiqueta del paquete 2.
4. **La red (3):** toma aérea de toda la red con globos "router" sobre las 5 estaciones y tráfico de otras vagonetas.
5. **El router (4 y 5):** el cartógrafo de A ("The whole way to Alex? No idea.") y el libro de rutas abierto.
6. **Saltos (6):** la cámara sigue al paquete 1 por A, R y B ("hop 1", "hop 2", "hop 3") hasta la casa de Alex.
7. **El camino largo (7):** toma aérea del paquete 2 yéndose por la izquierda (L y LB).
8. **Filas (8):** el paquete 2 espera detrás de dos vagonetas en LB; la fila llena en R ("busy!").
9. **Paquete tirado (9 y 10):** el 3 llega a R, el cartógrafo dice "Line is full. Thrown away!", la vagoneta desaparece y queda una barrera ("packet 3: lost"). Sale el paquete 4.
10. **Llegadas (11):** en la casa de Alex llegan el 4 y luego el 2 (el 1 ya estaba) y suben a la repisa: "got 1, 4, 2".
11. **Ordenar (12):** los pedazos bajan a su lugar en el marco; barrera en el lugar del 3 ("missing: 3").
12. **Reenvío (13 y 14):** el papel vuela de Alex a Steve (toma aérea), sale la copia del 3, llega y el cuadro se completa ("photo complete", sonido de nivel).
13. **TCP (15):** globo "TCP / numbers, order, / resend what was lost".
14. **Time to live (16 a 18):** la vagoneta atrapada en el lazo, el TTL baja de 4 a 0 y se quita ("removed"); toma aérea con el tráfico normal ("no endless loops").
15. **Ping y lag (19 y 20):** ida y vuelta con el reloj ("ping: 40 ms"); fila larga en R ("long line = lag / ping: 180 ms").
16. **Cierre (21 y 22):** toma aérea con tráfico y vuelta a la portada. El último cuadro es igual al primero (loop).

## Cómo se hace

### Decisiones de Aldo

- Tema: paquetes. Igual que DNS: short vertical de menos de 3 minutos, todo en 3D, todo con Minecraft.
- Voz madura clonada y música de C418 (reglas de la línea y del 2026-10-25).
- **Primero el código; la voz y el render en otro momento** (2026-10-28).

### Decisiones de Claude (Aldo puede cambiarlas)

- Las vagonetas con cofre como paquetes y las estaciones con cartógrafo como routers (el cartógrafo es el aldeano de los mapas).
- El cuadro `bust` del juego como la foto: es de 2 × 2, así que cada paquete es exactamente un bloque del cuadro.
- **Lugar:** `birch-terraces` (era el candidato `mac-13` de MacEntorno: abedules sobre terrazas de tierra), con turn 0.7854 y un lote aplanado de `[-38, 30, -44, 34]` para la red. Es el primer short de tecnología en bosque de abedules; DNS y HTTPS son llanuras. Las texturas de sus bloques se copian del jar (comando de "Problemas conocidos" en `GUIA.md`).
- **Red:** Steve en (0, 22) y Alex en (0, −34). Camino corto por R (72 bloques, 3 routers) y camino largo por L y LB (92 bloques, 4 routers). Un lazo L → W1 → W2 → LB → L para el TTL y dos entradas de tráfico ajeno (este y oeste).
- De día, con ovejas, gallinas, vacas y un lobo fuera de la red.
- Música: Subwoofer Lullaby (el video dura menos de 209 s).
- Loop como en DNS y HTTPS.

### Piezas nuevas

- `herramientas/temas/minecraft-original/rieles.js`:
  - `makeTracks(imgs, polilíneas)`: rieles del juego en cada bloque (rectos, curvas giradas según sus vecinos y cruces).
  - `makeMinecart(imgs, {chest})`: el modelo `MinecartModel` del juego (textura de 64 × 32), con o sin cofre; `place(ruta, d)`.
  - `makeStation(imgs, {label})`: el puesto del router.
  - `along`, `pathLength`, `distancesTo`, `distanceAt(keys, t)` y `timeAt`: una vagoneta avanza por llaves `[tiempo, distancia]`, y dos llaves con la misma distancia son una espera en la fila.
- `gente.js`: `entityPart` (antes `part`, ahora acepta el tamaño de la textura) y `skinMat` exportados para otros modelos del juego.
- `extraer.py`: `rail`, `rail_corner`, `minecart` (entidad), `painting_bust` y `painting_back`; sonidos `minecart_roll`, `fizz`, `painting_place`, `frame_add` y `bell`.

## Forma de trabajo y revisiones (cuando se haga la voz y el render)

Lo mismo que en DNS (`videos/tech/dns/DISENO.md`, "Forma de trabajo y revisiones"): cuadros fijos de cada escena antes del render completo, voz revisada línea por línea, la lista de errores de `GUIA.md`, duración del video igual a la del audio, música, loop y verlo en movimiento. Sin commit ni push hasta que Aldo lo pida, y sin firma de IA.

## Siguiente tema

Aldo pidió para después de este: **cómo funciona el backend, qué es Kafka y cómo funciona** (2026-10-28). Hay también un diseño de "How SQL works" en `videos/tech/sql/DISENO.md`, de otra sesión, pendiente de aprobación.
