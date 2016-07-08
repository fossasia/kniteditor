"""This module contains the editor window."""
import knittingpattern
import os
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout

from knittingpattern.convert.Layout import GridLayout
from .InstructionSVGWidgetCache import default_cache

class EditorWindow(App):

    """The editor window."""

    def build(self):
        """Build the UI elements."""
        self.root = FloatLayout()

        # patterns = knittingpattern.load_from_relative_file("knittingpattern",
        #     "convert/test/test_patterns/block4x4.json")
        patterns = knittingpattern.load_from().example("Cafe.json")
        pattern = patterns.patterns.at(0)
        layout = GridLayout(pattern)
        cache = default_cache()
        instruction_height = 20
        min_x, min_y, max_x, max_y = layout.bounding_box
        width = max_x - min_x
        height = max_y - min_y
        instructions = list(layout.walk_instructions())
        instructions.sort(
            key=lambda i: i.instruction.get("render", {}).get("z", 0))
        for instruction in instructions:
            print(instruction.instruction.type, instruction.x, instruction.y)
            svg = cache.create_svg_widget(
                instruction.instruction, size_hint=(None, None))
            self.root.add_widget(svg)
            svg.scale = instruction_height / svg.height
            # TODO: fixpositioning according to svg rendering
            svg.set_right((width - instruction.x + min_x + 1) * instruction_height)
            svg.y = (instruction.y - min_y + 1) * instruction_height


def main():
    """Open the editor window."""
    EditorWindow().run()

__all__ = ["main", "EditorWindow"]
