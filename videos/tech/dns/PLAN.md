# Plan: short DNS todo en 3D

Diseño: `DISENO.md` (aprobado por Aldo el 2026-10-28). Aldo pidió implementarlo directo, con commit y push al terminar cada sección.

## Tareas

1. [x] **Voz en esta PC:** crear `~/.manim-skill-src/.venv-tts` con torch de CPU y `qwen-tts`; clonar una línea con `pruebas/voces_demo/tts_qwen_clone.py`, medir el tiempo y que Aldo la escuche.
2. [ ] **Narración completa:** `narration.txt` (las 26 líneas del diseño), `voiceover.mp3` y `timestamps.json`. Revisar cada línea: `silencedetect` (ningún silencio > 0.45 s) y duración ≤ palabras × 0.65 + 1.5.
3. [x] **Assets:** `extraer.py` copia a `gente/` (aldeano, tipos, profesiones, jugador, illager) y las texturas y sonidos nuevos de bloques (`tex/`, `sounds/`). `gente/` va al `.gitignore` del tema.
4. [x] **`gente.js`** (tema): `makeVillager(imgs, {profession, type})`, `makePlayer(imgs, {skin})`, `makeIllager(imgs, {kind})`, cada uno `{g, head, walk(s, amount), ...}`. Página de vista con cuadros de los personajes.
5. [x] **`aldea.js`** (tema): bibliotecas, torre de la raíz, lugar google.com y sus copias, cuarto de barreras, banco falso con TNT, casa de Steve, globo tooltip y objeto volador.
6. [x] **Lugar:** zona nueva de los mundos de esta PC, anotada en `mundos/lugares.json`.
7. [x] **Modo solo 3D en `build.py`** (`"solo3d"` en `video.json`) y `--cues` en `render.mjs` (efectos marcados en `window.sfxCues`). Comprobar que un video viejo (`shorts/02-dfs`, `build.py mux`) sigue igual.
8. [ ] **`three/dns.html`:** las 10 escenas sobre los tiempos de `timestamps.json`. Cuadros fijos de cada escena para Aldo antes del render completo.
9. [ ] **Render y revisión:** duración video = audio, música, loop (diferencia media < 1), errores de `GUIA.md`; abrir en Edge.
10. [ ] **Documentación:** `BITACORA.md`, sección de `GUIA.md` sobre videos solo 3D, `descripcion.txt` (≤ 100 caracteres).

## Lo que puede fallar sin que nada lo pruebe

- Texto ilegible en el celular: cada globo o letrero, al menos ~40 px de alto de letra en el cuadro de 1080.
- Desfase voz-imagen: todo evento se ancla a `[línea, segundos]` de `timestamps.json`, nunca a segundos absolutos.
- Globos tapados por paredes o terreno: `depthTest: false` y `renderOrder` alto.
- Loop roto: la cámara y los personajes vuelven al estado del cuadro 0.
- Voz con silencios o palabras de más: revisión del punto 2.
