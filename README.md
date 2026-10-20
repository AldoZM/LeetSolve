# LeetSolve

Animated explainers for data structures and algorithms behind common LeetCode problems, built with [Manim Community Edition](https://www.manim.community/) and local [Kokoro](https://github.com/hexgrad/kokoro) TTS narration.

## Topics

| Folder | Topic | Video |
|---|---|---|
| [Three](Three/) | Trees: anatomy, depth/height, binary search trees, traversals, recursion (`maxDepth`) | [Three.mp4](Three/Three.mp4) |

## Folder contents

- `Three.txt` — the prompt/storyboard used to generate the video
- `narration.txt` — narration lines
- `timestamps.json` — per-line audio timing
- `script.py` — Manim source (one class per scene)
- `concat.txt` — scene order
- `Three.mp4` — final video (9:16, narrated)

## Rebuild

Requires Python 3.10+, `manim`, `kokoro`, `soundfile`, ffmpeg and a LaTeX distribution.

```bash
cd Three
manim script.py   # render scenes listed in concat.txt
```

Then concatenate the scenes with ffmpeg and mux with the narration audio, as described in [manim-skill](https://github.com/Yusuke710/manim-skill).
