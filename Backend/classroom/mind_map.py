import graphviz
import random
import re
from .watsonx_utils import call_llm
from uuid import uuid4
from pathlib import Path

class MindMapGenerator:
    root_path: str = "minds_maps"
    main_prompt: str = "<s> [INST] ارجو منك تقسيم درس {} ل 5 أقسام وفروعها لتشكيل خريطة ذهنية باللغة العربية لدرس {} [/INST]"
    def __init__(self, section: str):
        self.section = section

    def parse_outline(self, resp_text):
        lines = resp_text.splitlines()
        mind_map = {}
        stack = []
        last_level = 0

        for line in lines:
            line = line.rstrip()
            if not line:
                continue

            # Determine the level of the current line based on numbering
            match = re.match(r'^(\s*)(\d+|[ء-ي])\.\s*(.*)', line)
            if match:
                indent, marker, content = match.groups()
                level = (len(indent) // 3) + 1  # Each indentation level is 3 spaces

                # Adjust the stack to the current level
                while len(stack) > level - 1:
                    stack.pop()

                node = content.strip(':')
                current_dict = {}
                if not stack:
                    # We're at the root level
                    mind_map[node] = current_dict
                    stack.append(mind_map[node])
                else:
                    # Add to the last dictionary in the stack
                    stack[-1][node] = current_dict
                    stack.append(stack[-1][node])
            else:
                # Lines without numbering are ignored or can be handled here
                continue

        return mind_map

    def create_arabic_mind_map(self, ideas, filename="arabic_mind_map"):
        dot = graphviz.Digraph(comment="Arabic Mind Map", format="png")
        dot.attr(rankdir="RL", size="12,8")
        dot.attr("node", shape="rectangle", style="rounded,filled", fontname=r"C:\Users\user\Downloads\Noto_Sans_Arabic\static\NotoSansArabic_Condensed-Black.ttf", fontsize="14")
        dot.attr("edge", color="#7C7C7C", dir="back")  # Change arrow direction

        color_palette = ["#FFD700", "#FF6347", "#4682B4", "#32CD32", "#FF69B4", "#9370DB", "#20B2AA"]

        def add_nodes(parent_id, parent_label, children, level=0):
            # Generate a unique node ID
            parent_node_id = f"node_{random.randint(1, 100000)}"
            fillcolor = color_palette[level % len(color_palette)]
            dot.node(parent_node_id, parent_label, fillcolor=fillcolor, fontcolor="#000000")

            if parent_id is not None:
                dot.edge(parent_node_id, parent_id, penwidth="1.5")

            if isinstance(children, dict):
                for key, value in children.items():
                    add_nodes(parent_node_id, key, value, level + 1)
            elif isinstance(children, list):
                for item in children:
                    # For list items, treat them as leaf nodes
                    node_id = f"node_{random.randint(1, 100000)}"
                    fillcolor = color_palette[(level + 1) % len(color_palette)]
                    dot.node(node_id, item, fillcolor=fillcolor, fontcolor="#000000")
                    dot.edge(node_id, parent_node_id, penwidth="1.5")

        # Start adding nodes from the root(s)
        for root_label, root_children in ideas.items():
            add_nodes(None, root_label, root_children)

        # Use fdp layout engine for a more organic look
        dot.engine = "fdp"

        # Save the mind map
        dot.render(filename, self.root_path, format="png", cleanup=True)
        print(f"Arabic mind map saved as {filename}.png")

    def __call__(self):
        prompt = self.main_prompt.format(self.section, self.section)
        print(f"{prompt=}")
        text = call_llm(prompt)
        mind_maps_ideas = self.parse_outline(
            text
        )
        print(f"{mind_maps_ideas=}")

        filename = str(uuid4())
        self.create_arabic_mind_map({self.section : mind_maps_ideas}, filename)
        return Path(self.root_path) / f"{filename}.png"