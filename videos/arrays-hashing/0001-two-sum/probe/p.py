from manim import *
config.pixel_width, config.pixel_height = 540, 720
config.frame_width, config.frame_height = 9, 12
class P(Scene):
    def construct(self):
        c = Code(code_string="def twoSum(nums, target):\n    seen = {}\n    for i, x in enumerate(nums):\n        need = target - x\n        if need in seen:\n            return [seen[need], i]\n        seen[x] = i", language="python", formatter_style="monokai", background="rectangle",
                 background_config={"fill_color": "#11162A", "stroke_color": "#A78BFA", "stroke_width": 2}, paragraph_config={"font": "Consolas"})
        print("CODE", c.width, c.height)
        t = Text("Two Sum", font="Segoe UI", weight=BOLD, font_size=110); print("TITLE", t.width, t.height)
        self.add(c.scale_to_fit_width(8.2), t.to_edge(UP))
