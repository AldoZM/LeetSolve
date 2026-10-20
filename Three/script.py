from manim import *
import numpy as np

# Vertical 9:16 configuration (YouTube Shorts)
config.pixel_width = 480
config.pixel_height = 854
config.frame_width = 9.0
config.frame_height = 16.0
config.frame_rate = 15
config.background_color = "#0f172a"

# Vertical tree layout constants
NODE_POSITIONS = {
    8: np.array([0.0, 3.0, 0.0]),
    3: np.array([-2.1, 1.5, 0.0]),
    10: np.array([2.1, 1.5, 0.0]),
    1: np.array([-3.3, 0.0, 0.0]),
    6: np.array([-0.9, 0.0, 0.0]),
    14: np.array([3.3, 0.0, 0.0]),
    4: np.array([-1.5, -1.5, 0.0]),
    7: np.array([-0.3, -1.5, 0.0]),
    13: np.array([2.4, -1.5, 0.0]),
}

EDGE_PAIRS = [
    (8, 3), (8, 10),
    (3, 1), (3, 6),
    (6, 4), (6, 7),
    (10, 14),
    (14, 13)
]

LEAF_VALS = {1, 4, 7, 13}
ROOT_VAL = 8

def create_tree_mobjects(active_vals=(), leaf_color="#16a34a", root_color="#eab308", node_color="#2563eb", active_color="#f97316", edge_color="#94a3b8", scale=1.0, shift_vec=ORIGIN):
    nodes = {}
    for val, base_pos in NODE_POSITIONS.items():
        pos = (base_pos * scale) + shift_vec
        if val in active_vals:
            c = active_color
        elif val == ROOT_VAL and root_color:
            c = root_color
        elif val in LEAF_VALS and leaf_color:
            c = leaf_color
        else:
            c = node_color
        circ = Circle(radius=0.34 * scale, fill_color=c, fill_opacity=0.9, stroke_color=WHITE, stroke_width=2.2 * scale)
        circ.move_to(pos)
        txt = Text(str(val), font_size=int(20 * scale), weight=BOLD, color=WHITE)
        txt.move_to(pos)
        nodes[val] = VGroup(circ, txt)

    edges = []
    for u, v in EDGE_PAIRS:
        p1 = (NODE_POSITIONS[u] * scale) + shift_vec
        p2 = (NODE_POSITIONS[v] * scale) + shift_vec
        edge = Line(p1, p2, buff=0.36 * scale, color=edge_color, stroke_width=2.8 * scale)
        edges.append(edge)

    edges_group = VGroup(*edges)
    nodes_group = VGroup(*[nodes[k] for k in sorted(nodes.keys())])
    return nodes, edges_group, nodes_group


class Scene1_Introduction(Scene):
    def construct(self):
        # Subtitle 0 (7.150s)
        dur0 = 7.15
        self.add_subcaption(
            "A list stores data one item after another. But many problems need a different way to organize information.",
            duration=dur0
        )
        title = Tex(r"\textbf{Trees}", font_size=48, color=BLUE_B).to_edge(UP, buff=1.2)
        subtitle = Text("Data Structure Explainer", font_size=20, color="#94a3b8").next_to(title, DOWN, buff=0.2)
        
        # 1D array of items fitted to vertical width
        vals = [1, 3, 4, 6, 7, 8, 10, 13, 14]
        boxes = []
        for i, val in enumerate(vals):
            sq = Square(side_length=0.72, fill_color="#1e293b", fill_opacity=0.9, stroke_color="#64748b", stroke_width=1.8)
            t = Text(str(val), font_size=18, weight=BOLD, color=WHITE)
            cell = VGroup(sq, t).move_to(np.array([(i - 4) * 0.85, 0.5, 0]))
            boxes.append(cell)
        list_group = VGroup(*boxes)
        list_label = Text("Linear Array: Sequential Access", font_size=20, color="#94a3b8").next_to(list_group, DOWN, buff=0.8)

        self.play(FadeIn(title, shift=DOWN), FadeIn(subtitle), run_time=1.0)
        self.play(FadeIn(list_group, shift=UP), FadeIn(list_label), run_time=1.8)
        self.play(Indicate(list_group, color=YELLOW), run_time=1.5)
        self.wait(dur0 - (1.0 + 1.8 + 1.5))

        # Subtitle 1 (6.325s)
        dur1 = 6.325
        self.add_subcaption(
            "A tree organizes data in levels, like a company org chart or the folders on your computer.",
            duration=dur1
        )
        _, edges_group, nodes_group = create_tree_mobjects(leaf_color=None, root_color=None, node_color="#2563eb", shift_vec=DOWN*0.5)
        tree_label = Text("Hierarchical Tree:\nMulti-Level Organization", font_size=22, weight=BOLD, color=YELLOW_B).to_edge(DOWN, buff=1.5)

        self.play(
            FadeOut(list_label),
            Transform(list_group, nodes_group),
            run_time=2.2
        )
        self.play(Create(edges_group), FadeIn(tree_label, shift=UP), run_time=1.5)
        self.wait(dur1 - (2.2 + 1.5))


class Scene2_Anatomy(Scene):
    def construct(self):
        # Subtitle 2 (4.500s)
        dur2 = 4.5
        self.add_subcaption(
            "Each element is a node, and each connection between nodes is an edge.",
            duration=dur2
        )
        title = Tex(r"\textbf{Anatomy of a Tree}", font_size=42, color=BLUE_B).to_edge(UP, buff=1.2)
        nodes, edges_group, nodes_group = create_tree_mobjects(leaf_color=None, root_color=None, node_color="#2563eb", shift_vec=DOWN*0.2)
        tree = VGroup(edges_group, nodes_group)

        node_arrow = Arrow(start=nodes[3].get_center() + LEFT*1.4 + UP*0.8, end=nodes[3].get_center() + LEFT*0.35, buff=0.05, color=BLUE_B)
        node_lbl = Text("Node", font_size=20, color=BLUE_B).next_to(node_arrow.get_start(), UP, buff=0.1)

        edge_arrow = Arrow(start=np.array([1.2, 3.8, 0]), end=np.array([1.1, 2.3, 0]), buff=0.05, color="#cbd5e1")
        edge_lbl = Text("Edge", font_size=20, color="#cbd5e1").next_to(edge_arrow.get_start(), UP, buff=0.1)

        self.play(FadeIn(title), FadeIn(tree), run_time=1.2)
        self.play(Create(node_arrow), FadeIn(node_lbl), Create(edge_arrow), FadeIn(edge_lbl), run_time=1.5)
        self.wait(dur2 - (1.2 + 1.5))

        # Subtitle 3 (6.825s)
        dur3 = 6.825
        self.add_subcaption(
            "The node at the top is the root. Every node can have children, and nodes with no children are called leaves.",
            duration=dur3
        )
        root_arrow = Arrow(start=np.array([1.5, 3.8, 0]), end=nodes[8].get_right() + RIGHT*0.1, buff=0.05, color=YELLOW_B)
        root_lbl = Text("Root", font_size=22, weight=BOLD, color=YELLOW_B).next_to(root_arrow.get_start(), RIGHT, buff=0.1)

        children_lbl = Text("Children of 3: {1, 6}", font_size=18, color=BLUE_C).move_to(np.array([-2.0, -2.8, 0]))

        leaf_anims = []
        for lf in sorted(LEAF_VALS):
            leaf_anims.append(nodes[lf][0].animate.set_fill("#16a34a"))
        leaves_tag = Text("Leaves: Nodes with No Children", font_size=20, weight=BOLD, color="#4ade80").to_edge(DOWN, buff=1.4)

        self.play(FadeOut(node_arrow), FadeOut(node_lbl), FadeOut(edge_arrow), FadeOut(edge_lbl), run_time=0.5)
        self.play(
            nodes[8][0].animate.set_fill("#eab308"),
            Create(root_arrow), FadeIn(root_lbl),
            run_time=1.5
        )
        self.play(
            FadeIn(children_lbl),
            *leaf_anims, FadeIn(leaves_tag, shift=UP),
            run_time=1.8
        )
        self.wait(dur3 - (0.5 + 1.5 + 1.8))

        # Subtitle 4 (7.450s)
        dur4 = 7.45
        self.add_subcaption(
            "Any node, together with all of its descendants, forms a subtree. This idea is the key to everything that follows.",
            duration=dur4
        )
        subtree_rect = RoundedRectangle(
            corner_radius=0.35, width=2.8, height=2.6,
            fill_color="#38bdf8", fill_opacity=0.15,
            stroke_color="#38bdf8", stroke_width=2.5
        ).move_to(np.array([-0.9, -0.9, 0]))
        subtree_tag = Text("Subtree rooted at 6", font_size=20, weight=BOLD, color="#38bdf8").to_edge(DOWN, buff=1.6)

        self.play(
            FadeOut(root_arrow), FadeOut(root_lbl),
            FadeOut(children_lbl),
            FadeOut(leaves_tag),
            run_time=0.6
        )
        self.play(Create(subtree_rect), FadeIn(subtree_tag), run_time=1.8)
        self.play(Indicate(VGroup(nodes[6], nodes[4], nodes[7]), color="#38bdf8"), run_time=1.5)
        self.wait(dur4 - (0.6 + 1.8 + 1.5))


class Scene3_DepthHeight(Scene):
    def construct(self):
        # Subtitle 5 (4.000s)
        dur5 = 4.0
        self.add_subcaption(
            "The depth of a node is how many edges separate it from the root.",
            duration=dur5
        )
        title = Tex(r"\textbf{Depth and Height}", font_size=42, color=BLUE_B).to_edge(UP, buff=1.2)
        nodes, edges_group, nodes_group = create_tree_mobjects(shift_vec=DOWN*0.2)
        tree = VGroup(edges_group, nodes_group)

        # Levels
        level_y = [2.8, 1.3, -0.2, -1.7]
        lines, labels = [], []
        for lvl, y in enumerate(level_y):
            line = DashedLine(start=np.array([-4.0, y, 0]), end=np.array([4.0, y, 0]), color="#334155", stroke_width=1.5)
            lbl = Text(f"Level {lvl}", font_size=16, color="#94a3b8").move_to(np.array([-3.5, y + 0.28, 0]))
            lines.append(line)
            labels.append(lbl)
        level_lines = VGroup(*lines)
        level_labels = VGroup(*labels)

        self.play(FadeIn(title), FadeIn(tree), Create(level_lines), FadeIn(level_labels), run_time=1.8)
        
        depth_arrow = DoubleArrow(start=np.array([-0.9, 2.8, 0]), end=np.array([-0.9, -0.2, 0]), buff=0.1, color=ORANGE)
        depth_tag = Text("Depth = 2 edges", font_size=18, color=ORANGE).next_to(depth_arrow, RIGHT, buff=0.1)
        self.play(Create(depth_arrow), FadeIn(depth_tag), run_time=1.2)
        self.wait(dur5 - (1.8 + 1.2))

        # Subtitle 6 (5.825s)
        dur6 = 5.825
        self.add_subcaption(
            "The height of the tree is the longest path from the root down to a leaf. Here, the height is three.",
            duration=dur6
        )
        p1 = Line(NODE_POSITIONS[8] + DOWN*0.2, NODE_POSITIONS[10] + DOWN*0.2, buff=0.36, color=YELLOW_B, stroke_width=5)
        p2 = Line(NODE_POSITIONS[10] + DOWN*0.2, NODE_POSITIONS[14] + DOWN*0.2, buff=0.36, color=YELLOW_B, stroke_width=5)
        p3 = Line(NODE_POSITIONS[14] + DOWN*0.2, NODE_POSITIONS[13] + DOWN*0.2, buff=0.36, color=YELLOW_B, stroke_width=5)
        longest_path = VGroup(p1, p2, p3)

        height_badge = VGroup(
            RoundedRectangle(corner_radius=0.2, width=8.0, height=1.1, fill_color="#1e293b", fill_opacity=0.95, stroke_color=YELLOW_B, stroke_width=2),
            Text("Tree Height = 3 edges\n(Longest Root-to-Leaf Path)", font_size=18, weight=BOLD, color=YELLOW_B)
        ).to_edge(DOWN, buff=1.4)

        self.play(FadeOut(depth_arrow), FadeOut(depth_tag), run_time=0.5)
        self.play(Create(longest_path), run_time=1.8)
        self.play(FadeIn(height_badge, shift=UP), run_time=1.2)
        self.wait(dur6 - (0.5 + 1.8 + 1.2))


class Scene4_BinarySearchTree(Scene):
    def construct(self):
        # Subtitle 7 (10.400s)
        dur7 = 10.4
        self.add_subcaption(
            "In a binary tree, every node has at most two children. If everything on the left is smaller and everything on the right is larger, we have a binary search tree.",
            duration=dur7
        )
        title = Tex(r"\textbf{Binary Search Tree}", font_size=40, color=BLUE_B).to_edge(UP, buff=1.2)
        rule = MathTex(r"\text{Left} < \mathbf{\text{Node}} < \text{Right}", font_size=26, color=YELLOW_B).next_to(title, DOWN, buff=0.3)
        
        nodes, edges_group, nodes_group = create_tree_mobjects(shift_vec=DOWN*0.3)
        tree = VGroup(edges_group, nodes_group)

        check_8_l = Text("< 8", font_size=20, color="#4ade80").move_to(np.array([-1.8, 2.3, 0]))
        check_8_r = Text("> 8", font_size=20, color="#4ade80").move_to(np.array([1.8, 2.3, 0]))

        check_3_l = Text("< 3", font_size=17, color="#4ade80").move_to(np.array([-3.2, 0.7, 0]))
        check_3_r = Text("> 3", font_size=17, color="#4ade80").move_to(np.array([-0.8, 0.7, 0]))

        self.play(FadeIn(title), FadeIn(rule), FadeIn(tree), run_time=1.8)
        self.play(FadeIn(check_8_l), FadeIn(check_8_r), nodes[8][0].animate.set_fill(YELLOW_D), run_time=2.6)
        self.play(FadeIn(check_3_l), FadeIn(check_3_r), nodes[3][0].animate.set_fill(BLUE_C), run_time=2.5)
        self.play(FadeOut(check_8_l), FadeOut(check_8_r), FadeOut(check_3_l), FadeOut(check_3_r), run_time=0.8)
        self.wait(dur7 - (1.8 + 2.6 + 2.5 + 0.8))

        # Subtitle 8 (8.550s)
        dur8 = 8.55
        self.add_subcaption(
            "To find seven, we compare at each node. Less than eight, go left. Greater than three, go right. Greater than six, go right. Found it.",
            duration=dur8
        )
        box_rect = RoundedRectangle(corner_radius=0.2, width=8.0, height=0.9, fill_color="#1e293b", fill_opacity=0.95, stroke_color=ORANGE, stroke_width=2)
        box_txt = Text("Search target: 7", font_size=20, weight=BOLD, color=WHITE).move_to(box_rect.get_center())
        search_card = VGroup(box_rect, box_txt).to_edge(DOWN, buff=1.4)

        t1 = Text("At 8: 7 < 8  --> Go Left", font_size=19, color=ORANGE).move_to(box_rect.get_center())
        t2 = Text("At 3: 7 > 3  --> Go Right", font_size=19, color=ORANGE).move_to(box_rect.get_center())
        t3 = Text("At 6: 7 > 6  --> Go Right", font_size=19, color=ORANGE).move_to(box_rect.get_center())
        t4 = Text("At 7: 7 == 7  --> Found!", font_size=19, weight=BOLD, color="#4ade80").move_to(box_rect.get_center())

        self.play(FadeIn(search_card), run_time=0.75)
        self.play(
            nodes[8][0].animate.set_fill(ORANGE),
            Transform(search_card[1], t1),
            run_time=1.5
        )
        self.play(
            nodes[8][0].animate.set_fill(YELLOW_D),
            nodes[3][0].animate.set_fill(ORANGE),
            Transform(search_card[1], t2),
            run_time=1.5
        )
        self.play(
            nodes[3][0].animate.set_fill(BLUE_D),
            nodes[6][0].animate.set_fill(ORANGE),
            Transform(search_card[1], t3),
            run_time=1.5
        )
        self.play(
            nodes[6][0].animate.set_fill(BLUE_D),
            nodes[7][0].animate.set_fill("#16a34a"),
            Transform(search_card[1], t4),
            Flash(nodes[7].get_center(), color="#4ade80", line_length=0.3),
            run_time=1.5
        )
        self.wait(dur8 - (0.75 + 1.5 + 1.5 + 1.5 + 1.5))

        # Subtitle 9 (6.400s)
        dur9 = 6.4
        self.add_subcaption(
            "At every step we discard half of the tree. That is why searching costs log n in a balanced tree.",
            duration=dur9
        )
        right_side = VGroup(nodes[10], nodes[14], nodes[13])
        discard_lbl = Text("Half of tree discarded!", font_size=20, weight=BOLD, color="#ef4444").move_to(np.array([1.5, 4.2, 0]))
        complexity = MathTex(r"\mathcal{O}(\log n)\text{ Time Complexity}", font_size=28, color=YELLOW_B).to_edge(DOWN, buff=1.4)

        self.play(
            FadeOut(search_card),
            right_side.animate.set_opacity(0.2),
            FadeIn(discard_lbl),
            run_time=1.8
        )
        self.play(FadeIn(complexity, shift=UP), run_time=1.5)
        self.wait(dur9 - (1.8 + 1.5))


class Scene5_DegenerateTree(Scene):
    def construct(self):
        # Subtitle 10 (7.125s)
        dur10 = 7.125
        self.add_subcaption(
            "But if we insert data that is already sorted, the tree turns into a line, and searching takes n steps again.",
            duration=dur10
        )
        title = Tex(r"\textbf{Degenerate Tree}", font_size=42, color=RED_B).to_edge(UP, buff=1.2)
        seq_text = Text("Insert sorted: [1, 2, 3, 4, 5]", font_size=20, color="#94a3b8").next_to(title, DOWN, buff=0.3)

        # Skewed chain fitted to vertical screen
        chain_nodes, chain_edges = [], []
        for i in range(5):
            pos = np.array([-1.8 + i*0.9, 2.5 - i*1.2, 0])
            c = Circle(radius=0.34, fill_color="#ef4444", fill_opacity=0.9, stroke_color=WHITE, stroke_width=2)
            c.move_to(pos)
            t = Text(str(i+1), font_size=18, weight=BOLD, color=WHITE).move_to(pos)
            chain_nodes.append(VGroup(c, t))
            if i > 0:
                p_prev = np.array([-1.8 + (i-1)*0.9, 2.5 - (i-1)*1.2, 0])
                e = Line(p_prev, pos, buff=0.36, color="#ef4444", stroke_width=2.5)
                chain_edges.append(e)

        chain_group = VGroup(*chain_edges, *chain_nodes)
        worst_case = VGroup(
            RoundedRectangle(corner_radius=0.2, width=8.0, height=1.0, fill_color="#1e293b", fill_opacity=0.95, stroke_color=RED, stroke_width=2),
            Text("Worst Case:\nDegenerates to O(n) Linked List", font_size=18, weight=BOLD, color=RED)
        ).to_edge(DOWN, buff=1.4)

        self.play(FadeIn(title), FadeIn(seq_text), run_time=1.0)
        self.play(Create(chain_group), run_time=2.2)
        self.play(FadeIn(worst_case, shift=UP), run_time=1.5)
        self.wait(dur10 - (1.0 + 2.2 + 1.5))

        # Subtitle 11 (5.600s)
        dur11 = 5.6
        self.add_subcaption(
            "That is why self-balancing trees exist, like AVL trees and red-black trees.",
            duration=dur11
        )
        b_pos = {
            3: np.array([0.0, 1.8, 0]),
            2: np.array([-1.8, 0.4, 0]),
            4: np.array([1.8, 0.4, 0]),
            1: np.array([-2.8, -1.0, 0]),
            5: np.array([2.8, -1.0, 0]),
        }
        b_nodes, b_edges = {}, []
        for val, p in b_pos.items():
            circ = Circle(radius=0.34, fill_color="#2563eb", fill_opacity=0.9, stroke_color=WHITE, stroke_width=2)
            circ.move_to(p)
            txt = Text(str(val), font_size=18, weight=BOLD, color=WHITE).move_to(p)
            b_nodes[val] = VGroup(circ, txt)
        for u, v in [(3, 2), (3, 4), (2, 1), (4, 5)]:
            b_edges.append(Line(b_pos[u], b_pos[v], buff=0.36, color="#38bdf8", stroke_width=2.5))
        balanced_tree = VGroup(*b_edges, *b_nodes.values())

        badge = VGroup(
            RoundedRectangle(corner_radius=0.2, width=8.2, height=1.0, fill_color="#1e293b", fill_opacity=0.95, stroke_color="#38bdf8", stroke_width=2),
            Text("AVL & Red-Black Trees:\nAuto-balanced to O(log n)", font_size=18, weight=BOLD, color="#38bdf8")
        ).to_edge(DOWN, buff=1.4)

        self.play(
            FadeOut(seq_text),
            FadeOut(worst_case),
            Transform(chain_group, balanced_tree),
            run_time=2.0
        )
        self.play(FadeIn(badge, shift=UP), run_time=1.5)
        self.wait(dur11 - (2.0 + 1.5))


class Scene6_Traversals(Scene):
    def construct(self):
        # Subtitle 12 (5.700s)
        dur12 = 5.7
        self.add_subcaption(
            "Traversing a tree means visiting all of its nodes. There are four classic ways to do it.",
            duration=dur12
        )
        title = Tex(r"\textbf{Tree Traversals}", font_size=42, color=BLUE_B).to_edge(UP, buff=1.2)
        
        # 4 compact badges arranged 2x2 in vertical
        b_names = ["1. Preorder", "2. Inorder", "3. Postorder", "4. Level Order"]
        badges = []
        for i, name in enumerate(b_names):
            rx = -2.0 if (i % 2 == 0) else 2.0
            ry = 4.8 if (i < 2) else 3.9
            card = VGroup(
                RoundedRectangle(corner_radius=0.15, width=3.6, height=0.65, fill_color="#1e293b", fill_opacity=0.9, stroke_color="#64748b", stroke_width=1.5),
                Text(name, font_size=16, color=WHITE)
            ).move_to(np.array([rx, ry, 0]))
            badges.append(card)
        traversal_cards = VGroup(*badges)

        nodes, edges_group, nodes_group = create_tree_mobjects(scale=0.85, shift_vec=DOWN*1.2)
        tree = VGroup(edges_group, nodes_group)

        self.play(FadeIn(title), FadeIn(tree), run_time=1.5)
        self.play(FadeIn(traversal_cards), run_time=1.8)
        self.wait(dur12 - (1.5 + 1.8))

        # Subtitle 13 (7.275s)
        dur13 = 7.275
        self.add_subcaption(
            "In preorder, we visit the node first and then its children. In postorder, the children first and the node last.",
            duration=dur13
        )
        pre_info = VGroup(
            RoundedRectangle(corner_radius=0.15, width=8.2, height=1.0, fill_color="#1e293b", fill_opacity=0.95, stroke_color=YELLOW_B, stroke_width=1.5),
            Text("Preorder: Node -> Left -> Right\nPostorder: Left -> Right -> Node", font_size=16, color=YELLOW_B)
        ).move_to(np.array([0, 4.3, 0]))

        pre_order = [8, 3, 1, 6, 4, 7, 10, 14, 13]
        pre_anims = [nodes[val][0].animate.set_fill(ORANGE) for val in pre_order[:4]]

        self.play(Transform(traversal_cards, pre_info), run_time=1.0)
        self.play(AnimationGroup(*pre_anims, lag_ratio=0.3), run_time=2.5)
        self.play(AnimationGroup(*[nodes[val][0].animate.set_fill("#2563eb") for val in pre_order[:4]]), run_time=1.5)
        self.wait(dur13 - (1.0 + 2.5 + 1.5))

        # Subtitle 14 (7.226s)
        dur14 = 7.226
        self.add_subcaption(
            "In inorder, we visit left, node, right. In a binary search tree, this gives us the values in sorted order.",
            duration=dur14
        )
        in_info = VGroup(
            RoundedRectangle(corner_radius=0.15, width=8.2, height=1.0, fill_color="#1e293b", fill_opacity=0.95, stroke_color="#4ade80", stroke_width=1.5),
            Text("Inorder: Left -> Node -> Right\n==> Sorted: [1, 3, 4, 6, 7, 8, 10, 13, 14]", font_size=15, color="#4ade80")
        ).move_to(np.array([0, 4.3, 0]))

        in_order = [1, 3, 4, 6, 7, 8, 10, 13, 14]
        in_anims = [nodes[val][0].animate.set_fill("#16a34a") for val in in_order]

        self.play(Transform(traversal_cards, in_info), run_time=1.0)
        self.play(AnimationGroup(*in_anims, lag_ratio=0.12), run_time=2.8)
        sorted_tag = Text("Always Sorted for BST!", font_size=20, weight=BOLD, color="#4ade80").to_edge(DOWN, buff=1.3)
        self.play(FadeIn(sorted_tag, shift=UP), run_time=1.4)
        self.wait(dur14 - (1.0 + 2.8 + 1.4))

        # Subtitle 15 (6.500s)
        dur15 = 6.5
        self.add_subcaption(
            "In level order, we use a queue and visit the tree one floor at a time. This is breadth-first search.",
            duration=dur15
        )
        bfs_info = VGroup(
            RoundedRectangle(corner_radius=0.15, width=8.2, height=1.0, fill_color="#1e293b", fill_opacity=0.95, stroke_color=BLUE_B, stroke_width=1.5),
            Text("Level Order (BFS): Queue [FIFO]\n8, 3, 10, 1, 6, 14, 4, 7, 13", font_size=16, color=BLUE_B)
        ).move_to(np.array([0, 4.3, 0]))

        levels = [
            [8],
            [3, 10],
            [1, 6, 14],
            [4, 7, 13]
        ]
        sweep_anims = []
        for lvl in levels:
            sweep_anims.append(AnimationGroup(*[nodes[val][0].animate.set_fill(YELLOW_D) for val in lvl]))

        self.play(FadeOut(sorted_tag), Transform(traversal_cards, bfs_info), run_time=1.0)
        self.play(Succession(*sweep_anims), run_time=2.8)
        bfs_badge = Text("Breadth-First Search (BFS)", font_size=20, color=YELLOW_B).to_edge(DOWN, buff=1.3)
        self.play(FadeIn(bfs_badge), run_time=1.0)
        self.wait(dur15 - (1.0 + 2.8 + 1.0))


class Scene7_RecursionLeetCode(Scene):
    def construct(self):
        # Subtitle 16 (6.750s)
        dur16 = 6.75
        self.add_subcaption(
            "On LeetCode, a tree is represented by nodes that store a value and point to their left and right child.",
            duration=dur16
        )
        title = Tex(r"\textbf{Trees on LeetCode}", font_size=40, color=BLUE_B).to_edge(UP, buff=1.2)

        # Code block on the top half
        code_lines = [
            "class TreeNode:",
            "    def __init__(self, val=0, left=None, right=None):",
            "        self.val = val",
            "        self.left = left",
            "        self.right = right"
        ]
        code_mobs = []
        for i, cl in enumerate(code_lines):
            t = Text(cl, font="Consolas", font_size=15, color="#f8fafc")
            t.move_to(np.array([-3.8 + t.width/2, 4.8 - i*0.4, 0]))
            code_mobs.append(t)
        code_box = VGroup(
            RoundedRectangle(corner_radius=0.2, width=8.0, height=2.5, fill_color="#020617", fill_opacity=0.95, stroke_color="#334155", stroke_width=2).move_to(np.array([0, 4.0, 0])),
            *code_mobs
        )

        # Visual node on the bottom half
        center_node = Circle(radius=0.5, fill_color="#2563eb", fill_opacity=0.9, stroke_color=WHITE, stroke_width=2.5).move_to(np.array([0, 0.0, 0]))
        center_txt = Text("val", font_size=22, weight=BOLD, color=WHITE).move_to(center_node.get_center())
        left_arrow = Arrow(start=center_node.get_center() + DL*0.35, end=np.array([-2.2, -1.6, 0]), buff=0.08, color="#38bdf8")
        left_lbl = Text(".left", font="Consolas", font_size=18, color="#38bdf8").next_to(left_arrow.get_end(), DOWN, buff=0.1)
        right_arrow = Arrow(start=center_node.get_center() + DR*0.35, end=np.array([2.2, -1.6, 0]), buff=0.08, color="#38bdf8")
        right_lbl = Text(".right", font="Consolas", font_size=18, color="#38bdf8").next_to(right_arrow.get_end(), DOWN, buff=0.1)
        node_vis = VGroup(center_node, center_txt, left_arrow, left_lbl, right_arrow, right_lbl)

        self.play(FadeIn(title), FadeIn(code_box, shift=DOWN), run_time=1.8)
        self.play(FadeIn(node_vis, shift=UP), run_time=1.8)
        self.wait(dur16 - (1.8 + 1.8))

        # Subtitle 17 (8.575s)
        dur17 = 8.575
        self.add_subcaption(
            "Since every child is the root of a subtree, almost every problem is solved the same way: solve the left, solve the right, and combine.",
            duration=dur17
        )
        maxdepth_lines = [
            "def maxDepth(root):",
            "    if not root:",
            "        return 0",
            "    return 1 + max(",
            "        maxDepth(root.left),",
            "        maxDepth(root.right)",
            "    )"
        ]
        m_mobs = []
        for i, cl in enumerate(maxdepth_lines):
            c_color = "#38bdf8" if "maxDepth" in cl else "#f8fafc"
            t = Text(cl, font="Consolas", font_size=15, color=c_color)
            t.move_to(np.array([-3.8 + t.width/2, 5.0 - i*0.38, 0]))
            m_mobs.append(t)
        maxdepth_box = VGroup(
            RoundedRectangle(corner_radius=0.2, width=8.0, height=3.0, fill_color="#020617", fill_opacity=0.95, stroke_color="#38bdf8", stroke_width=2).move_to(np.array([0, 3.8, 0])),
            *m_mobs
        )

        pattern_badge = VGroup(
            RoundedRectangle(corner_radius=0.2, width=8.0, height=0.9, fill_color="#1e293b", fill_opacity=0.95, stroke_color=YELLOW_B, stroke_width=2),
            Text("Divide & Conquer:\nSolve(Left)  +  Solve(Right)  --> Combine", font_size=17, color=YELLOW_B)
        ).move_to(np.array([0, 1.35, 0]))

        tree_sub = VGroup(
            Text("Left Subtree", font_size=16, color="#38bdf8").move_to(np.array([-2.2, -2.2, 0])),
            Text("Right Subtree", font_size=16, color="#38bdf8").move_to(np.array([2.2, -2.2, 0]))
        )

        self.play(Transform(code_box, maxdepth_box), run_time=2.0)
        self.play(FadeIn(pattern_badge), FadeIn(tree_sub), run_time=2.2)
        self.play(Indicate(pattern_badge), run_time=1.5)
        self.wait(dur17 - (2.0 + 2.2 + 1.5))

        # Subtitle 18 (5.500s)
        dur18 = 5.5
        self.add_subcaption(
            "For example, the maximum depth is one plus the larger depth of its two subtrees.",
            duration=dur18
        )
        depth_calc = VGroup(
            RoundedRectangle(corner_radius=0.2, width=8.0, height=1.5, fill_color="#1e293b", fill_opacity=0.95, stroke_color="#4ade80", stroke_width=2),
            Text("Leaves depth: 1\nNode 6: 1 + max(1,1) = 2\nNode 3: 1 + max(1,2) = 3\nRoot 8: 1 + max(3,3) = 4", font_size=16, color=WHITE)
        ).move_to(np.array([0, -0.4, 0]))

        result_tag = Text("maxDepth(root) = 4", font_size=24, weight=BOLD, color="#4ade80").to_edge(DOWN, buff=1.4)

        self.play(FadeIn(depth_calc, shift=UP), run_time=2.8)
        self.play(FadeIn(result_tag, shift=UP), run_time=1.2)
        self.wait(dur18 - (2.8 + 1.2))


class Scene8_WrapUp(Scene):
    def construct(self):
        # Subtitle 19 (6.725s)
        dur19 = 6.725
        self.add_subcaption(
            "Remember: a tree is a node with subtrees. Once you understand that, you understand recursion on trees.",
            duration=dur19
        )
        title = Tex(r"\textbf{Summary}", font_size=44, color=BLUE_B).to_edge(UP, buff=1.2)

        points = [
            "1. Hierarchy: Root, branches, leaves",
            "2. Fast Search: O(log n) in balanced BST",
            "3. 4 Traversals: Pre, In, Post, BFS",
            "4. Core Mindset: A node with subtrees!"
        ]
        cards = []
        for i, pt in enumerate(points):
            c_color = YELLOW_B if i == 3 else WHITE
            t = Text(pt, font_size=17, weight=BOLD if i == 3 else NORMAL, color=c_color)
            t.move_to(np.array([0, 5.2 - i*0.7, 0]))
            cards.append(t)
        bullets_group = VGroup(*cards)

        nodes, edges_group, nodes_group = create_tree_mobjects(scale=0.75, shift_vec=DOWN*1.2)
        tree = VGroup(edges_group, nodes_group)

        self.play(FadeIn(title), FadeIn(bullets_group), FadeIn(tree), run_time=1.5)
        glow_anims = [
            nodes[8][0].animate.set_fill(YELLOW_D),
            AnimationGroup(nodes[3][0].animate.set_fill(ORANGE), nodes[10][0].animate.set_fill(ORANGE)),
            AnimationGroup(nodes[1][0].animate.set_fill(GREEN_D), nodes[6][0].animate.set_fill(GREEN_D), nodes[14][0].animate.set_fill(GREEN_D)),
            AnimationGroup(nodes[4][0].animate.set_fill(GREEN_D), nodes[7][0].animate.set_fill(GREEN_D), nodes[13][0].animate.set_fill(GREEN_D))
        ]
        self.play(Succession(*glow_anims), run_time=2.5)
        slogan = Text("Think in Subtrees!", font_size=26, weight=BOLD, color=YELLOW_B).to_edge(DOWN, buff=1.4)
        self.play(FadeIn(slogan, shift=UP), run_time=1.2)
        self.wait(dur19 - (1.5 + 2.5 + 1.2))
