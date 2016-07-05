"""This module contains the editor window."""
import knittingpattern
import os
from kivy.uix.scatter import Scatter
from kivy.app import App
from kivy.graphics.svg import Svg
from kivy.uix.floatlayout import FloatLayout

from knittingpattern.convert.Layout import GridLayout


class SvgWidget(Scatter):

    """This is the widget for a instruction to display."""

    # https://github.com/kivy/kivy/blob/master/examples/svg/main.py

    def __init__(self, filename, **kwargs):
        """Render the instruction given as svg as a file name."""
        super(SvgWidget, self).__init__(**kwargs)
        with self.canvas:
            svg = Svg(filename)
        self.size = svg.width, svg.height


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
        dir = os.path.dirname(knittingpattern.__file__)
        filename = os.path.join(dir, "convert", "instruction-svgs", "{}.svg")
        height = 20
        min_x, min_y, max_x, max_y = layout.bounding_box
        width = max_x - min_x
        height = max_y - min_y
        instructions = list(layout.walk_instructions())
        instructions.sort(
            key=lambda i: i.instruction.get("render", {}).get("z", 0))
        for instruction in instructions:
            print(instruction.instruction.type, instruction.x, instruction.y)
            svg = SvgWidget(filename.format(instruction.instruction.type),
                            size_hint=(None, None))
            self.root.add_widget(svg)
            svg.scale = height / svg.height
            svg.set_right((width - instruction.x + min_x + 1) * height)
            svg.y = (instruction.y - min_y + 1) * height


def main():
    """Open the editor window."""
    EditorWindow().run()

__all__ = ["main", "EditorWindow", "SvgWidget"]
