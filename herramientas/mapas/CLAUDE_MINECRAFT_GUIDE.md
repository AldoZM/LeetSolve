# 🧭 Minecraft Structure & Biome Locator (Guía para Claude y Agentes)

Esta herramienta permite a **Claude** (o cualquier asistente/script) inspeccionar, ubicar y extraer coordenadas exactas de aldeas, estructuras y biomas de los mundos de Minecraft Java instalados en el sistema (Overworld, Nether y The End).

---

## 📁 Archivos Disponibles

* **Script ejecutable:** `herramientas/mapas/minecraft_locator.py`
* **Datos Overworld JSON (Mundo MAC / MacEntorno):** `herramientas/mapas/mac_entorno_structures.json`
* **Datos Nether JSON (Mundo MAC / MacEntorno):** `herramientas/mapas/mac_entorno_nether.json`

---

## ⚡ Comandos para Claude y Terminal

### 1. Listar mundos disponibles y su información
```bash
python3 herramientas/mapas/minecraft_locator.py list
```

### 2. Localizar estructuras y aldeas en el Overworld
```bash
python3 herramientas/mapas/minecraft_locator.py locate --world MacEntorno --type all --json
```

### 3. Localizar estructuras y biomas en el Nether
Calcula automáticamente el punto de entrada relativo en el Nether según la posición del jugador en el Overworld (coordenadas / 8):
```bash
python3 herramientas/mapas/minecraft_locator.py locate --world MacEntorno --dimension nether --json
```

### 4. Consultar The End (Ciudades del End)
```bash
python3 herramientas/mapas/minecraft_locator.py locate --world MacEntorno --dimension end --json
```

### 5. Buscar desde coordenadas personalizadas
```bash
python3 herramientas/mapas/minecraft_locator.py locate --world MacEntorno --dimension nether --pos 0 0 --json
```

---

## 🗺️ Ejemplo de Salida Nether (`mac_entorno_nether.json`)

```json
{
  "world": {
    "world_name": "MacEntorno",
    "seed": -8850467306991264225
  },
  "dimension": "nether",
  "reference_position": [-184, 108],
  "results": [
    {
      "target": "minecraft:bastion_remnant",
      "x": -208,
      "z": 336,
      "dist_ref": 229.3,
      "tp_command": "/execute in minecraft:the_nether run tp -208 ~ 336"
    },
    {
      "target": "minecraft:fortress",
      "x": -864,
      "z": -128,
      "dist_ref": 719.8,
      "tp_command": "/execute in minecraft:the_nether run tp -864 ~ -128"
    }
  ]
}
```

---

## 🛡️ Seguridad
El script nunca escribe ni modifica los archivos de guardado reales. Ejecuta una instancia aislada y efímera en memoria temporal para consultar el motor nativo del juego y se limpia automáticamente.

---

## 🔬 Metodología Técnica y Arquitectura del Sistema

Para lograr una precisión del 100% sin depender de herramientas externas ni arriesgar la integridad del mundo, se aplicó el siguiente proceso de ingeniería inversa e integración:

### 1. Extracción de Metadatos NBT (Python Puro)
* Se implementó un parser de NBT (Named Binary Tag) en [minecraft_locator.py](file://herramientas/mapas/minecraft_locator.py) que lee archivos `.dat` comprimidos en gzip.
* Se leyó `level.dat` y `world_gen_settings.dat` para extraer:
  * **Semilla del Mundo:** `-8850467306991264225`
  * **Versión del motor:** `26.3` (DataVersion `5023`).
  * **Punto de spawn:** `(0, 73, 0)`.
  * **Ubicación exacta del jugador:** Leyendo el archivo más reciente en `players/data/*.dat` (`X: -1471.5, Y: 67.0, Z: 864.5`).

### 2. Aislamiento Sandboxed y Ejecución Headless
En lugar de simular manualmente los complejos algoritmos de biomas (ruido Perlin/MultiNoise), se aprovechó el motor oficial de Minecraft ya instalado en la Mac:
* **Entorno Java 25:** Se utiliza el binario nativo empaquetado por Mojang ubicado en `~/Library/Application Support/minecraft/runtime/java-runtime-epsilon/.../bin/java`.
* **Classpath Oficial:** Se cargan `26.3.jar` junto a sus 114 bibliotecas de dependencias (LWJGL, FastUtil, Mojang DataFixers, etc.).
* **Sandbox Efímero:** Se genera un directorio temporal (`/tmp/...`) con copias ligeras de solo lectura de `level.dat` y `data/`. Esto garantiza que el archivo `session.lock` del mundo real permanezca intacto y no sufra bloqueos ni corrupción.

### 3. Consultas Nativas de Estructuras y Biomas
* Se levanta `net.minecraft.server.Main --nogui` en el sandbox.
* Se envían comandos de búsqueda vía `stdin`:
  * **Overworld:** `/execute positioned X 70 Z run locate structure <id>`
  * **Nether:** `/execute in minecraft:the_nether positioned X 64 Z run locate structure/biome <id>`
* Se parsean las respuestas en stdout mediante expresiones regulares, capturando el identificador, coordenadas exactas `[X, Y, Z]` y calculando la distancia euclidiana hacia el jugador o portal.

### 4. Matemática de Coordenadas del Nether
* La relación entre el Overworld y el Nether es $1:8$.
* Para ubicar las estructuras relevantes al entrar al Nether, se tomó la coordenada del jugador en el Overworld `(-1472, 864)` y se dividió entre 8, estableciendo el punto de origen en el Nether en `(-184, 108)`. Esto permitió encontrar el Bastión a tan solo 229 bloques de caminata desde el portal de entrada.
