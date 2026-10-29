# Plan: short de paquetes todo en 3D

Diseño: `DISENO.md`. Aldo pidió empezar por el código y dejar la voz y el render para otro momento (2026-10-28).

## Tareas

1. [x] **Assets en `extraer.py`:** rieles, vagoneta, el cuadro `bust` y su reverso; sonidos de vagoneta, `fizz`, cuadro, marco y campana.
2. [x] **`rieles.js`** (tema): rieles, vagoneta del juego, estación del router y avance por llaves. `gente.js` exporta `entityPart` y `skinMat`.
3. [x] **Lugar:** `mac-13` → `birch-terraces`, anotado en `mundos/lugares.json`.
4. [x] **`narration.txt`, `video.json`, `descripcion.txt`** (93 caracteres).
5. [x] **`three/packets.html`:** las 16 escenas ancladas a `ev(línea, fracción)`. Revisado con `node --check`; la lógica de rieles probada en Node (largos de las rutas, curvas, pasadas del TTL).
6. [x] **En esta PC, antes de probar:** `extraer.py 26.3` corrido y 5 texturas de `birch-terraces` copiadas del jar (2026-10-28).
7. [x] **Voz:** `pruebas/voces_demo/tts_qwen_clone.py videos/tech/packets` con la voz madura. Revisar cada línea (silencios, duración).
8. [x] **Cuadros fijos de cada escena** (2026-10-28): uno a la mitad de cada línea, más t = 0, el letrero bajando y el último cuadro, en `review3d/` con `hoja1.png`, `hoja2.png` y `hoja_rieles.png`. Tiempos de `three/timestamps.json` **provisional** (2.5 palabras por segundo + 0.35 s por línea, 130.4 s): **borrarlo antes del render final**, o la página no usa los tiempos de la voz. Corregido en la revisión:
   - Las etiquetas "1" y "2" de las vagonetas en espera, fuera del cuadro a 79°, llenaban la pantalla de morado (línea 4). Arreglado en `placeUI` (`aldea.js`).
   - El globo "1 photo = thousands of packets" era más ancho que el cuadro 9:16 y se cortaba. `placeUI` ahora lo achica.
   - Los rieles no se veían en las tomas lejanas. El terreno los tapaba; ahora son recorte opaco (`rieles.js`).
   - La portada decía "OW PACKET WORK": el texto no cabía. Ahora son 3 renglones (`HOW / PACKETS / WORK`, h 2.2).
   - El letrero de la portada tapaba la mitad de la toma de Steve (líneas 0 a 2). Ahora baja al suelo al salir de la portada y sube para el último cuadro (loop: diferencia 0.01).
   - Con los tiempos provisionales, la toma del TTL (líneas 16 y 17) deja la vagoneta y "time to live" pegados abajo. Revisarla otra vez con la voz real.
9. [x] **Render y revisión:** `build.py` (corre `three mux`), duración igual al audio, música, loop, errores de `GUIA.md`; abrirlo en Edge.
10. [x] **Al terminar:** `BITACORA.md`, "Videos hechos" de `GUIA.md` y el video renombrado en `export/`.

## Lo que puede fallar y solo se ve en los cuadros

- **Tiempos de las vagonetas:** revisados con los tiempos provisionales, midiendo la distancia entre todas las vagonetas visibles cada 0.05 s. Ninguna choca (mínimo 1.5 bloques, la separación de las filas). El 4 llega antes que el 2 (65.4 s contra 67.9 s) y el 2 sale de LB (62.5 s) después de las dos vagonetas de adelante (58.5 s y 61.5 s). El tráfico de las tomas aéreas iba en los dos sentidos por la misma vía y se atravesaba de frente; ahora va en un solo sentido, con la misma velocidad y 6 bloques de separación. **Repetir la revisión con la voz real**, porque los tiempos cambian.
- **La toma aérea:** la red mide unos 64 × 60 bloques; en 9:16 las entradas este y oeste pueden quedar cortadas a los lados (no importa) y los globos "router" no deben encimarse.
- **Los rieles:** las curvas y los cruces nunca se han visto renderizados. En los cruces van dos rieles encimados.
- **La vagoneta:** el modelo se armó desde `MinecartModel` (piso y 4 paredes); revisar que el cofre quede adentro y que las paredes no salgan volteadas.
- **Globos:** varios a la vez en la casa de Alex (repisa, "missing: 3", "photo complete"); que no se tapen entre sí.
- **Terrazas de tierra:** alrededor del lote aplanado puede verse una pared de tierra en la toma aérea.

## Cierre (2026-10-29, PC de Windows)

- Voz clonada: 23 líneas, 105.9 s. Sin silencios largos ni líneas fuera del límite de duración. Whisper marcó las líneas 10 y 11: la 10 se oye bien con 0.3 s de audio previo ("packet three is gone") y la 11 solo cambia los números a cifras.
- `three/timestamps.json` provisional borrado. La toma del TTL (líneas 16 y 17) se abrió para que la vagoneta no quede pegada abajo.
- Render: 105.9 s de video y audio, 37 efectos, Subwoofer Lullaby, loop con diferencia 0.66. `How Packets Work.mp4` en la carpeta y en `export/`.
