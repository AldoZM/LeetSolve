# Diseño: short "How SQL works", todo en 3D

Estado: aprobado por Aldo el 2026-10-28 ("Chi"), con la narración, los nombres de las filas y la música propuestos. El código está escrito (2026-10-28, laptop); **la voz y el render quedan para otra sesión** por orden de Aldo. Ver "Estado del código" al final.

## Intención

Tercer short de la línea "cómo funcionan las tecnologías" (después de DNS y HTTPS/TLS), y el primero de **backend**. Aldo pidió enfocarse en el backend y no en redes: aquí no aparecen paquetes, servidores ni caminos entre aldeas, solo **la base de datos y el lenguaje con que se le habla**.

Aldo eligió **un solo short** (opción A) con la misma forma que el de DNS: cómo funciona y luego tres usos reales (índice, transacción e inyección SQL).

## Metas

- Un short vertical (1080 × 1920, 30 fps) de **menos de 3 minutos** que explique qué es una tabla, qué es una consulta, en qué orden la ejecuta la base de datos y tres cosas que pasan en la vida real.
- Todo dentro del mundo 3D: textos en letreros, libros, globos de tooltip y objetos. Nada de capas 2D encima.
- Que alguien que nunca escribió SQL entienda la consulta del ejemplo solo con ver la bodega.
- Dejar la **bodega** reutilizable para los videos de la sección Database de LeetCode (#175, #176, #182…).

## Fuera del alcance

- JOIN, GROUP BY, INSERT/UPDATE/DELETE, NoSQL, ORMs: quedan para otro short si este funciona.
- Servidores, APIs y redes.
- Escenas de Manim, código en pantalla fuera del mundo y subtítulos quemados.
- Publicar, hacer commit o push: lo decide Aldo.

## No debe pasar (aunque técnicamente funcione)

- Que la narración diga algo falso o exagerado de SQL (ver "Exactitud").
- Que se vea como un video 2D con fondo 3D.
- Texto ilegible en el celular. La consulta es el texto más largo: va partida en renglones, uno por cláusula.
- Caracteres que la fuente del juego no tiene (`→`, `≠`, `✓`, `³`). `>`, `=`, `'` y `-` sí existen; verificarlo en la hoja de cuadros.
- Logos de marcas o el de Minecraft.

## La metáfora

- **Base de datos** = una bodega bajo la aldea (sótano de piedra con antorchas).
- **Tabla** = un estante largo con letrero `players`. Arriba de cada columna, un letrero: `name`, `emeralds`, `village`.
- **Fila (registro)** = un renglón del estante: la cabeza del jugador, su nombre en un letrero, un marco con esmeraldas y el número, y un estandarte o bloque de su aldea.
- **Consulta** = un libro y pluma con la orden escrita, un renglón por cláusula.
- **Motor de la base de datos** = el aldeano bibliotecario de la bodega: lee el libro y hace el trabajo. Es el mismo modelo de los shorts de DNS y HTTPS.
- **Resultado** = una tabla nueva, más chica, que el bibliotecario arma en un cofre o estante aparte.
- **Índice** = un árbol de letreros ordenados (B-tree) que apunta a las filas.
- **Transacción** = una caja con dos pasos que se confirma completa o se deshace completa.
- **Inyección SQL** = el texto del jugador escrito directo en el libro de la orden.

## Narración (borrador, en inglés)

Unas 380 palabras, ~130 s con la voz clonada (~2.9 palabras por segundo). No se estira para llenar 3 minutos. En `narration.txt` las siglas se escriben como se dicen (`S Q L`, `one equals one`).

```
0  Every app you use keeps its data somewhere. Your account, your orders, your messages.
1  Much of it lives in a database, and you talk to it with a language called SQL.
2  Picture a storage room. A table is a long shelf. Each column has a sign: name, emeralds, village.
3  Each row is one record. Steve, Alex, and every other player.
4  To get data, you write a query, like a note for the librarian: select the names of players with more than ten emeralds.
5  The database reads it, but not in the order you wrote it.
6  First, FROM: find the right shelf. Then WHERE: walk the rows and keep only the ones that match.
7  Then SELECT keeps just the columns you asked for. ORDER BY sorts them, and LIMIT cuts the list.
8  The answer comes back as a new, smaller table.
9  You say what you want, not how to find it. The database decides the how, and that's where the tricks are.
10 First, speed. With a million players, checking every row takes forever. That's a full scan.
11 An index is a sorted guide, built like a tree. Each sign tells the librarian which way to go.
12 A few jumps, and he's at the right row out of a million.
13 Second, safety. Steve pays Alex five emeralds: take five from Steve, give five to Alex.
14 But a creeper blows up the room right in the middle. Steve lost his emeralds, and Alex got nothing.
15 A transaction fixes that. Both steps happen, or neither does. If anything fails, it all rolls back.
16 Third, the dangerous one: SQL injection. A bad login form pastes your text straight into the query.
17 So someone types a quote, then OR one equals one, and two dashes to hide the rest. Now the check is always true.
18 The fix: never paste text into a query. Send it as a value in its own slot, so it can never become a command.
19 So every time an app remembers you, a librarian is reading a note and walking down a shelf.
20 That's SQL.
```

La consulta que se ve en el libro (líneas 4 a 8):

```sql
SELECT name
FROM players
WHERE emeralds > 10
ORDER BY emeralds DESC
LIMIT 3
```

La consulta de la inyección (líneas 16 a 18), escrita en el libro con el texto de Steve en otro color:

```sql
SELECT * FROM users
WHERE name = '' OR 1=1 --' AND password = '...'
```

### Exactitud (revisar antes de generar la voz)

- **Orden de ejecución:** es el orden **lógico** del estándar (FROM, JOIN, WHERE, GROUP BY, HAVING, SELECT, DISTINCT, ORDER BY, LIMIT). El optimizador puede ejecutarlo físicamente de otra manera, pero el resultado es como si siguiera ese orden. La narración dice "not in the order you wrote it", que es cierto en ese sentido. No decir que la base de datos "siempre" lo hace paso por paso así.
- **Línea 9:** SQL es declarativo; el planificador elige cómo (escaneo completo o índice). Cierto.
- **Índice:** los índices comunes (B-tree) guardan las claves ordenadas en un árbol balanceado de pocos niveles: con un millón de filas son unos 3 o 4 saltos. Cada nodo tiene **muchas** claves, no dos: dibujar nodos anchos con varios letreros, no un árbol binario. El índice ayuda cuando se busca por la columna indexada (aquí `emeralds` o `name`). No mencionar el costo en escrituras (fuera del alcance), pero no decir que un índice "siempre" acelera todo.
- **Transacción:** atomicidad (la A de ACID). Si algo falla a la mitad (error, caída del servidor), la base de datos deshace los pasos incompletos. El creeper representa la falla. Sin transacción, cada paso se guarda por separado y puede quedar a medias, como dice la línea 14.
- **Inyección:** con `' OR 1=1 --` la condición queda siempre verdadera y `--` comenta el resto (la revisión de la contraseña). Pasa solo cuando el programa **pega** el texto en la consulta. El arreglo real son las **consultas parametrizadas**: el valor viaja aparte y la base de datos nunca lo interpreta como SQL. La línea 16 dice "a bad login form": no afirmar que todos los formularios son vulnerables.
- Los datos del ejemplo deben dar el resultado que se ve: con `LIMIT 3` y `DESC`, el cofre de resultado tiene los 3 nombres con más esmeraldas (mayores a 10), en ese orden.

## Datos del ejemplo (tabla `players`)

Seis filas, para que quepan en el cuadro vertical:

| name | emeralds | village |
|---|---|---|
| Steve | 12 | plains |
| Alex | 30 | desert |
| Noor | 4 | taiga |
| Kai | 18 | plains |
| Zuri | 9 | savanna |
| Ren | 25 | snowy |

`WHERE emeralds > 10` deja Steve 12, Alex 30, Kai 18 y Ren 25. `ORDER BY emeralds DESC` da Alex, Ren, Kai, Steve. `LIMIT 3` deja **Alex, Ren, Kai**. Los nombres son inventados (sin personas reales) salvo Steve y Alex, que son los skins del juego; las demás filas pueden usar skins de aldeano o cabezas de mobs si no hay más skins de jugador.

## Escenas (qué se ve en cada parte)

1. **Gancho (0 y 1):** la aldea de día. Steve abre un cofre en su casa; la cámara baja por una escalera de piedra a la bodega. Letrero grande "HOW SQL WORKS".
2. **La tabla (2 y 3):** el estante `players` con los letreros de columna. Cada fila se enciende cuando la voz la nombra (Steve, Alex, el resto juntos).
3. **La consulta (4 y 5):** Steve le da al bibliotecario un libro y pluma; la cámara lo lee de cerca, con la consulta en 5 renglones. En la línea 5 los renglones del libro **se reordenan** (FROM sube al primer lugar).
4. **Ejecución (6 a 8), un renglón del libro brilla a la vez:**
   - FROM: el bibliotecario camina al estante `players`.
   - WHERE: recorre las filas; las de 10 o menos se apagan (Noor, Zuri) y las demás brillan.
   - SELECT: de las filas que brillan solo vuela el letrero del nombre; las otras columnas se quedan.
   - ORDER BY: los letreros se acomodan por esmeraldas, de mayor a menor.
   - LIMIT: el cuarto (Steve) cae; quedan Alex, Ren y Kai en el estante de resultado.
5. **Declarativo (9):** toma abierta de la bodega; el bibliotecario guarda el libro.
6. **Índice (10 a 12):** la cámara se aleja y el estante se alarga hasta perderse (muchas filas, instanciadas). Primero el bibliotecario camina fila por fila con cámara acelerada y un reloj del juego girando (full scan). Después aparece el árbol de letreros: raíz arriba, nodos anchos con rangos ("1-500K", "500K-1M"), y el bibliotecario baja 3 saltos en vagoneta hasta la fila exacta. Se puede usar `rieles.js` si la otra sesión lo termina.
7. **Transacción (13 a 15):** dos cofres, "Steve" y "Alex". Salen 5 esmeraldas del de Steve; antes de llegar al de Alex, un creeper silba y explota. Las esmeraldas desaparecen. Se repite dentro de un marco (la transacción): el creeper explota igual, pero las esmeraldas **regresan** volando al cofre de Steve (ROLLBACK). Tercera vez sin creeper: llegan y el marco se sella con brillo (COMMIT).
8. **Inyección SQL (16 a 18):** un letrero de login en la puerta de la bóveda con dos casillas, `name` y `password`. Steve escribe `' OR 1=1 --`; el texto entra al libro de la orden en rojo, el resto se tacha y todos los cofres de la bóveda se abren. Arreglo: el libro tiene una casilla aparte (un marco de objeto) donde va el texto de Steve como objeto, no como renglón; el bibliotecario busca a alguien llamado literalmente `' OR 1=1 --`, no lo encuentra y la puerta sigue cerrada (el "no" del aldeano).
9. **Cierre (19 y 20):** repaso rápido (libro, estante, árbol, marco sellado) y la cámara vuelve a la toma de la portada. Loop.

## Cómo se hace

### Decisiones de Aldo

- Un solo short (opción A), enfocado en backend, con SQL como tema.
- Mismas reglas que los shorts de DNS y HTTPS: vertical, menos de 3 minutos, todo en 3D, todo con Minecraft, voz madura clonada (Qwen3-TTS), música de C418 obligatoria, loop.

### Decisiones de Claude (Aldo puede cambiarlas)

- Contenido: tabla + consulta + orden de ejecución, y luego índice, transacción e inyección.
- La consulta del ejemplo y los datos de la tabla de arriba.
- Lugar nuevo de `mundos/lugares.json` que ningún video use; casi todo pasa en la bodega (interior hecho por código), así que solo la portada y el cierre necesitan el exterior.
- Música: Subwoofer Lullaby (la favorita de Aldo), o otra pista de C418 si Aldo quiere variar entre shorts.
- Carpeta: `videos/tech/sql/`.

### Piezas que hay que construir

1. **Bodega** en `aldea.js` o en la página del video: sótano de piedra, estante-tabla con letreros de columna, filas con cabeza, letrero, marco y estandarte. Debe servir después para los videos de Database de LeetCode.
2. **Libro de consulta** legible a 1080 px de ancho: renglones que se reordenan, brillan y cambian de color.
3. **Árbol de índice** con nodos anchos de letreros y el camino de bajada.
4. **Creeper** (modelo y animación de hincharse) y la explosión; las esmeraldas que vuelan y regresan.
5. **Letrero de login** y la puerta de la bóveda.
6. Reutiliza `gente.js` (Steve, Alex, bibliotecario), el modo `solo3d` de `build.py` y el paso de voz sin Manim de los shorts de DNS y HTTPS.

## Forma de trabajo y revisiones

1. Cuadros fijos de cada escena (`render.mjs --stills`) en una hoja 9:16 para que Aldo los vea antes del render completo.
2. La voz se revisa línea por línea (duración, `silencedetect` y, si se puede, transcripción contra el guion). Cuidar cómo pronuncia `S Q L`, `one equals one` y `ORDER BY`.
3. Revisar "Errores ya cometidos (no repetir)" de `GUIA.md`.
4. Antes de entregar: duración del video igual a la del audio, música presente, loop (diferencia media menor a 1) y verlo en movimiento.
5. Al terminar: entrada en `BITACORA.md`, el lugar en `mundos/lugares.json`, `descripcion.txt` (100 caracteres o menos) y el video abierto en Edge para Aldo. Sin commit ni push hasta que Aldo lo pida.

## Restricciones

- Otra sesión trabaja en LeetSolve al mismo tiempo (hoy tiene cambios en `gente.js`, `extraer.py` y el archivo nuevo `rieles.js`). Revisar `git status` antes de editar archivos compartidos y no tocar los suyos sin coordinar.
- Nunca subir archivos de Mojang.
- Entorno de Windows: `export PATH="$HOME/.manim-skill-src/.venv/Scripts:$PATH" PYTHONUTF8=1`; `python`, no `python3`.
- Código en inglés con comentarios breves; documentos en español.
- Al publicar: "Not an official Minecraft product" y los créditos de la música de C418.

## Estado del código (2026-10-28, laptop)

Hecho, sin render ni voz (Aldo pidió solo el código):

- `narration.txt` (21 líneas, 349 palabras, unos 125 s), `video.json` (solo3d, 9:16, Subwoofer Lullaby) y `descripcion.txt` (91 caracteres).
- `three/sql.html`: toda la página. Revisado con `node --check` y la lógica del índice simulada en Node (26 hojas sin choques, la ruta de Ren va sobre los rieles, 3 saltos). El resultado de la consulta del ejemplo se comprobó en Python (Alex, Ren, Kai).
- `three/timestamps.json`: **provisional** (palabras / 2.9 por segundo) para poder ver la página antes de tener voz. **Borrarlo antes del render final.**
- `.tts-cache/` tiene la primera línea con la voz clonada (se detuvo la generación por orden de Aldo).

Cambios respecto a lo de arriba, al construir:

- **La bodega no es un sótano:** es una sala de piedra sin techo y con el frente abierto, sobre el lote. En 9:16 la tabla completa (3 columnas) solo cabe con la cámara a ~18 bloques, más de lo que mide una sala cerrada. Los costados llevan libreros.
- **El estante de resultado** está a la izquierda, girado hacia la cámara; la cámara pasa de la tabla al estante en SELECT.
- **La consulta** son 5 globos (uno por cláusula) que flotan sobre el bibliotecario y lo siguen; la cláusula que corre se pinta de amarillo.
- **El millón de filas** es una pared de 61 × 40 cajones detrás de la sala, y el índice es un árbol de rieles en el piso: raíz, 3 ramas (A-I, J-R, S-Z), 3 bajo cada una y una vía por letra hasta su cajón. Letreros en cada rama. El bibliotecario baja en vagoneta (`rieles.js`).
- **Transacción:** sin la tercera vuelta con COMMIT. Primero el pago sin transacción (las esmeraldas se pierden) y luego dentro del marco de la transacción: explota otra vez y las esmeraldas regresan (ROLLBACK). La narración solo pide eso.
- **Inyección:** el que escribe es el illager ilusionista (como el impostor de DNS) y la bóveda es de hierro con 5 cofres.
- El creeper se arma en la página con `entityPart` y `skinMat` de `gente.js` y la textura `mobs/creeper.png` (`vida.js` no exporta sus modelos).

Falta, para la sesión del render:

1. En la PC que renderice: `extraer.py 26.3` (en esta laptop faltan `gente/` y casi todas las texturas de los shorts de tecnología) y las texturas del lugar.
2. **Lugar:** la página usa `mac-02` (arena con abedules, MacEntorno) como prueba. Revisar con `--stills`; al elegir, renombrarlo y anotarlo en `mundos/lugares.json` (no se tocó porque otra sesión lo estaba editando).
3. Voz: `tts_qwen_clone.py videos/tech/sql` (reanuda desde la caché) y revisión línea por línea.
4. Cuadros fijos de cada escena (`render.mjs --stills`) y ajuste de cámaras. Las poses de cámara están calculadas a mano, sin verlas: lo más probable es que haya que moverlas.
5. Borrar `three/timestamps.json`, render completo, loop y la lista de revisión.

Dependencias sin commit de otra sesión: `rieles.js` y los cambios de `gente.js` (`entityPart` y `skinMat` exportados) y de `extraer.py` (rieles, vagoneta, sonido `minecart_roll`). Si esa sesión cambia esas funciones, revisar esta página.

## Estado (2026-10-29, PC de Windows)

- Lugar: se queda `mac-02` (sin renombrar todavía; al terminar, renombrarlo y anotarlo en `lugares.json` junto con el servidor, que usa el mismo).
- Cuadros revisados y cámaras corregidas; voz lista (21 líneas, 115.1 s, revisada con Whisper); `three/timestamps.json` provisional borrado.
- El render quedó corriendo al cerrar la sesión. Falta: confirmar `video.mp4`, loop, hoja de cuadros, renombrar a `How SQL Works.mp4`, copiarlo a `export/`, su bloque en `export/descripciones-tecnologia.md`, "Videos hechos" de `GUIA.md`.
