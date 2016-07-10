"""This module contains a widget to display knittingpatterns.

This module is a kivy display for :class:`knitting patterns
<knittingpattern.KnittingPatternSet.KnittingPatternSet>`.
"""
from kivy.uix.floatlayout import FloatLayout
from knittingpattern.convert.Layout import GridLayout
from .InstructionSVGWidgetCache import default_cache


class KnittingPatternWidget(FloatLayout):

    """The widget to display a knittitng pattern."""

    def __init__(self, patterns, **kw):
        super().__init__(**kw)
        self._patterns = patterns

    def build(self):
        """Build the UI elements."""
        self.clear_widgets()
        pattern = self._patterns.patterns.at(0)
        layout = GridLayout(pattern)
        cache = default_cache()
        zoom = 20
        bbox = layout.bounding_box
        min_y = bbox[1]
        flip_x = bbox[2]
        instructions = list(layout.walk_instructions())
        instructions.sort(key=lambda i: i.instruction.render_z)
        for instruction in instructions:
            svg = cache.create_svg_widget(instruction.instruction,
                                          size_hint=(None, None))
            self.add_widget(svg)
            svg.scale = zoom / svg.height
            # TODO: fixpositioning according to svg rendering
            right = (flip_x - instruction.x) * zoom
            svg.set_right(right)
            svg.y = (instruction.y - min_y) * zoom

__all__ = ["KnittingPatternWidget"]
