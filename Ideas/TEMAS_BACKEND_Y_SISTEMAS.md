# Ideas de Videos: Backend, Redes y Diseño de Sistemas

Banco de temas para la línea `videos/tech/` de LeetSolve. Ordenados desde fundamentos de una petición hasta arquitectura distribuida y casos reales.

---

## 1. Fundamentos del Backend (El viaje de una petición)

1. **Qué hace un servidor por dentro (Request → Response y APIs REST)**
   - **Concepto:** Llega un pedido (`GET`/`POST`), pasa por el cadenero (middleware), el cocinero (controlador/lógica de negocio) procesa y devuelve JSON con un código de estado (`200`, `400`, `404`, `500`).
2. **Autenticación y Sesiones (Cookies vs JWT)**
   - **Concepto:** HTTP no tiene memoria. Cómo recuerda el servidor quién eres: anotar tu sesión en una libreta del servidor (Cookie + Session ID) vs entregarte un gafete firmado criptográficamente (JWT) que el servidor solo verifica sin consultar base de datos.
3. **Bases de Datos, Transacciones (ACID) e Índices**
   - **Concepto:** Dónde viven los datos. Qué pasa si dos personas compran el último boleto al mismo tiempo (locks y atomicidad) y cómo un índice evita leer toda la tabla fila por fila.
4. **Caché en Memoria (Redis / Memcached)**
   - **Concepto:** No bajar a la bodega (disco/SQL) por el dato que piden mil veces por segundo; dejarlo en el mostrador (RAM), manejar su caducidad (TTL) y qué pasa cuando el dato cambia (invalidación de caché, Cache-Aside vs Write-Through).
5. **Balanceador de Carga (Load Balancer) y Escalado Horizontal**
   - **Concepto:** Vertical (comprar un servidor más grande) vs Horizontal (poner muchos servidores iguales). Cómo el recepcionista reparte el tráfico (Round Robin, Least Connections, Health Checks).
6. **Colas de Mensajes y Eventos (RabbitMQ vs Kafka)**
   - **Concepto:** Desacoplar trabajo pesado. En vez de dejar esperando al usuario, metes el pedido en una banda transportadora (cola o log de eventos con particiones y grupos de consumidores) para procesarlo asíncronamente.
7. **Comunicación en Tiempo Real (Polling vs Long Polling vs SSE vs WebSockets)**
   - **Concepto:** Dejar de preguntar *"¿ya hay mensajes nuevos?"* cada segundo y abrir un túnel bidireccional permanente para chats, notificaciones o juegos.
8. **Rate Limiting (Protección contra abuso y picos)**
   - **Concepto:** El límite de peticiones por minuto para que un bot no tire el servidor. Algoritmos visuales: *Token Bucket* (cubeta de fichas que se recarga), *Leaky Bucket* (embudo con salida constante) y *Sliding Window*.

---

## 2. Datos y Almacenamiento a Fondo

9. **Sharding y Particionamiento de Bases de Datos**
   - **Concepto:** Cuando una tabla ya no cabe en un solo servidor y la partes en fragmentos (por rango, por hash de usuario o por zona geográfica), y el problema de los *hotspots* (el famoso al que todos consultan).
10. **Replicación (Leader-Follower) y Teorema CAP (Consistencia Eventual)**
    - **Concepto:** Un servidor maestro recibe escrituras y las copia a réplicas de lectura. Por qué a veces publicas un comentario, refrescas y todavía no sale en otra réplica (*replication lag*).
11. **B-Trees vs LSM-Trees (Cómo guardan datos las bases de datos en disco)**
    - **Concepto:** Por qué Postgres/MySQL usan árboles balanceados de páginas (B+Tree, rápido para leer) mientras Cassandra/RocksDB escriben todo de corrido en un cuaderno y luego compactan (LSM-Tree + SSTables, brutal para escrituras masivas).
12. **Write-Ahead Log (WAL): Cómo no pierde datos una base de datos si se va la luz**
    - **Concepto:** Antes de modificar cualquier tabla en disco, la base de datos anota la operación en una bitácora secuencial (append-only). Si el servidor se apaga a mitad de operación, al prender lee el diario y reconstruye todo.
13. **Deadlocks y Race Conditions (Concurrencia en el Servidor)**
    - **Concepto:** Dos procesos esperando el candado que tiene el otro (abrazo mortal), o dos hilos leyendo el mismo saldo bancario antes de restar (cobro perdido). Locks pesimistas vs optimistas (versionado).
14. **Blob Storage vs Base de Datos (S3 y Presigned URLs)**
    - **Concepto:** Por qué guardar fotos o videos dentro de SQL arruina el rendimiento, y cómo el backend le entrega al cliente un "pase temporal firmado" para que suba el archivo directo a la bodega (S3/CDN) sin saturar tu servidor.

---

## 3. Arquitectura y Sistemas Distribuidos

15. **Monolito vs Microservicios**
    - **Concepto:** Un solo taller donde todos trabajan bajo el mismo techo vs 20 talleres separados que se mandan mensajeros por la calle. Ventajas de escalar por separado vs el costo oculto de la red.
16. **Idempotencia (Cómo evitar cobrar dos veces una tarjeta)**
    - **Concepto:** Qué pasa si el usuario aprieta "Pagar" tres veces porque su internet se trabó. Cómo una `Idempotency-Key` hace que repetir la misma petición 10 veces produzca el efecto una sola vez.
17. **Transacciones Distribuidas (Patrón Saga vs Two-Phase Commit)**
    - **Concepto:** Reservar vuelo, hotel y cobrar tarjeta cuando cada uno vive en un servidor distinto. Si falla el hotel, cómo ejecutas pasos de compensación en reversa para cancelar todo limpiamente.
18. **Circuit Breaker, Retries con Exponential Backoff y Backpressure**
    - **Concepto:** Si un servidor externo empieza a fallar, reintentar al instante entre miles de clientes lo remata (*thundering herd*). Cómo esperar cada vez más tiempo (backoff + jitter) y abrir el "fusible" (Circuit Breaker) para evitar fallos en cascada.
19. **Consenso Distribuido (Algoritmo Raft)**
    - **Concepto:** Si tienes 5 servidores y el jefe se apaga, ¿cómo votan entre ellos para elegir un nuevo líder sin que queden dos jefes dando órdenes contradictorias (*split-brain*)?

---

## 4. Red, Protocolos y Ejecución Interna

20. **Reverse Proxy vs Load Balancer vs API Gateway (Nginx / Envoy)**
    - **Concepto:** El proxy normal esconde al cliente; el *Reverse Proxy* esconde a tus servidores detrás de una sola fachada que maneja SSL, compresión, caché y ruteo.
21. **REST vs GraphQL vs gRPC (Protobuf)**
    - **Concepto:** Pedir el combo fijo en texto (REST, a veces te sobra o falta comida), pedir a la carta exactamente los campos que ocupas (GraphQL) o hablar en binario compacto entre microservicios (gRPC).
22. **Connection Pooling (Por qué abrir conexiones nuevas mata tu base de datos)**
    - **Concepto:** Abrir una conexión TCP + TLS + autenticación con Postgres toma mucho tiempo y memoria. Cómo una "alberca" mantiene 20 conexiones ya abiertas y las presta por milisegundos a miles de peticiones.
23. **Event Loop (Node.js / Async I/O) vs Multi-threading**
    - **Concepto:** Un restaurante con 100 meseros que se quedan parados frente a la cocina esperando cada plato (hilos bloqueantes) vs un solo mesero velocísimo que toma la orden, la deja en ventanilla y sigue atendiendo mesas hasta que suena la campana (Event Loop).
24. **CDN (Content Delivery Network) y Edge Computing**
    - **Concepto:** En lugar de que todos viajen hasta tu servidor central en Virginia, copias las imágenes, videos y hasta pequeñas funciones en sucursales pegadas a cada ciudad.
25. **NAT y Puertos (Cómo 20 dispositivos en casa salen con 1 sola IP)**
    - **Concepto:** El router como recepcionista de edificio que traduce direcciones privadas (`192.168.x.x`) a una sola dirección pública usando números de puerto para recordar a quién iba cada respuesta.
26. **TCP vs UDP vs QUIC (HTTP/3)**
    - **Concepto:** TCP numera, ordena y pide acuse de recibo (pero si se pierde el paquete 1, frena los demás: *head-of-line blocking*). UDP dispara sin preguntar (juegos/voz). QUIC mete canales independientes sobre UDP para no frenar todo por un paquete perdido.

---

## 5. Estructuras y Algoritmos Reales que Mueven el Backend

27. **Consistent Hashing (El anillo que salva tu caché)**
    - **Concepto:** Si repartes datos con `hash(key) % N` y se cae 1 de tus 4 servidores (`N=3`), casi todas las llaves cambian de lugar y tu base de datos muere. Cómo doblar la línea en un círculo con nodos virtuales hace que solo se mueva `1/N` de los datos.
28. **Bloom Filters (Cómo saber al instante si algo NO existe)**
    - **Concepto:** Cómo verifica un servidor si un nombre de usuario ya está ocupado o si una llave no está en disco sin buscar en millones de registros: un arreglo de bits y varias funciones hash que nunca dan falsos negativos.
29. **Índice Invertido (Cómo buscan Google y Elasticsearch en milisegundos)**
    - **Concepto:** Por qué `SELECT * FROM posts WHERE texto LIKE '%minecraft%'` lee toda la base de datos, y cómo armar el glosario al revés (palabra → lista de documentos donde aparece + tokenización) hace la búsqueda instantánea.
30. **Generadores de IDs Distribuidos (UUID vs Auto-Increment vs Snowflake ID)**
    - **Concepto:** En 50 servidores no puedes usar `1, 2, 3...` sin chocar, y un UUID aleatorio desordena los índices B-Tree. Cómo el **Snowflake ID** (usado por Twitter/Discord) mete en 64 bits el milisegundo exacto, el ID de la máquina y un contador para que sean únicos y ordenables por tiempo.

---

## 6. Seguridad e Infraestructura en Producción

31. **Hashing de Contraseñas (Salt + Pepper + Bcrypt/Argon2)**
    - **Concepto:** Por qué cifrar no es igual a hashear, cómo un atacante usa tablas precalculadas (*Rainbow Tables*) si dos usuarios tienen la misma contraseña, y cómo agregar una pizca de "sal" aleatoria única por usuario rompe el ataque.
32. **OAuth 2.0 ("Iniciar sesión con Google" sin dar tu contraseña)**
    - **Concepto:** El flujo de autorización explicado como una llave de *valet parking*: Google te autentica a ti y le da a la aplicación un boleto limitado (Access Token) que abre la puerta pero no la cajuela.
33. **SQL Injection y Prepared Statements**
    - **Concepto:** Cómo concatenar texto de un usuario dentro de una consulta permite que escriba `' OR 1=1 --` y se salte el login, y cómo los parámetros compilados separan la estructura de la orden de los datos.
34. **CORS (Por qué el navegador bloquea tu API y la terminal no)**
    - **Concepto:** El navegador como policía que impide que una página maliciosa use tus cookies para pedir datos a tu banco, y qué es la petición *preflight* (`OPTIONS`).
35. **Contenedores (Docker) vs Máquinas Virtuales**
    - **Concepto:** Levantar una casa entera con sus propios cimientos y tuberías para cada inquilino (VM con su propio sistema operativo) vs departamentos ligeros aislados que comparten el mismo edificio (namespaces y cgroups del kernel).
36. **Zero-Downtime Deployments (Blue-Green, Canary y Rolling Updates)**
    - **Concepto:** Cómo actualizas la versión de un servidor en producción a las 3 de la tarde sin desconectar a los usuarios activos.
37. **Observabilidad: Logs, Métricas y Distributed Tracing**
    - **Concepto:** Cuando una compra tarda 8 segundos y pasa por 12 microservicios, cómo un sello de rastreo (`Trace-ID`) te dibuja la línea del tiempo exacta de dónde estuvo el cuello de botella.

---

## 7. Casos Reales ("¿Cómo funciona X por dentro?")

En vez de presentar el tema en abstracto (*"Qué es un Distributed Lock"*), el gancho es un problema real que todos han vivido y por dentro enseña la pieza de backend con una metáfora en Minecraft:

38. **Ticketmaster / Conciertos: ¿Cómo evitan vender el mismo asiento dos veces?**
    - **Backend que enseña:** *Race Conditions*, Cola de espera (*Virtual Waiting Room*) y *Distributed Locks con TTL* en Redis.
    - **Metáfora Minecraft:** Dos jugadores corren al mismo cofre por el último boleto; el guardia pone un candado con reloj de arena (TTL de 5 min) mientras uno busca sus esmeraldas. Si no paga a tiempo, el candado explota y pasa el siguiente.
39. **Uber / Didi: ¿Cómo encuentra al chofer más cercano en milisegundos?**
    - **Backend que enseña:** Índices espaciales (*Geohash / Cuadrículas / Uber H3*) vs fuerza bruta $O(N)$.
    - **Metáfora Minecraft:** En vez de medir con cinta métrica la distancia a cada caballo de todo el mundo, el mapa se divide en parcelas con código; solo revisas tu parcela y las vecinas.
40. **Netflix / YouTube: ¿Cómo reproduce video sin trabarse aunque baje tu internet?**
    - **Backend que enseña:** *Chunking*, *Adaptive Bitrate Streaming (HLS/DASH)* y *CDN* en el borde.
    - **Metáfora Minecraft:** La película no viaja como un bloque gigante, sino como una fila de vagonetas de 2 segundos en 3 tamaños (diamante 4K, oro 1080p, madera 360p). Si el riel se estrecha, el servidor cambia al instante a vagonetas de madera sin detener el tren.
41. **Bancos / Stripe: ¿Cómo mueven dinero sin perder ni inventar un centavo aunque se caiga el servidor?**
    - **Backend que enseña:** *ACID*, *Idempotency Key* (no cobrar doble al apretar dos veces) y *Double-Entry Ledger* (contabilidad inmutable).
    - **Metáfora Minecraft:** El banquero jamás borra ni sobrescribe el cofre; tiene un libro donde apunta con pluma `-10 esmeraldas a Steve` y `+10 a Alex` bajo un sello único. Si Steve manda la misma carta dos veces por error, el banquero ve el sello repetido y no vuelve a cobrar.
42. **Discord / WhatsApp: ¿Cómo mandan un mensaje a 100,000 personas al mismo tiempo?**
    - **Backend que enseña:** *WebSockets*, *Pub/Sub* y el problema del *Fan-out* (Push vs Pull).
    - **Metáfora Minecraft:** En un pueblo de 5 casas, el cartero corre a dejar copia en cada buzón (*Push*). En una ciudad de 100,000 aldeanos, el cartero moriría; mejor clava el aviso en un pizarrón central y cada quien lo lee cuando se acerca (*Pull*).
43. **Spotify / Shazam: ¿Cómo identifica una canción en 3 segundos entre 100 millones?**
    - **Backend que enseña:** *Audio Fingerprinting* (espectrograma de picos) y búsqueda por *Hash Table* en $O(1)$.
    - **Metáfora Minecraft:** En vez de comparar toda la canción nota por nota, toma solo las estrellas más brillantes (picos de frecuencia), arma una constelación con la distancia entre ellas y busca ese código numérico directo en un índice.
44. **Google Docs / Figma: ¿Cómo escriben 10 personas en el mismo párrafo sin pisarse?**
    - **Backend que enseña:** *Operational Transformation (OT)* y *CRDTs* (estructuras libres de conflicto sin bloquear el documento).
    - **Metáfora Minecraft:** Dos constructores poniendo bloques en la misma pared al mismo tiempo sin usar candados; cada bloque lleva el reloj e identificador de quién lo puso para que ambos mundos converjan exactos.
45. **Amazon / MercadoLibre: ¿Cómo sabe cuántas piezas quedan cuando hay 50 bodegas y miles de compras por segundo?**
    - **Backend que enseña:** *Event-Driven Architecture (Kafka)*, *Inventario reservado vs físico* y *Patrón Saga*.
    - **Metáfora Minecraft:** El mostrador descuenta al vuelo de una pizarra rápida, mientras por detrás sale una vagoneta (evento en Kafka) hacia la bodega real, el cobrador y el repartidor.
46. **Instagram / TikTok: ¿Cómo se arma tu feed en menos de 200 ms cuando entras a la app?**
    - **Backend que enseña:** *Pre-cálculo en Caché (Timeline en Redis)*, *Híbrido Push/Pull* (el problema de la celebridad con 50 millones de seguidores).
    - **Metáfora Minecraft:** Tu bandeja de entrada ya está armada en el mostrador antes de que llegues, excepto los posts del "Rey del servidor", que se mezclan al momento de abrirla para no saturar millones de buzones cada vez que él publica.
47. **Google Search / Autocompletado: ¿Cómo adivina lo que vas a escribir en cada tecla?**
    - **Backend que enseña:** Árbol de prefijos (*Trie*), caché de los *Top-K* más buscados en cada nodo y *Debounce* en el cliente.
    - **Metáfora Minecraft:** Un camino de letreros que se bifurca letra por letra (`M` → `I` → `N`...); en cada cruce ya está colgado un cartel con las 3 palabras más famosas que empiezan por ahí para no recorrer todo el bosque.
48. **Cloudflare / Escudo Anti-DDoS: ¿Cómo distingue a 1 millón de bots de usuarios reales sin caerse?**
    - **Backend que enseña:** *Anycast DNS*, *Reverse Proxy*, *Rate Limiting (Token Bucket)* y retos de trabajo.
    - **Metáfora Minecraft:** En vez de que la horda de zombies llegue al castillo central, hay murallas repartidas por todo el mapa que absorben el golpe cerca de donde nacen y solo dejan pasar por el puente a quienes tienen ficha.
49. **GitHub / Git: ¿Cómo guarda 10,000 versiones de tu código sin llenar el disco de copias repetidas?**
    - **Backend que enseña:** *Content-Addressable Storage*, hashes *SHA* y grafos acíclicos dirigidos (*DAG* / árboles de Merkle).
    - **Metáfora Minecraft:** No toma una foto nueva de toda la aldea cada día; solo guarda en un cofre las casas que cambiaron identificadas por su huella digital y apunta con flechas a las casas viejas que siguen igual.

