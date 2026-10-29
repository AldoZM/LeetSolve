# Ideas de Videos: SQL y Bases de Datos Relacionales

Diseñadas para reutilizar el escenario 3D de la **bodega subterránea con el bibliotecario y los estantes** de `videos/tech/sql/DISENO.md` (donde el primer short ya cubrió `SELECT/FROM/WHERE/ORDER BY/LIMIT`, vistazo a Índice, Transacción y SQL Injection).

---

## 1. Conceptos Clave de SQL (Secuelas directas en la Bodega)

1. **Cómo funcionan los JOINs de verdad (`INNER`, `LEFT`, `RIGHT`, `FULL`, `CROSS`)**
   - **Gancho:** Por qué guardar todo en una sola tabla gigante llena la bodega de datos repetidos, y cómo el bibliotecario cruza dos estantes (`players` y `villages`) usando una llave (`village_id`).
   - **Visual en la bodega:** Dos estantes frente a frente conectados con hilos/rieles donde coincide el estandarte. Qué pasa con el jugador sin aldea en `INNER JOIN` (queda fuera) vs `LEFT JOIN` (entra con su casilla de aldea vacía `NULL`).
   - **Extra técnico:** Cómo lo hace el bibliotecario por dentro (*Nested Loop* vs *Hash Join* vs *Merge Join*).

2. **`GROUP BY`, Agregaciones (`COUNT`, `SUM`, `AVG`) y `HAVING` vs `WHERE`**
   - **Gancho:** "¿Cuántas esmeraldas tiene cada aldea en total?" y la trampa clásica de entrevista: ¿por qué no puedes usar `WHERE COUNT(*) > 5`?
   - **Visual en la bodega:**
     1. `WHERE` filtra jugadores *antes* de juntarlos en cajas.
     2. `GROUP BY village` mete a los jugadores en cajas separadas por estandarte de aldea.
     3. `SUM(emeralds)` funde las esmeraldas de cada caja en un solo total.
     4. `HAVING` tira las cajas ya armadas que no alcancen el mínimo.

3. **Window Functions (`ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LAG`, `LEAD`)**
   - **Gancho:** Cómo sacar un ranking o comparar con la fila anterior **sin aplastar las filas** como lo hace `GROUP BY`.
   - **Visual en la bodega:** En `GROUP BY` las filas desaparecen dentro de una caja resumen. En `OVER (PARTITION BY village ORDER BY emeralds DESC)`, los jugadores siguen parados en su estante pero el bibliotecario les cuelga una medalla (`1, 2, 2, 4` en `RANK` vs `1, 2, 2, 3` en `DENSE_RANK`).

4. **El misterio de `NULL` (Por qué `NULL = NULL` no es verdadero)**
   - **Gancho:** El error que rompe miles de reportes: buscar `WHERE guild != 'Red'` y que desaparezcan todos los jugadores que no tienen clan (`NULL`).
   - **Visual en la bodega:** Una casilla con `0` tiene un marco vacío; una casilla `NULL` tiene un cofre cerrado con signo de interrogación ("desconocido"). Si preguntas *"¿lo que hay adentro es igual a lo de este otro cofre cerrado?"*, el bibliotecario no responde ni Sí (`TRUE`) ni No (`FALSE`), responde `UNKNOWN`. Por eso existe `IS NULL` y `COALESCE`.

5. **Subconsultas vs CTEs (`WITH`) vs Vistas (`VIEW`) vs Tablas Temporales**
   - **Gancho:** Consultas dentro de consultas que nadie puede leer vs armar mesas de trabajo paso a paso con `WITH`.
   - **Visual en la bodega:** Una subconsulta correlacionada obliga al bibliotecario a correr toda la bodega por cada fila; un CTE (`WITH ricos AS (...)`) arma una mesa auxiliar etiquetada para usarla limpia en el paso siguiente; una `VIEW` no es un estante real, es una ventana mágica con una consulta guardada.

6. **Normalización (1NF, 2NF, 3NF) vs Desnormalización**
   - **Gancho:** ¿Qué pasa si un jefe de aldea cambia de nombre y tienes que editar 10,000 filas a mano? (Anomalías de actualización, inserción y borrado).
   - **Visual en la bodega:** Pasar de un estante caótico con listas pegadas en un solo letrero a 3 estantes limpios conectados por ID (`Primary Key` y `Foreign Key`), y cuándo vale la pena romper la regla a propósito para leer más rápido.

---

## 2. Casos Reales de SQL en Producción ("¿Por qué se cayó la base de datos?")

7. **El problema `N+1 Queries` (El asesino silencioso de los ORMs)**
   - **Caso real:** Pides la lista de 100 jugadores con su aldea. El código hace 1 consulta para traer los 100 jugadores (`SELECT * FROM players`) y luego dentro de un `for` manda **100 viajes separados** al bibliotecario (`SELECT * FROM villages WHERE id = ?`).
   - **Visual:** El mensajero corriendo 101 veces por las escaleras de la bodega vs pedir todo en 1 solo viaje con `JOIN` o `WHERE id IN (...)`.

8. **Por qué tu Índice dejó de funcionar (Las 4 trampas que fuerzan un *Full Table Scan*)**
   - **Caso real:** Pusiste un índice pero la consulta sigue tardando 10 segundos.
   - **Las 4 trampas visuales con el árbol de letreros:**
     1. `LIKE '%steve%'` (comodín al inicio: en un diccionario ordenado de la A a la Z no puedes buscar por cómo *termina* una palabra).
     2. Envolver la columna en una función (`WHERE YEAR(created_at) = 2026` en vez de rango de fechas).
     3. Índice compuesto (`(village, emeralds)`) usado al revés (buscar solo por `emeralds` sin dar `village`).
     4. Baja cardinalidad o pedir el 80% de la tabla (sale más barato recorrer el estante corrido que saltar mil veces del árbol al estante).

9. **Paginación en Millones de Filas: Por qué `OFFSET 1000000` congela tu app (y cómo lo arregla *Keyset / Cursor Pagination*)**
   - **Caso real:** En la página 1 (`LIMIT 10 OFFSET 0`) carga al instante; en la página 50,000 (`LIMIT 10 OFFSET 500000`) tarda 15 segundos.
   - **Visual:** Con `OFFSET 500000`, el bibliotecario igual tiene que contar y sacar 500,000 filas del estante para tirarlas a la basura y quedarse con 10. Con *Cursor Pagination* (`WHERE id < ultimo_id_visto LIMIT 10`), pone un separador de libros donde se quedó y salta directo en $O(\log N)$.

10. **Niveles de Aislamiento y MVCC (Cómo leen miles mientras otros escriben sin bloquearse)**
    - **Caso real:** *Dirty Reads* (leer dinero de una transacción que luego hace rollback), *Non-Repeatable Reads* y *Lost Updates* (dos cajeros cobrando el último asiento: `SELECT ... FOR UPDATE`).
    - **Visual:** Cómo Postgres usa fotografías instantáneas por versión (*MVCC*) para que los lectores nunca esperen a los escritores.

11. **`EXPLAIN ANALYZE`: Cómo piensa el Optimizador de Consultas**
    - **Caso real:** Tú escribes *qué* quieres, pero el bibliotecario revisa su libreta de estadísticas (cuántas filas hay en cada estante) y dibuja el mapa de costos antes de mover un dedo.

12. **El costo oculto de tener demasiados Índices**
    - **Caso real:** "Si los índices aceleran `SELECT`, ¿por qué no indexo las 20 columnas?"
    - **Visual:** Cada vez que entra un jugador nuevo (`INSERT`) o gana una esmeralda (`UPDATE`), el bibliotecario no solo cambia el estante principal: tiene que correr a reacomodar 20 árboles de letreros distintos. Lecturas vuelan, escrituras se arrastran.

---

## 3. Problemas Clásicos de SQL en LeetCode (Usando la misma Bodega)

Con el mismo set de `videos/tech/sql/` puedes sacar la serie de **LeetCode Database**:

- **#175 Combine Two Tables:** El mejor para introducir `LEFT JOIN` (jugadores que no tienen dirección aún deben salir con `NULL`).
- **#176 Second Highest Salary:** Cómo hallar el segundo con más esmeraldas (y qué pasa si hay empate o solo hay 1 jugador: `LIMIT 1 OFFSET 1` vs `MAX() WHERE < MAX()`).
- **#178 Rank Scores:** Mostrar en vivo la diferencia entre `ROW_NUMBER()`, `RANK()` y `DENSE_RANK()`.
- **#181 Employees Earning More Than Their Managers:** *Self-Join* (cruzar el estante `players` consigo mismo cuando el jefe también es una fila del mismo estante).
- **#182 Duplicate Emails:** `GROUP BY email HAVING COUNT(*) > 1` en 45 segundos.
- **#183 Customers Who Never Order:** `LEFT JOIN ... WHERE b.id IS NULL` vs `NOT IN` (y el peligro mortal de `NOT IN` cuando hay un `NULL`).
- **#185 Department Top Three Salaries:** El jefe final de `DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) <= 3`.

---

## 4. SQL Avanzado y Tripas del Motor Relacional

Temas de nivel Senior / DBA / Internals, muy visuales usando la bodega del bibliotecario:

13. **Algoritmos Físicos de JOIN: *Nested Loop* vs *Hash Join* vs *Merge Join***
    - **Concepto:** Tú escribes `JOIN`, pero el bibliotecario tiene 3 formas físicas de cruzar dos estantes:
      1. *Nested Loop:* Por cada fila del estante A, recorre el estante B (bueno solo si A es diminuto y B tiene índice).
      2. *Hash Join:* Arma una tabla hash en una mesa temporal (`work_mem`) con el estante chico y pasa el grande una sola vez (y qué pasa cuando no cabe en la mesa y desborda a barriles en el piso: *disk spill*).
      3. *Sort-Merge Join:* Si ambos estantes ya están ordenados por la llave, avanza con dos dedos en paralelo como cierre de chamarra en $O(N + M)$.

14. **MVCC (Multi-Version Concurrency Control), Filas Fantasma (*Dead Tuples*) y `VACUUM`**
    - **Concepto:** En Postgres, un `UPDATE` o `DELETE` **jamás borra ni sobrescribe la fila en el estante**. Hacer `UPDATE emeralds = 20` deja la fila vieja marcada con un sello de "muerta a partir del turno X" (`xmax`) y escribe una fila nueva más adelante (`xmin`).
    - **Visual:** Por qué dos lectores ven distintas versiones de la misma fila sin bloquearse, por qué el estante se hincha de cadáveres (*Table Bloat*) si haces muchos updates, y cómo entra el gólem barrendero (`AUTOVACUUM`) a limpiar los huecos muertos.

15. **Recursividad en SQL (`WITH RECURSIVE`): El caso donde el jefe también es esclavo**
    - **Gancho visual:** Todos están en el **mismo estante** (`players` con `id`, `name`, `boss_id`). No hay una tabla de jefes y otra de esclavos: el capataz manda al minero, pero ese mismo capataz tiene `boss_id` apuntando al noble, y el noble es esclavo del Rey (`boss_id = NULL`). Todo jefe (salvo la raíz) es a la vez esclavo de alguien más arriba.
    - **El problema del `JOIN` normal:** Un *Self-Join* (`players e JOIN players boss ON e.boss_id = boss.id`) solo sube **un escalón**. Si la cadena de mando tiene 8 niveles (o no sabes cuántos niveles tiene), no puedes adivinar cuántos `JOIN` escribir.
    - **Cómo lo resuelve `WITH RECURSIVE` en la bodega (las 2 mesas del bibliotecario):**
      1. **Caso Base (Ancla):** El bibliotecario busca primero al único que no es esclavo de nadie (`WHERE boss_id IS NULL` → el Rey, nivel 1) y lo pone en una **Mesa de Turno** (*Working Table*).
      2. **Paso Recursivo (`UNION ALL`):** Mira quién está en la Mesa de Turno, camina al estante y trae a todos los que tengan `boss_id = id_de_la_mesa` (los esclavos directos del Rey, nivel 2). Pasa al Rey al **Cofre Final** y deja solo a los nuevos en la Mesa de Turno.
      3. **Repetición automática:** En la siguiente vuelta, esos jefes de nivel 2 buscan a sus propios esclavos (nivel 3). Cuando el último esclavo de hasta abajo ya no tiene a nadie debajo de él, la Mesa de Turno queda vacía y la consulta se detiene sola.
    - **El giro / trampa mortal (Ciclo infinito: cuando el Rey es esclavo del último esclavo):**
      - ¿Qué pasa si alguien edita la fila del Rey (`id = 1`) y le pone que su jefe es el minero del nivel 4 (`boss_id = 4`)? Ahora el jefe supremo es esclavo de su propio esclavo (`1 → 2 → 3 → 4 → 1...`).
      - El bibliotecario entra en un **bucle infinito** metiendo las mismas filas una y otra vez hasta reventar la bodega.
      - **La solución en SQL:** Llevar una lista de visitados en el camino (`path` o cláusula `CYCLE id SET is_cycle USING path`) o un tope de profundidad (`WHERE level < 10`) para que el bibliotecario vea que ese ID ya pasó por la mesa y corte la cadena.
    - **Consulta de ejemplo para el libro:**
      ```sql
      WITH RECURSIVE chain AS (
        SELECT id, name, boss_id, 1 AS lvl
        FROM players WHERE boss_id IS NULL
        UNION ALL
        SELECT p.id, p.name, p.boss_id, c.lvl + 1
        FROM players p
        JOIN chain c ON p.boss_id = c.id
      )
      SELECT * FROM chain;
      ```

16. **Clustered Index (MySQL InnoDB) vs Heap Table (Postgres) e *Index-Only Scans***
    - **Concepto:**
      - En **MySQL (InnoDB)**, el estante principal *es* las hojas del árbol B+ de la Primary Key (*Clustered Index*). Si buscas por un índice secundario, este no apunta al estante sino a la Primary Key (doble búsqueda en árbol).
      - En **Postgres**, el estante es un montón sin orden (*Heap*) y todos los índices apuntan a la coordenada física `(página, hueco)`. Si usas un *Covering Index* (`CREATE INDEX ... INCLUDE (emeralds)`), el bibliotecario lee el dato directo del árbol sin caminar nunca al estante (*Index-Only Scan*).

17. **`SELECT ... FOR UPDATE SKIP LOCKED`: Cómo convertir una tabla SQL en una cola ultrarrápida**
    - **Concepto:** Si 10 bibliotecarios quieren procesar pedidos pendientes al mismo tiempo, con `FOR UPDATE` normal 9 se quedan formados esperando al primero. Con `SKIP LOCKED`, cada bibliotecario se salta las filas que tienen candado y agarra la siguiente libre al instante sin estorbarse.

18. **Anomalías de Aislamiento Reales: *Phantom Reads*, *Write Skew* y `SERIALIZABLE` (SSI)**
    - **Concepto:** El caso clásico de *Write Skew*: la regla dice que siempre debe haber al menos 1 guardia despierto en la aldea. Hay 2 guardias (Steve y Alex). Al mismo tiempo ambos revisan `SELECT COUNT(*) WHERE despierto = true` (ambos ven `2`), así que cada uno actualiza su propia fila a `despierto = false`. Ninguno tocó la misma fila que el otro (no hubo conflicto de candado de fila), pero la aldea se quedó con `0` guardias.

19. **Índices más allá del B-Tree: `GIN`, `BRIN`, *Partial Indexes* y *Expression Indexes***
    - **Concepto:**
      - **Partial Index (`WHERE active = true`):** Si el 99% de tus pedidos ya están cerrados, ¿para qué indexarlos? Un árbol diminuto solo para el 1% pendiente.
      - **BRIN (Block Range Index):** En un estante de 100 millones de eventos ordenados por fecha, en vez de un árbol gigante solo anotas en la entrada de cada pasillo *"Pasillo 4: del 1 al 5 de mayo"*. Ocupa 1,000 veces menos espacio.
      - **GIN:** Índice invertido para buscar dentro de un `JSONB` o arreglo en una columna.

20. **`LATERAL JOIN` (`CROSS APPLY`): El "for-each" dentro de SQL**
    - **Concepto:** Quieres traer las 3 compras más caras de *cada* jugador. Un `JOIN` normal no te deja usar `LIMIT 3` por cada fila de la izquierda; `JOIN LATERAL` le permite al bibliotecario correr una mini-consulta con `ORDER BY ... LIMIT 3` por cada jugador que va leyendo.

21. **Particionamiento de Tablas y *Partition Pruning* (`DROP` vs `DELETE` de 100 millones de filas)**
    - **Concepto:** Hacer `DELETE FROM logs WHERE fecha < '2025-01-01'` en una tabla gigante satura el WAL, bloquea discos y llena de *dead tuples*. Si partes la tabla por mes (particiones físicas separadas), la consulta ignora cuartos enteros (*Partition Pruning*) y borrar un mes viejo es simplemente desenganchar ese cuarto en 1 ms (`DROP TABLE logs_2024_12`).

22. **Páginas de 8KB, *Buffer Pool*, *Dirty Pages* y *Checkpoints***
    - **Concepto:** El disco nunca lee 1 sola fila: sube cajas completas de **8 KB (Pages)** a la mesa del bibliotecario (RAM / *Buffer Pool*). Ahí las modifica (*Dirty Page*), anota el cambio en su pergamino (*WAL*) y responde "listo" sin haber tocado el estante del sótano todavía.

23. **Window Frames Avanzados (`ROWS` vs `RANGE`, Acumulados y *Gaps & Islands*)**
    - **Concepto:** Cómo calcular una suma acumulada o promedio móvil de 3 días (`ROWS BETWEEN 2 PRECEDING AND CURRENT ROW`), la diferencia tramposa entre `RANGE` (agrupa empates) y `ROWS` (cuenta filas físicas), y cómo detectar rachas de días seguidos conectándose (*Gaps and Islands*).

24. ***Parameter Sniffing* y Estadísticas del Optimizador (Por qué un plan cacheado de pronto se vuelve lentísimo)**
    - **Concepto:** Si la primera vez que se compila una consulta buscan una aldea chiquita (2 jugadores), el bibliotecario guarda como plan fijo usar el índice. Cuando luego buscan la capital (900,000 jugadores) reutilizando ese mismo plan guardado, da 900,000 viajes individuales del árbol al estante en vez de barrer el estante de corrido.

