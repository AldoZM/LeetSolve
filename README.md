# LeetSolve

Animated explainers for the data structures and algorithms behind common LeetCode problems, built with [Manim Community Edition](https://www.manim.community/), local [Kokoro](https://github.com/hexgrad/kokoro) TTS narration and a Three.js 3D section.

Current style: vertical 1080×1440 videos set inside a real Minecraft world, with the code shown next to the solution and a seamless loop.

## Docs (Spanish)

- [GUIA.md](GUIA.md) — full working context: format, folders, workflow, helpers, known problems.
- [INSTRUCCIONES_IA.md](INSTRUCCIONES_IA.md) — step-by-step brief so any AI model can make a new video with the same parameters.
- [BITACORA.md](BITACORA.md) — what was done in each session.

## Layout

- `videos/<section>/<number>-<name>/` — one video per folder (narration, timings, scenes, 3D page).
- `pruebas/` — experiments. `pruebas/0001-two-sum-minecraft-original` is the template of the approved style.
- `herramientas/` — shared tools: `build.py`, `prelude.py`, `sheet.py`, the 3D renderer (`three/render.mjs`, `three/stage.js`) and the visual themes.
- `herramientas/temas/minecraft-original/mundos/` — the ClaudeEntorno world (`ClaudeEntorno.zip`, Java Edition 26.2+) and its exported surface (`claude.json`).
- `Three/` — the first tree explainer (16:9).

Final videos and render intermediates are not committed; `herramientas/build.py` rebuilds them.

## Minecraft assets

The game's textures, GUI, font and sounds are copied from a local Minecraft Java install by `herramientas/temas/minecraft-original/extraer.py` and are never committed. The world save and the code here are original.

NOT AN OFFICIAL MINECRAFT PRODUCT. NOT APPROVED BY OR ASSOCIATED WITH MOJANG OR MICROSOFT.
