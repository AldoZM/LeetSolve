# Diseño: short "How a Virtual Machine Works", todo en 3D

Estado: **aprobado por Aldo (2026-11-01).** Idea de Aldo (2026-11-01): cómo funciona una máquina virtual (hipervisor, sistema operativo invitado, hardware virtual). Lo demás es propuesta de Claude y está marcado **(propuesta)**.

## Intención

Un short de la línea "cómo funcionan las tecnologías" (`videos/tech/vm/`). Explica qué es una máquina virtual por dentro y en qué se diferencia de un contenedor, para que quede como pareja de los dos de Docker. Alguien que nunca usó una máquina virtual debe entender, solo con ver el mundo, qué es el hardware real, qué hace el hipervisor y qué es un sistema operativo invitado.

## Metas

- Un short vertical (1080 × 1920, 30 fps) de **hasta 3 minutos**, sin estirarlo. El borrador de narración da unos 125 a 135 s.
- Que se lleven seis ideas:
  1. Una **máquina virtual** es una computadora completa hecha de software, que vive dentro de una real.
  2. El **hipervisor** reparte el hardware real (procesador, memoria, disco y red) y le da a cada máquina virtual su **hardware virtual**.
  3. Cada máquina virtual arranca su **sistema operativo completo, con su kernel** (el invitado), y pueden ser sistemas distintos en la misma máquina.
  4. **Aislamiento:** si una se cae o se infecta, las demás y el anfitrión siguen.
  5. Una máquina virtual son archivos: se le puede sacar un **snapshot** y volver a él.
  6. **El precio:** cada una carga un sistema operativo entero. Los contenedores comparten el kernel y arrancan más rápido, pero no pueden usar otro kernel. La nube renta máquinas virtuales.
- Loop: en la última línea todo vuelve al estado del cuadro 0 detrás de la portada, con los subtítulos ocultos mientras sube (`"ocultar"`).
- Todo dentro del mundo 3D: letreros, globos de tooltip y objetos, sin capas 2D encima.

## Fuera del alcance

- Instrucciones de virtualización por nombre (VT-x, AMD-V), anillos de privilegio, paravirtualización, emulación contra virtualización.
- Marcas de hipervisores salvo VirtualBox como ejemplo de tipo 2, sin logo. Sin logos de Windows ni de Linux: los sistemas se distinguen por el estilo de la casa y su globo.
- Migración en vivo, sobreasignación de memoria, GPU virtual.
- Publicar, hacer commit o push: lo decide Aldo.

## No debe pasar (aunque técnicamente funcione)

- Que la narración diga algo falso (ver "Exactitud").
- Que parezca que el hipervisor ejecuta cada instrucción del invitado: casi todo corre directo en el procesador real.
- Que parezca que un contenedor es una máquina virtual pequeña.
- Texto ilegible, cortado o tapado. Globos encimados y la portada cruzando los subtítulos (errores 18 y 19 de `GUIA.md`).
- Repetir las metáforas de Docker tal cual: aquí la máquina virtual es la protagonista.

## La metáfora (propuesta)

**El hardware real** es el **sótano de piedra** de un terreno grande (`host`): cuatro hornos (los núcleos del procesador), una fila de cofres (la memoria), una pared de barriles (el disco) y una vía que sale del terreno (la tarjeta de red). Cada pieza tiene su globo (`CPU: 4 cores`, `RAM`, `disk`, `network`).

**El hipervisor** es un **Illusioner** (el ilusionista del juego), parado en el centro del sótano. Es el mob que crea copias de sí mismo que parecen reales: aquí crea para cada casa hornos y cofres que parecen propios. Sus animaciones y sonido (`illusioner_mirror`) ya están en el tema.

**Cada máquina virtual** es una **casa completa con sus propios cimientos**, construida encima del sótano (la misma casa de la Parte 1 de Docker, con su losa de piedra):
- Adentro, un aldeano (el sistema operativo invitado) con un globo `guest OS + kernel`.
- **Hardware virtual:** hornos y cofres translúcidos dentro de la casa (`virtual CPU`, `virtual RAM`). El aldeano los usa como si fueran suyos.
- **Sistemas distintos:** tres casas de estilos diferentes: madera de roble (`Linux`), cuarzo (`Windows`) y piedra labrada vieja (`old system`).

**Repartir el hardware:** el ilusionista levanta los brazos y de los hornos y cofres del sótano salen rayos hacia cada casa: una recibe dos hornos y cuatro cofres (`2 cores, 4 GB`), otra cuatro y ocho.

**Cómo corre:** el aldeano mete un objeto en su horno translúcido y el horno real del sótano se enciende (`furnace_front_on`). Casi siempre va directo; cuando toca disco o red, la vagoneta baja por la vía y el ilusionista la atiende.

**Aislamiento:** un creeper explota dentro de la casa de piedra vieja (partículas y sonido del juego). La casa queda en ruinas, pero las otras dos siguen trabajando y el sótano no se toca.

**Snapshot:** un cartógrafo hace un **mapa** de la casa (el mapa lleno del juego) antes de la explosión. Después, la casa se reconstruye bloque por bloque a partir del mapa.

**Tipo 1 y tipo 2:** el ilusionista del sótano está parado directo en la piedra (`type 1: on the hardware`). Al lado, la casa de Steve (su computadora con su sistema) tiene un ilusionista pequeño en una mesa, como una app (`type 2: an app, like VirtualBox`).

**La nube:** la toma se abre y el terreno resulta ser uno de muchos en un centro de datos; cada casa lleva el letrero de un cliente distinto (`Alex`, `Steve`, `shop`).

**Contra contenedores:** junto a las casas aparecen los cuartos de vidrio de Docker sobre un mismo piso con el globo `one shared kernel`; se levantan en un segundo mientras una casa nueva todavía se construye.

## Lugar, hora y luz (propuesta)

- Un lugar nuevo de MacEntorno, porque cada video va en un lugar distinto: `mac-09` (loma de abedules con arroyo) o `mac-10` (bosque de abedules con flores). Se elige con cuadros sueltos y se renombra (por ejemplo `vm-creek`) en `lugares.json`. El sótano y las casas se construyen por código encima del terreno, como la plataforma de Docker.
- De día, con `makeWorld({ shaders: true })`.
- Mobs: vacas y ovejas en la loma, un lobo en el bosque y el creeper solo en su línea.
- Música: `living_mice` (188 s), que no usó ningún short de tecnología.

## Animaciones (todas del juego)

- **Ilusionista:** brazos arriba al lanzar el hechizo, el sonido `illusioner_mirror` y partículas de hechizo.
- **Horno real:** cambia a `furnace_front_on` cuando trabaja, como en el juego.
- **Casas:** se colocan bloque por bloque con el sonido de madera y piedra.
- **Creeper:** se infla, parpadea en blanco y explota (`fuse` y `explode`, ya en el tema), con el humo grande.
- **Mapa:** el cartógrafo sostiene el mapa lleno; al restaurar, los bloques vuelven en el orden en que se rompieron.
- **Vagoneta:** `rieles.js` del short de paquetes.
- **Listo:** orbes de experiencia y `levelup`.

Faltan en el tema y se revisan en el jar antes de dibujarlos: textura del creeper (ya está en `mobs/`), bloques de cuarzo (ya están) y partículas de hechizo.

## Narración (borrador en inglés)

Unas 330 palabras (entre 125 y 135 s). Una línea por viñeta en `narration.txt`.

```
0  Your laptop runs Windows. But one project needs Linux, and another needs an old system. Do you buy three computers?
1  No. You run virtual machines. Whole computers made of software, living inside your real one. Here's how.
2  Start with the real machine. A processor, memory, a disk and a network card. That's the hardware.
3  Normally one operating system owns all of it. To share it, you need a referee, called a hypervisor.
4  The hypervisor splits the real hardware. This machine gets two cores and four gigabytes. That one gets four cores and eight.
5  Each virtual machine sees its own processor, its own memory and its own disk. They're virtual, but to the guest they look real.
6  Most of the guest's work runs straight on the real processor. When it touches the hardware, the hypervisor steps in.
7  Inside, each one boots a full operating system, kernel and all. That's called the guest.
8  And the guests don't have to match. Linux, Windows and an old system can run side by side on one machine.
9  Each one is sealed off. If one crashes, or gets a virus, the others keep running, and so does the host.
10 A virtual machine is just files on a disk. So you can take a snapshot, a copy of its whole state, at any moment.
11 Break something? Roll back to the snapshot, and the machine is exactly as it was.
12 Some hypervisors run straight on the hardware, like in a data center. Others run as an app on your computer, like VirtualBox.
13 That's what the cloud rents you. A cloud server is usually a virtual machine on someone else's hardware.
14 The price? Every virtual machine carries a whole operating system. That takes memory, and it can take a minute to boot.
15 Containers skip that. They share the host's kernel, so they start in a second. But they can't bring a different kernel.
16 So virtual machines give you whole computers, fully separated. Containers give you light, fast apps.
17 Real hardware, a hypervisor that splits it, and full operating systems running side by side.
18 That's a virtual machine.
```

## Exactitud (lo que el guion afirma)

- Una máquina virtual emula una computadora completa (procesador, memoria, disco, red) y corre un sistema operativo completo. Correcto.
- El hipervisor reparte y aísla el hardware real entre máquinas virtuales. Correcto (tipo 1 o tipo 2).
- "Most of the guest's work runs straight on the real processor. When it touches the hardware, the hypervisor steps in": con virtualización asistida por hardware, el código del invitado corre directo en el procesador y las operaciones privilegiadas y de entrada y salida pasan al hipervisor. Correcto como simplificación; no se nombran VT-x ni AMD-V.
- Invitados distintos en el mismo anfitrión (Linux y Windows). Correcto.
- Aislamiento: una caída o un virus en un invitado no afecta a los otros ni al anfitrión en el caso normal; los escapes de máquina virtual existen pero son raros. "Keep running" es correcto para el ejemplo.
- Una máquina virtual se guarda en archivos (disco virtual y configuración); un snapshot guarda el estado del disco y, opcionalmente, de la memoria, y se puede volver a él. Correcto.
- Tipo 1 (sobre el hardware: centros de datos) y tipo 2 (app sobre un sistema operativo: VirtualBox). Correcto.
- "A cloud server is usually a virtual machine": las instancias normales de la nube son máquinas virtuales; también existen servidores dedicados ("bare metal"), por eso dice "usually".
- "It can take a minute to boot": un sistema operativo completo tarda de segundos a minutos. "Can take" es honesto.
- Los contenedores comparten el kernel del anfitrión y no pueden usar otro kernel. Correcto en Linux (en Mac y Windows, Docker usa una máquina virtual por debajo; queda fuera del alcance, como en Docker).

## Pasos después de aprobar

1. Elegir entre `mac-09` y `mac-10` con cuadros sueltos; fijar el sótano, las casas, la casa de Steve y el lugar de los contenedores.
2. Revisar en el jar las partículas de hechizo y lo que falte; agregarlo a `extraer.py`.
3. `narration.txt`, `video.json` (`solo3d`, 9:16, música) y `descripcion.txt`.
4. Voz clonada (sola, sin render en paralelo) y revisión con Whisper `small.en`.
5. `three/vm.html`, cuadros fijos a 25 y 75 % de cada línea; correcciones.
6. `palabras.py`, subtítulos, render, revisión con cuadros al 20, 55 y 90 % de cada línea, inicio y final.
7. `export/How a Virtual Machine Works.mp4`, descripción en `export/descripciones-tecnologia.md` y entrada en `BITACORA.md`.

## Lo que cambió al construirlo

- **Lugar:** `mac-12`, renombrado `vm-basin` (cuenca de arena con abedules y terrazas al este). `mac-09` y `mac-10` ya estaban usados (`birch-creek` y `birch-grove`). Giro 0: la escena usa las coordenadas de la exportación.
- **Distribución en capas, vista de frente:** las casas atrás (z 5..9), el Illusioner en medio (z 12) y la fila de hardware al frente (z 16), porque es baja y deja ver todo. Con las casas al frente tapaban al hipervisor y al hardware.
- **Hardware:** 8 hornos (núcleos), 16 cofres en dos filas (GB), 6 barriles (disco) y un tramo de riel con vagoneta (red). El reparto se marca con marcos de color en las piezas reales: VM 1 verde (2 núcleos, 4 cofres), VM 2 azul (4 y 8), VM 3 naranja (2 y 4).
- **Hardware virtual:** horno, barril y cofre translúcidos dentro de cada casa; el horno virtual se enciende junto con su horno real.
- **Snapshot:** el cartógrafo saca el mapa de la VM 3 en silencio al final de la línea 8 (antes del creeper) y lo muestra en las líneas 10 y 11, cuando la casa se reconstruye en orden inverso.
- **Casa de Steve (laptop):** casa de cuarzo en la parte plana de la cuenca (x −4..0, z 19..23) con un patio de piedra al frente; en la línea 12 aparecen en su mesa un Illusioner pequeño y una casita (tipo 2).
- **Centro de datos:** dos plataformas más con casas suben detrás en la línea 13. **Contenedores:** dos cuartos de vidrio sobre un piso de piedra al este de la plataforma, junto a la VM 4 que se construye despacio.
- Sin partículas de hechizo nuevas: el hechizo usa `trade_glint` teñido de morado.

