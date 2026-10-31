# Diseño: continuación de Git ("How Teams Really Use Git — Part 2"), todo en 3D

Estado: **aprobado por Aldo (2026-10-31)**. Lo escribió AGY (el original sigue en `videos/tech/git/DisenoShort.md`); esta copia es la que se construye, con dos ajustes de Claude:
- Línea 10: `reset` solo rompe a los demás si se fuerza el push ("If you rewind with git reset and force the push, anyone who pulled it gets broken links.").
- Línea 13: el reflog no es secreto, es local ("Git keeps a local diary...").

---

## 1. Punto de partida: qué ya cubrió el Short 1 (`videos/tech/git/`)

En el primer short (`three/git.html`, 22 líneas) ya se vio y explicó:
- **Líneas 0–1:** Steve rompe el techo (`S1` → `S1b`) y lo recupera con `git restore` (reloj de máquina del tiempo).
- **Líneas 2–4:** Snapshot completo (`c1: a1f3`), ventanas al cofre con `git add` (staging area) y nueva maqueta con `git commit` (`c2: c7e2`).
- **Líneas 5–7:** Cadena de historia con riendas (`parent`), bloques sin cambios que no se guardan dos veces (brillan juntos en `c1` y `c2`), y cambio de hash (`c7e2` → `5b90`) si cambia un bloque.
- **Líneas 8–11:** Estandarte blanco `main` avanzando a `c3` (`9d04 skylight`), nueva rama naranja `roof`, `HEAD` sobre Steve, `git switch roof` cambiando el techo real a pirámide de lana roja (`c4: e15b`), y regreso a `main` (`git switch main`).
- **Líneas 12–13:** `c5` (`3a8c lamp`) en `main`, `git merge roof` creando `c6` (`f2d1`) con **dos riendas** (`two parents`), y resolución del **conflicto** en el pico del techo (parpadea entre lana roja y glowstone hasta que Steve elige glowstone).
- **Líneas 14–18:** Repositorio local de Steve (`at: [0, 0]`), remoto en la plaza de la campana (`at: [-10, -18]` con el cartógrafo en `(-2, G, -6.3)`) y casa de Alex (`at: [-30, -13]`). `git push` de `c4..c6` a la plaza, `git pull` a la casa de Alex, y el choque cuando Alex sube su chimenea (`c7: 7b3e`) antes que el tope de oro de Steve (`c8: b06a`): `push` rechazado (`shakeNo`), `pull` + `merge` (`c9: d4c9`) y `push` aceptado.

---

## 2. Qué explica esta continuación (Short 2) sin repetir nada del Short 1

El Short 1 termina con la casa de Steve en el estado `S9` (ventanas de vidrio, techo de lana roja con tope de oro y chimenea de ladrillos de Alex) y 9 pedestales (`c1..c9`) llenos de diamantes de merge. A partir de ahí, el Short 2 responde las **6 preguntas reales** que surgen en cuanto usas Git de verdad:

1. **`git clone` (¿Cómo empieza alguien nuevo desde cero?):**
   - En el Short 1 Alex ya tenía `c3` en su patio. Aquí se muestra cómo un constructor descarga por primera vez toda la cadena de maquetas desde la plaza de la campana a un patio vacío con **`git clone`**.
2. **`git diff` y `.gitignore` (¿Cómo reviso qué cambié y cómo evito subir basura o contraseñas?):**
   - Antes de meter bloques al cofre, **`git diff`** resalta en la casa real los bloques agregados en **verde (`+`)** y los quitados en **rojo (`-`)** frente a la última maqueta.
   - Pero Steve también puso **andamios temporales** (`node_modules` / archivos de compilación) y tiene un **libro con llaves secretas** (`.env` / contraseñas). Un filtro **`.gitignore`** en el cofre los rebota automáticamente para que jamás entren a un commit ni se suban a la plaza pública.
3. **`git stash` (¿Qué hago si estoy a mitad de un cambio y sale una urgencia?):**
   - Steve está a mitad de construir un porche (bloques a medio poner) cuando suena la campana de emergencia. No quiere hacer un commit a medias: **`git stash`** guarda esos bloques sueltos en un cofre temporal aparte y deja la casa limpia como la última maqueta; al terminar la urgencia, **`git stash pop`** los devuelve a su lugar.
4. **`git revert` vs `git reset` (¿Cómo deshago un commit malo que YA se subió sin romperle el proyecto al equipo?):**
   - En el Short 1 vimos `git restore` cuando aún no habías hecho commit. ¿Pero qué pasa cuando el error **ya es una maqueta en la cadena** (por ejemplo, una fogata/fuego en la chimenea que quema el techo)?
   - Si rompes esa maqueta con **`git reset`**, cortas la rienda de los demás que ya se colgaron de ella.
   - Con **`git revert`**, Git crea una **maqueta nueva al final** que aplica el cambio inverso (apaga el fuego y restaura el bloque), arreglando el desastre sin borrar la historia.
5. **`git rebase` vs `git merge` (¿Por qué la fila de pedestales se llenó de diamantes y cómo se deja en línea recta?):**
   - Muestra el contraste directo sobre los pedestales: mientras `merge` une dos caminos con dos riendas (dejando diamantes como `c4/c5 → c6`), **`git rebase`** toma la maqueta de tu rama local y la vuelve a plantar **en fila recta delante de la última maqueta de `main`** (antes de hacer `push`).
6. **Pull Requests (PR), Pruebas (CI) y Code Review en la plaza de la campana:**
   - En el Short 1 Steve y Alex empujaban directo al estandarte `main` de la plaza. En un equipo real, **`main` está protegido con vallas**: subes tu rama a un costado de la plaza, abres un **Pull Request** en el atril, el gólem prueba que la maqueta sea segura (**CI checks**) y Alex la aprueba (**Code Review**) antes de mover el estandarte `main`.
7. **Bonus de rescate (`git reflog`):**
   - Si borraste un estandarte por error, la maqueta no desaparece: el bibliotecario anota cada paso de `HEAD` en su bitácora (`reflog`) para que puedas volver a clavar el estandarte.

---

## 3. Coordenadas y escenario en `mundos/savanna-village.json`

Reutiliza exactamente el mismo mapa y sistema de coordenadas de `videos/tech/git/three/git.html`:
- **Casa de Steve:** `x 5..11, z 0..6, y 1..10`, piso `G = 1`.
- **Cofre de Staging:** `(11.5, G, 7.5)`, más un segundo cofre oscuro (`stashBox`) al lado en `(13.2, G, 7.5)` para `git stash`.
- **Pedestales de Steve (`REPOS.steve`):** fila principal en `z = 9` (`x = 4, 7, 10, 13, 16, 19, 22`) y carril de rama en `z = 12.5`.
- **Plaza de la campana (`REPOS.remote`, `at: [-10, -18]`):** custodiada por el cartógrafo (`keeper` en `(-2, G, -6.3)`), agregando:
  - Cerca de acacia (`makeFencePost`) alrededor del estandarte `main` de la plaza (rama protegida).
  - Un atril (`makeLectern` de `aldea.js`) en `(-0.5, G, -6.5)` para el **Pull Request**.
  - Un gólem de hierro (o el propio cartógrafo con farol verde) para los **checks automáticos**.
- **Casa de Alex (`REPOS.alex`, `at: [-30, -13]`):** Alex en `(-15.5, -2.0)`.

---

## 4. Narración (borrador en inglés)

24 líneas, 365 palabras (~135 s a 2.7 palabras por segundo).

```
0  You know how Git saves your house as a chain of models. Now, how do real teams use it every day without chaos?
1  When a new builder joins the village, she starts with an empty yard.
2  git clone copies the entire chain of models from the bell square, so she has the full project and its history.
3  Back at Steve's house, before saving, git diff compares the real house to the last model: green for added blocks, red for removed ones.
4  But not everything in your yard belongs in Git. Temporary ladders and secret keys should never go into the chest.
5  A file called dot gitignore blocks them at the lid, so junk and passwords never enter a commit.
6  Now, what if you're halfway through building a porch, and the emergency bell rings? You don't want to commit half a porch.
7  git stash tucks your unfinished blocks into a side chest, leaving the house clean. Fix the problem, then pop them right back.
8  What if a bad commit is already in the chain, like a fireplace that sets the roof on fire?
9  In the first video, git restore fixed the house before a commit. Here, the mistake is already saved on a pedestal.
10 If you rewind with git reset and force the push, anyone who pulled it gets broken links.
11 Instead, git revert adds a brand new model at the end that does the exact opposite, putting the fire out without erasing history.
12 What if someone deletes a branch banner by mistake? The model isn't gone.
13 Git keeps a local diary of every step HEAD took, called the reflog. Read the diary, find the pedestal, and plant the banner again.
14 Next, keeping history tidy. Merging branches creates diamond knots with two leads.
15 If your branch is still local, git rebase picks up your new models and replays them straight in front of main: one clean line.
16 Just never rebase models you already pushed to the square, or your teammates' leads won't match.
17 Finally, how teams protect the bell square. In real projects, nobody pushes straight to main.
18 Steve pushes his branch to the square and opens a Pull Request on the lectern.
19 Automated checks test that the model doesn't break, and Alex inspects the changes block by block.
20 Once she approves, the square merges the branch into main, and everyone pulls the update.
21 Clone, ignore the junk, stash, revert, and review every change in the square.
22 That's how teams really use Git.
```

---

## 5. Exactitud técnica (revisar antes de generar la voz)

- **`git clone`:** descarga tanto el último estado como todo el historial de commits y ramas del remoto. Exacto (línea 2: *"the full project and its history"*).
- **`git diff`:** muestra las diferencias entre el árbol de trabajo y el índice/`HEAD` (adiciones en verde, eliminaciones en rojo). Exacto.
- **`.gitignore`:** impide que archivos no rastreados que coincidan con la lista entren al staging area con `git add`, manteniéndolos intactos en el directorio de trabajo. Exacto.
- **`git stash` / `git stash pop`:** guarda cambios locales sin confirmar a un lado, restaura el directorio de trabajo a `HEAD` y luego los vuelve a aplicar. Exacto.
- **`git restore` vs `git reset` vs `git revert`:**
  - `restore`: descarta cambios no confirmados en la casa real (referenciado en la línea 9).
  - `reset`: mueve la rama hacia atrás dejando commits fuera de la historia; si ya se habían compartido, rompe la historia del equipo (línea 10).
  - `revert`: crea un commit nuevo que invierte los cambios del commit defectuoso sin reescribir la historia (línea 11). Exacto.
- **`git reflog`:** registra localmente cada movimiento de `HEAD` y de las ramas, permitiendo recuperar commits que quedaron sin estandarte (*dangling commits*) antes de que pase el recolector de basura. Exacto.
- **`git rebase`:** toma los commits de una rama y los reaplica sobre otra base creando commits nuevos en línea recta; la regla de oro es no hacer rebase de commits públicos (líneas 15 y 16). Exacto.
- **Pull Request + CI + Code Review:** rama `main` protegida en el servidor remoto (`GitHub`), subida de la rama de trabajo, ejecución de pruebas automáticas y revisión por pares antes del merge. Exacto.

---

## 6. Escenas paso a paso (diseño para `three/git2.html`)

| Escena | Líneas | Qué ocurre en el mundo 3D | Cámara sugerida |
|---|---|---|---|
| **1. Portada** | `0` | Letrero `"HOW TEAMS / USE GIT"` en `z = 17` frente a la casa de Steve (en estado `S9` con sus pedestales). Baja al suelo como en `git.html`. | `COVER` (`(8, 3.4, 26)` → `(8, 2.8, 17)`) |
| **2. `git clone`** | `1–2` | Patio de Alex vacío al inicio. Globo `git clone`: las maquetas vuelan en cadena desde la plaza (`REPOS.remote`) hasta los pedestales de Alex (`REPOS.alex`), atándose con riendas y colocando su estandarte `main`. | `ALEXSQ` → `ALEXV` |
| **3. `git diff`** | `3` | En la casa de Steve, dos bloques nuevos brillan con un marco verde (`makeFrame` teñido `0x55FF55`) y un bloque quitado muestra un marco rojo (`0xFF5555`). Globo `git diff: +added  -removed`. | `STEVEV` (`(12, 3.4, 11.5)` → `(8.6, 2.2, 5.6)`) |
| **4. `.gitignore`** | `4–5` | Junto al cofre de staging `(11.5, G, 7.5)` hay un letrero `.gitignore`. Tres objetos vuelan hacia el cofre: un bloque de vidrio entra (`pop`), pero una escalera temporal y un libro encantado (`secrets.env`) chocan con un ícono de `barrier` sobre el cofre y rebotan al pasto (`villager_no1`). | `CHESTV` (`(13.8, 2.9, 11.2)` → `(10.6, 1.4, 7.0)`) |
| **5. `git stash`** | `6–7` | Steve coloca dos bloques de un porche frente a la puerta. Suena la campana (`bell`). Globo `git stash`: se abre un segundo cofre oscuro en `(13.2, G, 7.5)`, los bloques del porche vuelan adentro y la fachada vuelve a quedar limpia. Luego globo `git stash pop`: el cofre se abre y los bloques regresan al porche. | `WIDE` / `STEVEV` |
| **6. `git reset` vs `git revert`** | `8–11` | En los pedestales hay un commit malo (`c_bad: b4d1`, `"fire"`), con fuego encendido sobre el techo tanto en la maqueta como en la casa real. Sobre `c_bad` aparece una barrera roja cuando se nombra `git reset` (`breaks shared history!`). Luego globo `git revert`: se construye un pedestal nuevo adelante (`c_rev: e8a2`, `"revert b4d1"`) atado con rienda a `c_bad`, y el fuego se apaga con sonido `fizz`. | `ROW` → `MERGE` |
| **7. `git reflog`** | `12–13` | El estandarte naranja se rompe y desaparece por error; su pedestal se oscurece un poco. El cartógrafo abre un atril con el globo `git reflog: HEAD -> e15b`; Steve camina al pedestal y vuelve a plantar el estandarte naranja. | `BRANCH` (`(16, 4.5, 18)` → `(10.5, 2.0, 9.5)`) |
| **8. `git rebase` vs `git merge`** | `14–16` | Se ve el diamante de dos riendas (`c4/c5 → c6`, globo `merge: diamond`). Luego, en una rama local nueva, la maqueta lateral se levanta en arco y se posa en el pedestal de adelante en la misma fila recta `z = 9` (`rebase: straight line`, cambiando su hash en el letrero). Globo de advertencia rojo: `local only!`. | `MERGE` (`(21, 5.5, 20)` → `(14, 2.0, 10)`) |
| **9. Pull Request y Code Review** | `17–20` | En la plaza de la campana (`SQUARE`), el estandarte `main` tiene postes de valla alrededor (`protected`). Steve manda su maqueta al carril lateral de la plaza y se abre el libro de un atril (`Pull Request #1`). Primero sale brillo verde (`checks: passed`), luego Alex camina junto al atril, mira la maqueta y asiente (`approved`). La maqueta de `merge` se crea en la fila `main` de la plaza, el estandarte `main` avanza, y copias vuelan a Steve y Alex. | `SQUARE` → `PUSH` → `TEAM` |
| **10. Cierre y Loop** | `21–22` | Toma aérea `TEAM` con los tres repositorios sincronizados; repaso en 3 globos y regreso suave a la pose `COVER` mientras el letrero sube para cerrar el loop (con `LOOP_T` restaurando el cuadro 0). | `TEAM` → `RECAP` → `COVER` |

---

## 7. Configuración lista para `video.json` y `descripcion.txt`

Cuando se cree la carpeta del segundo video (por ejemplo `videos/tech/git-workflow/` o `videos/tech/git-part2/`):

- **`descripcion.txt`** (95 caracteres):
  ```
  How teams really use Git: clone, stash, revert, rebase & Pull Requests in Minecraft #git #shorts
  ```
- **`video.json`**:
  ```json
  {"solo3d": {"page": "three/git2.html"}, "formato": "9:16", "tema": "minecraft-original",
   "musica": {"pista": "mice_on_venus", "volumen": 0.45},
   "subtitulos": {
    "cambios": {"dot gitignore": ".gitignore"},
    "amarillo": ["git clone", "git diff", ".gitignore", "git stash", "git restore", "git reset", "git revert",
                 "reflog", "git rebase", "Pull Request", "main"],
    "verde": ["added blocks", "house clean", "exact opposite", "one clean line", "checks", "approves"],
    "rojo": ["removed ones", "secret keys", "on fire", "broken links", "by mistake", "never rebase"],
    "dorado": ["How teams really use Git"]}}
  ```

---

## 8. Qué piezas técnicas reutiliza y qué pequeñas adiciones requiere

1. **Ya existen y se importan igual que en `videos/tech/git/three/git.html`:**
   - Mundo `savanna-village.json` con `makeWorld({ fov: 40, offset: 0, fog: [90, 220], shaders: true })`.
   - `makeModel`, `PIECES`, `LEADS`, `BANNERS` y `FLIGHTS` de `three/git.html`.
   - `makeBanner`, `makeLead`, `makeKnot`, `makeFencePost`, `makeDrop`, `makeCracks`, `swingArm`, `shakeNo` de `objetos.js`.
   - `makeLectern`, `bubble`, `placeUI`, `cameraAt`, `arc`, `makeItem` de `aldea.js`.
2. **Únicos elementos extra en la página `three/git2.html` (sin necesidad de modificar `objetos.js`):**
   - `fire` (textura que `extraer.py` ya copia desde el short del servidor) para el bloque de la chimenea defectuosa en `c_bad` y el sonido `fizz` al hacer `git revert`.
   - `barrier` y `writable_book` (ya existen en `tex/`) para el rebote de `.gitignore` sobre el cofre.
   - `makeLectern` (ya existe en `aldea.js`) para el atril del **Pull Request** en la plaza de la campana.
