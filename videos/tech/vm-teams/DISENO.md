# Diseño: short "How Teams Really Use Virtual Machines", todo en 3D

Estado: **Aldo pidió seguir (2026-11-01)**, tomado como aprobado. Pedido de Aldo (2026-11-01): la Parte 2 de la máquina virtual, como "How Teams Really Use Docker". Lo demás es propuesta de Claude y está marcado **(propuesta)**.

## Intención

Segunda parte de `videos/tech/vm/`. La Parte 1 explicó qué es una máquina virtual por dentro; esta cuenta cómo la usa un equipo real en la nube: nadie arma servidores a mano, todo sale de una imagen y de un archivo, las máquinas son desechables y los datos viven aparte. Termina con los contenedores corriendo dentro de máquinas virtuales, para enlazar con el short de comparación.

## Metas

- Un short vertical (1080 × 1920, 30 fps) de **hasta 3 minutos**. El borrador da unos 130 s.
- Que se lleven seis ideas:
  1. Una **golden image** (imagen base) trae el sistema, las actualizaciones y la app; cada máquina nueva es una **copia** idéntica.
  2. Las máquinas se describen en un archivo (**infraestructura como código**) y un comando las crea o las borra.
  3. Un **balanceador de carga** reparte a los usuarios, y el **autoescalado** agrega o quita copias según la gente (y el costo).
  4. Las máquinas son **desechables**: los datos van en **discos aparte** que sobreviven a la máquina, con **snapshots** de respaldo cada noche.
  5. **Red privada y firewall:** solo el balanceador da a internet; para entrar, **llave SSH** por una máquina de guardia (**bastion**).
  6. **Alta disponibilidad:** copias en **zonas** distintas; algunas nubes mueven una máquina viva de anfitrión (**live migration**). Y adentro de muchas máquinas virtuales corren **contenedores**.
- Loop: en la última línea todo vuelve al estado del cuadro 0 detrás de la portada, con los subtítulos ocultos mientras sube.
- Todo dentro del mundo 3D, sin capas 2D encima.

## Fuera del alcance

- Marcas de nubes y herramientas (AWS, Terraform, Ansible) salvo como palabra genérica; sin logos.
- Precios exactos, tipos de instancia, Kubernetes por dentro.
- Publicar, commit o push: lo decide Aldo.

## No debe pasar

- Que la narración diga algo falso (ver "Exactitud").
- Repetir la Parte 1: aquí no se explica otra vez el hipervisor.
- Globos encimados, letreros cruzando los subtítulos (errores 18 y 19 de `GUIA.md`).

## La metáfora (propuesta)

Mismo lugar que la Parte 1 (`vm-basin`), con la plataforma del hardware y las casas. La "nube" es el centro de datos de la Parte 1: varias plataformas (anfitriones) con casas (máquinas virtuales).

- **Golden image:** un **mapa** del cartógrafo con la casa ya armada (sistema, actualizaciones y el puesto de la app). Se **copia en la mesa de cartografía** (como en el juego) y de cada copia sale una casa idéntica.
- **Infraestructura como código:** un **libro y pluma** `infra` en un atril con `count: 3`, `size: 2 cores`, `network: private`. Cambiar `3` por `5` levanta dos casas más; borrar la línea las quita.
- **Balanceador de carga:** un **aldeano en la puerta** de la cerca con una campana: los clientes llegan y él los manda a una casa distinta cada vez.
- **Autoescalado:** de día llega mucha gente y aparecen casas nuevas a partir del mapa; al atardecer se van y las casas desaparecen (globo `fewer machines, lower bill`).
- **Máquinas desechables y discos aparte:** cada casa tiene un **barril** afuera, unido con una rienda (el disco). Una casa se rompe; el barril se queda y una casa nueva se amarra al mismo barril.
- **Snapshots de respaldo:** de noche, una copia de cada barril (un mapa pequeño) viaja a un **cofre** lejano (`backups`).
- **Red privada y firewall:** cerca alrededor de las casas; solo la puerta del balanceador da afuera. Un saqueador (vindicator) choca con la cerca.
- **SSH y bastion:** Steve trae una **llave** (`trial_key` del juego) y entra por una **caseta de guardia** junto a la cerca (el bastion), y desde ahí a una casa.
- **Live migration:** el Illusioner levanta una casa con el aldeano trabajando y la lleva a otra plataforma mientras el puesto sigue vendiendo.
- **Zonas:** dos grupos de plataformas separadas por agua; uno se apaga (se oscurece) y el otro sigue vendiendo.
- **Contenedores adentro:** el techo de una casa se vuelve transparente y adentro hay cuartos de vidrio de Docker.

## Lugar, hora y música (propuesta)

- `vm-basin`, como la Parte 1. Lo nuevo (cerca, caseta, mesa de cartografía, segunda zona) se construye por código.
- De día con un atardecer breve para el autoescalado (las horas de `vida.js`; solo se probó de día con `shaders`, así que el atardecer se revisa con cuadros sueltos y, si no se ve bien, se cambia por un reloj del juego).
- Música: `danny` (255 s), que no usó ningún short de tecnología.

## Narración (borrador en inglés)

Unas 330 palabras (entre 125 y 135 s).

```
0  Steve's team runs its app on virtual machines. But nobody builds them by hand. Here's how teams really do it.
1  It starts with an image. A golden image is a disk saved with the system, the updates and the app already installed.
2  Every new machine is a copy of that image. Ten servers, ten clones, all exactly the same.
3  The machines themselves are described in code. A file says how many, how big, and on which network.
4  One command, and the cloud builds them. Change the file, run it again, and the cloud matches it. That's infrastructure as code.
5  Users don't hit one machine. A load balancer sits in front and spreads them across all of them.
6  When the crowd grows, autoscaling adds more copies of the image. When it shrinks, it removes them, and you stop paying.
7  So every machine must be disposable. Any one can disappear, and nothing important is lost.
8  That's why the data lives on separate disks. A disk can outlive its machine and be attached to a new one.
9  And every night, snapshots of those disks are copied away as backups.
10 The machines sit on a private network. Only the load balancer faces the internet. A firewall blocks the rest.
11 To get inside, an engineer uses an S S H key, often through one guarded machine, called a bastion.
12 Some clouds can even move a running machine to another host while it works. That's live migration.
13 And for safety, copies run in different zones, separate data centers. If one goes dark, the others keep serving.
14 Look inside many of these machines, and you'll find something else. Containers.
15 In the cloud, containers usually run inside virtual machines. The machine gives the hard walls, the containers pack the apps.
16 So teams don't pick one. They stack them.
17 Golden images, machines as code, autoscaling behind a load balancer, and data on separate disks.
18 That's how teams really use virtual machines.
```

## Exactitud

- Golden image: una imagen de disco preparada (AMI, imagen personalizada) de la que se crean instancias idénticas. Correcto.
- Infraestructura como código: herramientas como Terraform comparan el archivo con lo que existe y crean, cambian o borran recursos. "The cloud matches it" lo dice sin marcas. Correcto.
- Balanceador de carga y grupos de autoescalado que agregan o quitan instancias según métricas; en la nube se paga por tiempo de uso. Correcto.
- Discos persistentes separados de la instancia (EBS, persistent disk) que se pueden desconectar y conectar a otra; snapshots de discos como respaldo. Correcto.
- Subred privada con firewall o grupos de seguridad; acceso por SSH con llave, a menudo por un bastion. Correcto (hay alternativas modernas, fuera del alcance).
- Live migration: Google Cloud la usa en mantenimiento; no todas las nubes. Por eso "some clouds". Correcto.
- Zonas de disponibilidad: centros de datos separados dentro de una región. Correcto.
- Contenedores dentro de máquinas virtuales: los nodos de Kubernetes administrado son máquinas virtuales. "Usually" es honesto.

## Pasos después de aprobar

1. `narration.txt`, `video.json` (música `danny`), `descripcion.txt`; voz (sola) y Whisper `small.en`.
2. Revisar en el jar la mesa de cartografía, la llave (`trial_key`) y la campana; agregarlas a `extraer.py`.
3. `three/vmteams.html` con piezas de la Parte 1; cuadros fijos a 30 y 75 % de cada línea.
4. `palabras.py`, subtítulos, render, revisión con 59 cuadros, `export/How Teams Really Use Virtual Machines.mp4`, descripción y bitácora.
