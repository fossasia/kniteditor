"""This module contains the editor window."""
import knittingpattern

from kivy.app import App
from kivy.uix.button import Button

import sys
from glob import glob
from os.path import join, dirname
from kivy.uix.scatter import Scatter
from kivy.app import App
from kivy.graphics.svg import Svg
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout


class SvgWidget(Scatter):
    # https://github.com/kivy/kivy/blob/master/examples/svg/main.py

    def __init__(self, filename, **kwargs):
        super(SvgWidget, self).__init__(**kwargs)
        with self.canvas:
            svg = Svg(filename)
        self.size = svg.width, svg.height

class EditorWindow(App):

    """The editor window."""

    def build(self):
        """Build the UI elements."""
        self.root = FloatLayout()
        
        # example = knittingpattern.load_from().example("Cafe.json")
        # filename = example.to_svg(1).temporary_path(".svg")
        filename = r"C:\Users\cheche\Documents\programmiertes\kniitting\knittingpattern\knittingpattern\convert\instruction-svgs\cdd.svg"

        svg = SvgWidget(filename, size_hint=(None, None))
        self.root.add_widget(svg)
        svg.scale = 1
        svg.center = Window.center
        


def main():
    """Open the editor window."""
    EditorWindow().run()

__all__ = ["main", "EditorWindow"]
