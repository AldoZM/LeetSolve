# Diseño: short "How Git works", todo en 3D

Estado: **aprobado y construido (2026-10-31)**. Aldo aprobó el diseño y la muestra de las líneas 2 a 9 (🟢). Lo que cambió al construirlo:
- La casa de Steve es la choza de acacia de (5..11, 0..6). Se saca del terreno y se dibuja por estados (S1 a S9) para poder cambiarla: ventanas de vidrio, tragaluz, techo de lana roja, lámpara de glowstone, chimenea de Alex y punta de oro de Steve.
- El gancho rompe el techo con las grietas del juego (`destroy_stage`) y lo regresa con `git restore`.
- Commits: `a1f3` start, `c7e2` windows, `9d04` skylight, `e15b` new roof (rama `roof`), `3a8c` lamp (main), `f2d1` merge, `7b3e` chimney (Alex), `b06a` gold top (Steve) y `d4c9` merge.
- El remoto usa el mismo acomodo de pedestales movido (−10, −18) a la plaza, y Alex el mismo movido (−30, −13) junto a su casa.
- La línea 20 dice "A chain of snapshots…": "Snapshots" al inicio salía "Step shots".
- Loop: en la última línea todo vuelve al estado del cuadro 0 detrás de la portada.

## Intención

Short de la línea "cómo funcionan las tecnologías" (`videos/tech/`). Explica **qué hace Git por dentro y cómo se usa en el día a día**, con las animaciones 3D de Minecraft haciendo el trabajo: que alguien que nunca lo usó entienda qué es un commit, una rama, un merge y un push solo con ver el mundo. Misma forma que DNS y Kafka: primero cómo funciona y luego cómo se usa con otras personas.

Decisiones de Aldo (2026-10-31):
- Alcance: por dentro + uso diario.
- Metáfora: maquetas de la casa.
- Lugar: una aldea de sabana real del juego (la generó Aldo en MacEntorno).
- El remoto (GitHub) es la plaza de la campana.
- Iluminación tipo shaders, de día.
- Las animaciones son las del juego (ver "Animaciones").

## Metas

- Un short vertical (1080 × 1920, 30 fps) de **hasta 3 minutos**, sin estirarlo. La narración de abajo da unos 125 a 140 s.
- Que se lleven seis ideas:
  1. Un commit es una foto de **todo** el proyecto, no solo del cambio.
  2. Antes del commit eliges qué entra (staging, `git add`).
  3. Los commits forman una cadena: cada uno apunta al anterior.
  4. Una rama es solo una etiqueta que se mueve, y HEAD es dónde estás parado.
  5. Merge junta dos ramas, y un conflicto es cuando las dos tocaron lo mismo.
  6. El remoto es otra copia: push manda tus commits, pull trae los de otros, y un push se rechaza si te falta trabajo ajeno.
- Todo dentro del mundo 3D: letreros, estandartes, globos de tooltip y objetos. Nada de capas 2D encima. Los comandos (`git add`, `git commit`...) aparecen como globos de tooltip del juego, cortos.

## Fuera del alcance

- Rebase, stash, reset, revert, tags, `.gitignore`, pull requests y forks.
- Cómo se calcula el hash (SHA). Solo se dice que el nombre sale del contenido.
- Fast-forward contra merge commit. El merge del video siempre crea un commit nuevo con dos padres.
- Instalación o configuración de Git, y la terminal real.
- Publicar, hacer commit o push al repo de LeetSolve: lo decide Aldo.

## No debe pasar (aunque técnicamente funcione)

- Que la narración diga algo falso de Git (ver "Exactitud").
- Que parezca que un commit guarda solo el cambio: la maqueta siempre es la casa completa.
- Que parezca que una rama es una copia del proyecto: es solo el estandarte.
- Animaciones inventadas cuando el juego ya tiene una para eso.
- Texto ilegible en el celular, cortado en los bordes o tapado por el terreno. Globos que se enciman (errores 18 y 19 de `GUIA.md`).
- Logos de marcas reales (GitHub, Git) o el logo de Minecraft. El nombre "GitHub" en texto sí.
- Subir al repositorio archivos del juego.

## La metáfora

- **El proyecto** es la casa de Steve, una casa real de la aldea (la de la calle del atril, a unos 40 bloques de la campana). Cambiar el proyecto es poner o quitar bloques.
- **Un commit** es una **maqueta**: la casa completa en miniatura (escala 1/8) sobre un pedestal de piedra pulida junto a la casa, con un letrero que lleva su nombre corto (`a1f3`) y el mensaje ("add door").
- **El staging** es un **cofre** junto a la casa. `git add` = los bloques cambiados vuelan al cofre como objetos que se recogen. `git commit` = el cofre se cierra y aparece la maqueta.
- **La cadena** son **riendas** del juego entre pedestales: cada maqueta va amarrada a la anterior.
- **Bloques sin cambio:** en la maqueta nueva, las partes que no cambiaron brillan un momento con la misma luz que en la anterior, y una rienda fina las une. Así se ve que Git no las guarda dos veces.
- **Una rama** es un **estandarte** clavado en el pedestal de una maqueta (`main` en blanco, `roof` en naranja). Al hacer commit, el estandarte se mueve al pedestal nuevo.
- **HEAD** es **donde está parado Steve**. Al cambiar de rama (`git switch roof`), Steve camina al otro estandarte y **la casa de verdad cambia** para coincidir con esa maqueta.
- **Merge:** aparece una maqueta nueva amarrada a las dos anteriores (dos riendas), con el techo nuevo y la puerta.
- **Conflicto:** los dos lados cambiaron el mismo bloque (la ventana: vidrio en una rama, vidrio tintado en otra). El bloque parpadea entre los dos y Steve elige uno.
- **El repositorio local** es todo lo que hay en la casa de Steve (casa, cofre, pedestales).
- **El remoto** es una fila de pedestales en **la plaza de la campana**, con su propio estandarte `main`.
  - `git push`: copias de las maquetas viajan a la plaza y el estandarte de ahí avanza.
  - `git pull`: Alex, en otra casa, recibe las copias y su estandarte avanza.
  - **Push rechazado:** Alex subió primero; el estandarte de la plaza ya está en otra maqueta, el aldeano de la plaza niega con la cabeza y Steve primero hace pull, merge y luego push.

## Lugar, hora y luz

- `mundos/savanna-village.json` (aldea de sabana de MacEntorno, centro −1467, 66, 873, radio 80, exportada con `--bioma savanna`). Ya anotada en `lugares.json` para `tech/git`.
- De día, con `makeWorld({ shaders: true })`: oclusión en esquinas, sombras del sol y tone mapping. El target del sol sigue la escena (casa de Steve o plaza).
- Mobs de la zona en el fondo: los aldeanos de la aldea, vacas y gallinas (y caballos si `vida.js` los tiene; si no, no se agregan).
- El terreno no se aplana (`plot`): la aldea se ve como la generó el juego. Las maquetas y pedestales van en lugares libres junto a la casa y en la plaza.

## Animaciones (todas del juego)

| Qué pasa | Cómo lo hace el juego |
|---|---|
| Steve pone o quita un bloque | brazo que golpea, grietas del bloque (`destroy_stage_0..9`), partículas del bloque y el bloque que cae como objeto girando y flotando |
| Bloques al cofre (`git add`) | el objeto vuela al cofre como al recogerlo, con el sonido `pop` |
| Cofre | la tapa abre y cierra con su modelo (`makeChest` ya lo hace), sonidos `chestopen`/`chestclosed` |
| La maqueta aparece (`git commit`) | bloques que se colocan uno a uno con el sonido de colocar madera o piedra |
| Riendas entre pedestales | la rienda del juego con su curva y el sonido `lead_tie` |
| Estandartes | se mecen con el viento como en el juego; al moverse, se rompen y se vuelven a poner |
| Steve camina o cambia de rama | caminata de `gente.js` |
| Merge listo, push aceptado | orbes de experiencia y el aviso "Advancement Made!" |
| Push rechazado | el aldeano niega con la cabeza y el sonido `villager_no` |
| Campana de la plaza | se balancea al sonar, sonido `bell` |

Faltan en el tema (se agregarían con los assets reales del juego): estandartes (`banner` con su modelo), grietas de bloque (`destroy_stage`), riendas entre postes (hay `lead` como objeto) y la cabeza del aldeano negando. Se revisa cada una en el jar y en la wiki antes de dibujarla.

## Narración (borrador, en inglés)

Unas 330 palabras: entre 125 s (2.6 palabras por segundo) y 140 s. Una línea por viñeta en `narration.txt`; los comandos se escriben como se dicen ("git add").

```
0  You spend all day building a house. One wrong move, and the roof is gone. Can you get the old one back?
1  With Git, you can. Git is a time machine for your project. Here's how it really works.
2  When you save with Git, it takes a snapshot of the whole house. That snapshot is called a commit.
3  But first you choose what goes in. Changed blocks go into a chest, called the staging area. That's git add.
4  Then git commit turns the chest into a little model of the house, with a note saying what changed.
5  Each new model is tied to the one before it. Together, the commits are a history you can walk back.
6  Blocks that didn't change aren't saved twice. The new model just points to the old ones, so history stays small.
7  Every commit gets a name made from its content, like a one f three. Change one block, and the name changes.
8  Now, branches. A branch is just a banner standing on a commit. This one is called main.
9  When you commit, the banner moves up to the new model. That's all a branch is. A label that moves.
10 Want to try a crazy roof without risking the house? Make a branch called roof, and switch to it.
11 Steve stands where he's working. Git calls that HEAD. Switch branches, and the real house changes to match.
12 The new roof works. Time to merge. Git makes a new model with two parents, main and roof.
13 If both branches changed the same block, Git won't guess. That's a conflict, and you pick which one stays.
14 So far, all of this lives in Steve's house. That's his local repository.
15 The bell square is the remote, like GitHub. It holds a shared copy everyone can see.
16 git push carries Steve's new commits to the square, and the main banner there moves up.
17 Alex doesn't have them yet. git pull brings the new models to her house and moves her banner too.
18 But if Alex pushed first, Steve's push is rejected. He pulls her work, merges, and then pushes again.
19 That's how a whole team builds the same village without wiping out each other's work.
20 A chain of snapshots, banners that move, and a square everyone shares.
21 That's Git.
```

## Exactitud (lo que el guion afirma)

- Un commit guarda el estado completo de los archivos que Git sigue (un árbol con todos), no un parche. Correcto.
- `git add` pone los cambios en el index (staging area); `git commit` guarda lo que hay en el index, no todo lo que cambió. Correcto.
- Cada commit apunta a su padre (o padres). Correcto.
- Archivos sin cambio no se guardan dos veces: el árbol nuevo apunta al mismo blob. Correcto (Git deduplica por contenido).
- El nombre del commit es un hash de su contenido (árbol, padres, autor, mensaje); si algo cambia, el nombre cambia. "Made from its content" es una simplificación honesta.
- Una rama es un puntero móvil a un commit, y avanza al hacer commit en ella. Correcto.
- HEAD apunta a la rama actual; `git switch` cambia los archivos de trabajo a esa rama. Correcto.
- Merge de dos ramas que divergieron crea un commit con dos padres. Correcto (el caso fast-forward queda fuera).
- Conflicto: los dos lados cambiaron la misma parte; Git se detiene y la persona decide. Correcto.
- Push manda los commits y mueve la rama del remoto; se rechaza si el remoto tiene commits que tú no tienes (no es fast-forward). Pull = fetch + merge. Correcto.
- GitHub es un servicio que aloja remotos; "like GitHub" no dice que Git sea GitHub. Correcto.

## Pasos después de aprobar

1. Revisar en el jar y la wiki los assets que faltan (estandarte, grietas, rienda entre postes, aldeano negando) y agregarlos al tema sin romper los videos anteriores.
2. Elegir la casa de Steve, la de Alex y los lugares de los pedestales en la aldea exportada (cuadros fijos).
3. `narration.txt`, `video.json` (`solo3d`, `formato` 9:16, música) y `descripcion.txt` (100 caracteres o menos).
4. `three/git.html` con un `three/timestamps.json` provisional; revisar cuadros a la mitad de cada línea.
5. Voz clonada (`tts_qwen_clone.py`), revisión con Whisper, borrar el provisional, `palabras.py`, subtítulos.
6. Render, hojas de cuadros al 20, 55 y 90 % de cada línea, loop, renombrar a `How Git Works.mp4` y copiar a `export/`.
