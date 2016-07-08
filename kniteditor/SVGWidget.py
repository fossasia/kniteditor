from kivy.uix.scatter import Scatter
from kivy.graphics.svg import Svg


class SVGWidget(Scatter):

    """This is the widget for an instruction to display."""

    # https://github.com/kivy/kivy/blob/master/examples/svg/main.py

    def __init__(self, filename, **kwargs):
        """Render the instruction given as svg as a file name."""
        super().__init__(**kwargs)
        with self.canvas:
            svg = Svg(filename)
        self.size = svg.width, svg.height

__all__ = ["SVGWidget"]
