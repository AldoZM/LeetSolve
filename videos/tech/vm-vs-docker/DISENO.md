# Diseño: short "VM vs Docker", todo en 3D

Estado: **Aldo pidió seguir (2026-11-01)**, tomado como aprobado. Pedido de Aldo (2026-11-01): la comparación entre máquinas virtuales y Docker, después de "How Teams Really Use Virtual Machines". Lo demás es propuesta de Claude y está marcado **(propuesta)**.

## Intención

Un short que pone lado a lado las dos tecnologías de los cuatro shorts anteriores (Docker 1 y 2, máquina virtual 1 y 2) y responde "¿cuál uso?". La respuesta honesta es "depende, y casi siempre las dos juntas". Reusa las dos metáforas ya vistas: la **casa con sus propios cimientos** (máquina virtual) y el **cuarto de vidrio sobre un piso compartido** (contenedor), así quien vio los otros reconoce todo al instante.

## Metas

- Un short vertical (1080 × 1920, 30 fps) de **hasta 3 minutos**. El borrador da unos 130 s.
- Que se lleven cinco ideas:
  1. Ponen las paredes en **niveles distintos**: la máquina virtual imita el **hardware** y trae su sistema operativo completo; el contenedor es un **proceso** del anfitrión, cercado por el **kernel compartido**.
  2. Por eso el contenedor es más **chico**, **arranca más rápido** y **caben más** en la misma máquina.
  3. La máquina virtual tiene la **pared más gruesa**: un kernel por máquina. Un fallo del kernel compartido pone en riesgo a todos los contenedores del anfitrión; por eso las nubes separan clientes con máquinas virtuales.
  4. Solo la máquina virtual corre **otro sistema** (Windows en un servidor Linux) o software viejo que espera una máquina completa.
  5. **Cuándo usar cada una**, y que en la práctica **se apilan**: los contenedores corren dentro de máquinas virtuales (hasta Docker Desktop usa una pequeña con Linux).
- Loop y reglas de siempre (todo en 3D, subtítulos ocultos cuando sube la portada).

## Fuera del alcance

- gVisor, Kata, Firecracker y microVMs por nombre (la idea de "las nubes separan clientes con máquinas virtuales" las cubre).
- WSL2, Hyper-V, contenedores de Windows.
- Números exactos de rendimiento.
- Publicar, commit o push: lo decide Aldo.

## No debe pasar

- Que parezca que un contenedor es inseguro o que una máquina virtual es lenta "siempre": son compromisos.
- Que la narración diga algo falso (ver "Exactitud").
- Repetir explicaciones largas de los shorts anteriores: aquí todo es comparación.

## La metáfora (propuesta)

**Una cancha partida en dos** (cambio al construirlo: en vertical se lee mejor adelante y atrás que izquierda y derecha): las casas (`VM`) adelante y los cuartos de vidrio (`containers`) atrás, separados por una línea de lana roja. La cámara alta las pone abajo y arriba del cuadro.

- **Niveles distintos:** a la izquierda, una casa con sus cimientos de piedra, y adentro el aldeano y el globo `own OS + kernel`; el Illusioner atrás (imita el hardware). A la derecha, cuartos de vidrio sobre un piso de piedra lisa que brilla con el globo `one shared kernel`.
- **Tamaño:** la imagen de la máquina virtual es una **pila de cofres** grande (`~ GBs`) y la del contenedor una sola **caja de shulker** (`~ MBs`), las de Docker.
- **Velocidad:** una carrera. Suena la campana: la casa se construye bloque por bloque mientras del otro lado los cuartos aparecen en un segundo y se ponen a vender.
- **Cuántos caben:** en el mismo terreno, 4 casas contra 12 cuartos (20 al final).
- **Grosor de la pared:** un saqueador (vindicator) entra a una casa: solo esa casa se oscurece, las otras tienen sus cimientos. Del otro lado, el saqueador rompe el piso compartido: la grieta (`destroy_stage`) corre bajo todos los cuartos y todos se ponen en rojo (`at risk`).
- **Las nubes:** casas con el nombre de distintos clientes (`Alex`, `Steve`, `shop`), cada uno en su casa.
- **Otro sistema y software viejo:** del lado VM aparecen una casa de cuarzo (`Windows on a Linux host`) y una de piedra vieja (`old software`); del lado de contenedores, un cuarto de cuarzo intenta aparecer y la barrera lo detiene (`no other kernel`).
- **Ventajas del contenedor:** la pila de shulkers viaja en el bote de Docker y diez cuartos aparecen antes de que una casa termine.
- **Cuándo usar cada una:** dos libros en atriles, uno por lado, con la lista corta.
- **Las dos juntas:** la cancha se junta: los cuartos de vidrio entran en una casa. Al final, la casa-laptop de Steve con una casita adentro y cuartos dentro de ella (`Docker Desktop: a small Linux VM`).

## Lugar, hora y música (propuesta)

- Un lugar nuevo: `mac-01` (arena con abedules y el mar al sur), renombrado `vs-shore` en `lugares.json`. La cancha y la plataforma se construyen por código.
- De día con `shaders`.
- Música: `minecraft` (261 s), que no usó ningún short de tecnología.

## Narración (borrador en inglés)

Unas 330 palabras (entre 125 y 135 s).

```
0  Virtual machines and Docker containers both run apps in their own space. So which one should you use?
1  They put the walls at different levels. Here's the difference, side by side.
2  A virtual machine imitates the hardware. On top, it runs a whole operating system, kernel and all, and then your app.
3  A container doesn't imitate hardware. It's a process on the host, fenced off by the host's own kernel.
4  That changes the size. A VM image is often gigabytes. A container image can be a few megabytes.
5  It changes the speed. A VM boots a whole system, often in a minute. A container starts in about a second.
6  And it changes how many fit. Where a handful of VMs run, you can pack many more containers.
7  But the walls aren't equally thick. Each VM has its own kernel, so an attacker has to break out of a whole machine.
8  Containers share one kernel. If an attacker finds a bug in it, every container on that host is at risk.
9  That's why clouds keep different customers in separate virtual machines, not just separate containers.
10 Need a different system? A VM can run Windows on a Linux server. A container can't bring its own kernel.
11 Old software that expects a full machine? That's a job for a VM too.
12 But for your own apps, containers are hard to beat. Small images, fast builds, and deploys in seconds.
13 They scale fast too. More copies are running before one VM finishes booting.
14 So, use a VM when you need another operating system, the strongest walls, or a whole machine to control.
15 Use containers when you ship your own services, many of them, and often.
16 And most of the time, it's both. Containers run inside VMs. Even Docker Desktop runs a small Linux VM.
17 Virtual machines imitate the hardware. Containers share the kernel. Teams stack them.
18 That's VM versus Docker.
```

## Exactitud

- La máquina virtual virtualiza el hardware y corre un sistema operativo invitado completo; el contenedor es un proceso aislado con namespaces y cgroups del kernel del anfitrión. Correcto ("imitates" es una simplificación honesta de "virtualiza").
- Tamaños: imágenes de máquina virtual de varios GB; imágenes de contenedor desde unos MB (Alpine ~ 5 MB). "Often" y "can be". Correcto.
- Arranque: un sistema completo de segundos a minutos; un contenedor en menos de un segundo a unos segundos. "Often" y "about". Correcto.
- Densidad: muchos más contenedores que máquinas virtuales en el mismo anfitrión, porque no repiten el sistema. Correcto como regla general.
- Seguridad: un escape por una falla del kernel compartido afecta a los contenedores del anfitrión; por eso los proveedores separan clientes con máquinas virtuales o microVMs. Correcto.
- Una máquina virtual puede correr Windows en un anfitrión Linux; un contenedor usa el kernel del anfitrión. Correcto.
- Docker Desktop en Mac y Windows corre una máquina virtual pequeña con Linux. Correcto.

## Pasos después de aprobar

1. Revisar `mac-01` con cuadros sueltos y renombrarlo `vs-shore`; `extraer.py`: vindicator ya está, falta revisar la textura de la campana si se usa.
2. `narration.txt`, `video.json` (música `minecraft`), `descripcion.txt`; voz (sola) y Whisper `small.en`.
3. `three/vmvsdocker.html` con piezas de `docker.html` y `vm.html`; cuadros fijos a 30 y 75 % de cada línea.
4. `palabras.py`, subtítulos, render, revisión con 59 cuadros, `export/VM vs Docker.mp4`, descripción y bitácora.
