# Diseño: shorts de la nube ("How Cloud Services Work" y "How Teams Really Use Cloud Services"), todo en 3D

Estado: **pedido de Aldo (2026-11-01)**: un short de servicios en la nube (GCP, AWS y Azure) y luego su Parte 2 de uso en equipo, como Docker y la máquina virtual. Lo demás es propuesta de Claude y está marcado **(propuesta)**.

## Intención

- **Parte 1, `videos/tech/cloud/` ("How Cloud Services Work"):** qué es la nube, quiénes son AWS, Azure y Google Cloud, qué venden (los mismos bloques con nombres distintos), los niveles de servicio, las regiones y cómo se cobra.
- **Parte 2, `videos/tech/cloud-teams/` ("How Teams Really Use Cloud Services"):** cómo la usa un equipo: cuentas y permisos, entornos separados, servicios administrados, costos bajo control, monitoreo, respaldo en otra región y la decisión de una o varias nubes.

Las dos van en el mismo lugar, con los mismos personajes, y cierran la serie de infraestructura (Docker 1 y 2, máquina virtual 1 y 2, VM vs Docker).

## Metas

- Dos shorts verticales de **hasta 3 minutos** cada uno; los borradores dan unos 130 s.
- **Parte 1**, seis ideas:
  1. La **nube** es rentar computadoras, discos y redes de los centros de datos de otro, por minuto, en lugar de comprar servidores.
  2. Los tres grandes: **AWS** (Amazon, el primero y el más grande), **Microsoft Azure** y **Google Cloud**. Venden los mismos bloques con nombres distintos.
  3. Los bloques básicos: **cómputo** (máquinas virtuales: EC2, Azure Virtual Machines, Compute Engine), **almacenamiento de objetos** (S3, Blob Storage, Cloud Storage), **bases de datos administradas** y **redes privadas**.
  4. **Niveles:** infraestructura (rentas la máquina y cuidas el sistema), plataforma (das el código y ellos lo corren) y software terminado (como el correo). **Serverless:** funciones que solo corren y cobran cuando llega una petición.
  5. **Regiones y zonas** en todo el mundo: eliges dónde viven tus datos y cerca de tus usuarios.
  6. **Pago por uso** y **responsabilidad compartida**: ellos cuidan los edificios y el hardware; tú, tu configuración, tus datos y quién entra.
- **Parte 2**, seis ideas:
  1. **Cuentas y permisos (IAM):** cada persona y cada servicio con el mínimo permiso; nadie usa la cuenta raíz; doble factor.
  2. **Entornos separados:** desarrollo, pruebas y producción en cuentas o proyectos distintos.
  3. **Servicios administrados** antes que armarlo a mano: la base de datos con respaldos y réplica la cuida el proveedor.
  4. **Costos:** presupuestos y alertas, etiquetas por equipo, apagar lo que no se usa, descuentos por compromiso y máquinas *spot* baratas que se pueden perder.
  5. **Monitoreo y alertas:** métricas y registros en un tablero; si algo falla, avisa a la persona de guardia.
  6. **Respaldo en otra región** y **una nube principal**: la mayoría de los equipos se queda en una (y acepta depender de ella); varias nubes cuestan más de lo que parece.

## Fuera del alcance

- Listas largas de servicios, precios exactos, certificaciones.
- Comparar cuál nube es mejor: el short no recomienda una.
- Kubernetes por dentro, redes avanzadas, CDN (ya salió en DNS).
- Publicar: se sube a Drive al terminar (regla de Aldo); el commit y push al terminar cada sección.

## No debe pasar

- Logos de AWS, Azure o Google Cloud (ni sus colores como marca reconocible en un logo). Los nombres en texto sí.
- Que parezca que una nube es "la buena".
- Que la narración diga algo falso (ver "Exactitud").
- Lo de siempre: globos encimados, letreros cruzando los subtítulos.

## La metáfora (propuesta)

**La nube es literal:** islas flotando en el cielo sobre el mar, hechas por código encima del lugar `mac-11` (mar abierto), renombrado `cloud-sea`. Abajo, en la orilla, la casa de Steve (su computadora) y su pequeño servidor de la Parte 1 de Docker.

- **Rentar en lugar de comprar:** Steve tiene un solo servidor (una casa) que se llena; en vez de construir más, sube por una escalera de andamios a las islas y **renta** una casa con esmeraldas que caen por minuto (un contador `emeralds / minute`).
- **Los tres grandes:** tres islas grandes, cada una con su mercado de aldeanos y un estandarte de un color sin logo: `AWS`, `Azure`, `Google Cloud` en letreros. Los tres tienen los mismos puestos:
  - Cómputo = una casa (la máquina virtual de los shorts anteriores), con los tres nombres: `EC2`, `Azure VMs`, `Compute Engine`.
  - Almacenamiento de objetos = **cubetas** (el *bucket* del juego), con `S3`, `Blob Storage`, `Cloud Storage`.
  - Base de datos administrada = estantes de libros con un bibliotecario que los cuida.
  - Red privada = una cerca alrededor del terreno rentado.
- **Niveles:** tres puestos uno tras otro:
  - Infraestructura: rentas el terreno y la casa vacía; Steve pone sus bloques.
  - Plataforma: Steve entrega un libro (su código) y un aldeano arma y corre el puesto.
  - Software: una casa ya terminada con el letrero `email`.
  - Serverless: un **dispensador** con un botón: cada vez que un cliente lo aprieta sale una esmeralda y se cobra una moneda; si nadie aprieta, no cobra.
- **Regiones y zonas:** un mapa del mundo en un marco (el mapa del juego) con islas marcadas en varios lugares; Steve escoge la más cercana a sus clientes.
- **Pago por uso:** el contador de esmeraldas sube rápido con muchas casas y baja al quitarlas.
- **Responsabilidad compartida:** la isla y sus cimientos los cuida un gólem del proveedor; la puerta y el cofre de Steve los cuida Steve (si deja la puerta abierta, entra un saqueador).

**En la Parte 2:**
- **IAM:** cada aldeano del equipo con una **llave** distinta que solo abre su puerta; la cuenta raíz es un cofre con candado que nadie abre; doble factor = la llave más un **reloj** que cambia.
- **Entornos:** tres islas pequeñas: `dev`, `staging` y `prod`, conectadas en ese orden por un riel.
- **Servicios administrados:** el bibliotecario de la base de datos hace copias de los libros solo, y si su estante se quema, otro estante igual ya tiene todo.
- **Costos:** un tablero de esmeraldas con una **campana** que suena al pasar el presupuesto; etiquetas (nametags) en cada casa por equipo; de noche las casas de `dev` se apagan; una casa *spot* barata desaparece con aviso y otra la reemplaza.
- **Monitoreo:** un mapa-tablero con luces de redstone por servicio; una se pone roja y la campana despierta a la persona de guardia.
- **Otra región:** una isla gemela lejos, con copias; cuando una isla se nubla, el riel manda a los clientes a la otra.
- **Una nube principal:** Steve tiene sus casas en una sola isla; tender puentes a las tres islas cuesta mucho (cada puente con su peaje de esmeraldas).

## Lugar, hora y música (propuesta)

- `mac-11` (mar abierto), renombrado `cloud-sea`. Las islas flotan a unos 25 bloques de altura, con nubes del juego alrededor.
- De día con `shaders`.
- Música: Parte 1 `sweden` (230 s; tiene una pausa propia de 10 s a los 127 s, así que se revisa que no caiga en un momento importante; si cae, `wet_hands` + otra), Parte 2 `minecraft` si VM vs Docker no la usa, si no `mice_on_venus`.

## Narración, Parte 1 (borrador en inglés)

```
0  Steve's shop outgrew his one server. Buy ten more machines and a building to keep them in? There's a better way.
1  Rent them. That's the cloud. Someone else's data centers, by the minute, from anywhere.
2  Three companies run most of it. Amazon Web Services, the first and the biggest. Microsoft Azure. And Google Cloud.
3  They sell the same building blocks, with different names. Here are the main ones.
4  Compute. Virtual machines you rent. E C 2 on AWS, Azure Virtual Machines, and Compute Engine on Google Cloud.
5  Storage. Buckets where you drop files of any size. S 3, Azure Blob Storage, and Google Cloud Storage.
6  Databases they run for you, with backups and copies included. And private networks to wire it all together.
7  You choose how much to manage. Rent bare machines, and you run the system yourself. That's infrastructure as a service.
8  Hand over your code, and they run it. That's a platform. Or use finished software, like email. That's software as a service.
9  Or go serverless. A function wakes up only when a request comes in, and you pay only for that moment.
10 All of this lives in regions around the world. Each region has zones, separate data centers.
11 You pick a region close to your users, and keep copies in more than one zone.
12 You pay for what you use. Ten machines for an hour cost about the same as one machine for ten hours.
13 That's why you can start small, and grow in minutes, without buying a single server.
14 But it cuts both ways. A machine you forget keeps running, and keeps billing.
15 And security is shared. The provider guards the buildings and the hardware.
16 You guard everything you put there. Your settings, your data, and who gets in.
17 Rented building blocks, three big providers, regions everywhere, and you pay for what you use.
18 That's how cloud services work.
```

## Narración, Parte 2 (borrador en inglés)

```
0  Steve's team is in the cloud now. Five people, three apps, one bill. Here's how teams keep it under control.
1  First, who can do what. Every person and every service gets its own identity, with only the permissions it needs.
2  Nobody uses the main root account day to day. It's locked away, with a second factor on every login.
3  Next, environments. Development, staging and production live in separate accounts or projects.
4  A mistake in development can't touch the real users. Changes move up step by step.
5  Teams also let the provider run the hard parts. A managed database takes backups and keeps a standby copy by itself.
6  If its machine fails, the standby takes over in a minute or two. Nobody gets paged at three A M to fix a disk.
7  Then, money. Every resource gets tags, like which team and which app, so the bill makes sense.
8  Budgets send an alert before the month goes over. Development machines shut down at night.
9  Steady servers get a discount for a one or three year commitment. Batch jobs run on spot machines, cheap, but they can be taken back.
10 Everything is watched. Metrics and logs flow into dashboards, and alerts fire when something looks wrong.
11 An alert pages whoever is on call, with a link to the exact graph that broke.
12 For disasters, backups are copied to another region, far away.
13 If a whole region goes down, the team can bring the app back up in the other one.
14 And how many clouds? Most teams pick one main provider and go deep.
15 Spreading across all three means three sets of tools, skills and bills. Some teams still do it, for very good reasons.
16 Staying in one cloud means depending on it. Teams accept that trade, with their eyes open.
17 Tight permissions, separate environments, managed services, and a close eye on the bill.
18 That's how teams really use cloud services.
```

## Exactitud

**Parte 1:**
- AWS lanzó sus primeros servicios públicos en 2006 y es el proveedor con más participación de mercado; Azure y Google Cloud le siguen. "The first and the biggest" es correcto entre los tres.
- Nombres: EC2, Azure Virtual Machines, Compute Engine; S3, Azure Blob Storage, Cloud Storage. Correctos.
- IaaS, PaaS y SaaS como se describen; serverless (Lambda, Azure Functions, Cloud Run functions) cobra por invocación y tiempo de ejecución. Correcto.
- Regiones con varias zonas de disponibilidad (centros de datos separados). Correcto en los tres.
- "Ten machines for an hour cost about the same as one machine for ten hours": con cobro por segundo u hora y el mismo tipo de máquina, es correcto ("about").
- Modelo de responsabilidad compartida: el proveedor protege la infraestructura; el cliente su configuración, datos e identidades. Correcto.

**Parte 2:**
- IAM con privilegio mínimo; la cuenta raíz guardada con MFA es la práctica recomendada de los tres. Correcto.
- Cuentas o proyectos separados por entorno (AWS Organizations, proyectos de GCP, suscripciones de Azure). Correcto.
- Bases administradas con respaldos automáticos y réplica de espera con conmutación automática (Multi-AZ, alta disponibilidad): "a minute or two" es el orden real. Correcto.
- Etiquetas para costos, presupuestos con alertas, apagar desarrollo de noche, descuentos por compromiso de 1 o 3 años (Reserved Instances, Savings Plans, committed use) y máquinas spot que el proveedor puede recuperar. Correcto.
- Monitoreo y alertas con guardia (CloudWatch, Azure Monitor, Cloud Monitoring + PagerDuty u otros). Correcto sin marcas.
- Respaldos entre regiones y recuperación en otra región. Correcto.
- La mayoría usa un proveedor principal; multi-nube agrega costo operativo. "Some teams still do it, for very good reasons" deja lugar a los casos reales.

## Pasos

1. Elegir la altura y forma de las islas sobre `mac-11` con cuadros sueltos; renombrar `cloud-sea`.
2. `extraer.py`: cubeta (`bucket`), dispensador, botón, reloj y marco de mapa si faltan.
3. Parte 1 completa (voz sola, cuadros, render, revisión, `export/How Cloud Services Work.mp4`, Drive).
4. Parte 2 completa en `videos/tech/cloud-teams/` (`export/How Teams Really Use Cloud Services.mp4`, Drive).
5. Descripciones, bitácora, commit y push.
