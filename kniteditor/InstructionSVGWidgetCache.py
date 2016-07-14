"""This module allows fast access to instruction SVGs."""
from knittingpattern.convert.InstructionSVGCache import default_svg_cache
from kivy.uix.scatter import Scatter
from kivy.graphics.svg import Svg


class SVGWidget(Scatter):

    """This is the widget for an instruction to display."""

    def __init__(self, svg, **kwargs):
        """Render the instruction given as svg as a file name."""
        super().__init__(**kwargs)
        self.canvas.add(svg)
        self.size = svg.width, svg.height


class InstructionSVGWidgetCache(object):

    """A chache to create widgets with instruction SVGs fast."""

    def __init__(self, svg_cache=None):
        """Create an InstructionSVGWidgetCache.

        :param svg_cache: a :class:`
          knitingpattern.convert.InstructionSVGCache.InstructionSVGCache` or
          :obj:`None` if :func:`
          knitingpattern.convert.InstructionSVGCache.default_svg_cache`
          shall be used
        """
        if svg_cache is None:
            svg_cache = default_svg_cache()
        self._svg_cache = svg_cache
        self._get_instruction_id = self._svg_cache.get_instruction_id
        self._svg_widget_cache = {}

    def create_svg_widget(self, instruction, **kw):
        """Create an SVGWidget for the instruction.

        :param instruction: an
          :class:`~knittingpattern.Instruction.Instruction`
        :param dict kw: they keyword arguments to pass to the widget
        :rtype: SVGWidget
        """
        instruction_id = self._get_instruction_id(instruction)
        if instruction_id in self._svg_widget_cache:
            svg = self._svg_widget_cache[instruction_id]
        else:
            dumper = self._svg_cache.to_svg(
                instruction, i_promise_not_to_change_the_result=True)
            svg = dumper.kivy_svg()
            self._svg_widget_cache[instruction_id] = svg
        return SVGWidget(svg, **kw)


def default_cache():
    """Return the default InstructionSVGWidgetCache.

    :rtype: InstructionSVGWidgetCache.InstructionSVGWidgetCache
    """
    global _cache
    if _cache is None:
        _cache = InstructionSVGWidgetCache()
    return _cache
_cache = None

__all__ = ["InstructionSVGWidgetCache", "SVGWidget", "default_cache"]
