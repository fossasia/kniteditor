"""This module contains a widget to display knittingpatterns.

This module is a kivy display for :class:`knitting patterns
<knittingpattern.KnittingPatternSet.KnittingPatternSet>`.
"""
from kivy.uix.floatlayout import FloatLayout
from knittingpattern.convert.Layout import GridLayout
from .InstructionSVGWidgetCache import default_cache
from kivy.graphics import Rectangle, Color
from kivy.graphics.instructions import InstructionGroup


class KnittingPatternWidget(FloatLayout):

    """The widget to display a knittitng pattern."""

    def __init__(self, **kw):
        super().__init__(**kw)
        self._pattern = None
        self._mark = None

    def show_pattern(self, pattern):
        """Show a knitting pattern.

        :param knittingpattern.KnittingPattern.KnittingPattern pattern: the
          pattern to display
        """
        self._pattern = pattern
        self._layout = GridLayout(self._pattern)
        self._bbox = self._layout.bounding_box
        self._cache = default_cache()
        self._instructions = list(self._layout.walk_instructions())
        self._instructions.sort(key=lambda i: i.instruction.render_z)
        self.update_widget()

    def update_widget(self):
        """Call after a resize to rerender the elements to fit."""
        if not self._pattern:
            return
        self.clear_widgets()
        bbox = self._bbox
        bbox_width = bbox[2] - bbox[0]
        bbox_height = bbox[3] - bbox[1]
        print(bbox, self.height, self.width)
        zoom = 20  # min(self.height / bbox_height, self.width / bbox_width)
        min_y = bbox[1] - 0.618
        flip_x = bbox[0] + bbox[2] + 1.618
        create_svg_widget = self._cache.create_svg_widget
        for instruction in self._instructions:
            svg = create_svg_widget(instruction.instruction,
                                    size_hint=(None, None))
            self.add_widget(svg)
            svg.scale = zoom / svg.height
            svg.x = (flip_x - instruction.x - instruction.width) * zoom
            svg.y = (instruction.y - min_y) * zoom
        self._zoom = zoom
        self._min_y = min_y
        self._flip_x = flip_x

    def mark_row(self, row, border_width=1):
        """Mark a row. Th eold mark is removed."""
        assert self._pattern, "I can only mark a row if I show a pattern."
        row = self._layout.row_in_grid(row)
        if self._mark:
            self.canvas.remove(self._mark)
        width = row.width * self._zoom + border_width + border_width
        height = row.height * self._zoom + border_width + border_width
        x = (self._flip_x - row.x - row.width) * self._zoom - border_width
        y = (row.y - self._min_y) * self._zoom - border_width
        self._mark = InstructionGroup()
        self._mark.add(Color(0, 0, 1, 1))
        self._mark.add(Rectangle(pos=(x, y), size=(width, border_width)))
        self._mark.add(Rectangle(pos=(x, y + height),
                                 size=(width, border_width)))
        self._mark.add(Rectangle(pos=(x, y), size=(border_width, height)))
        self._mark.add(Rectangle(pos=(x + width, y),
                                 size=(border_width, height)))
        self.canvas.add(self._mark)


__all__ = ["KnittingPatternWidget"]
