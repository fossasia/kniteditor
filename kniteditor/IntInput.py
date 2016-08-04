from kivy.factory import Factory
from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty
import re

_make_integer_pattern = re.compile('[^0-9]')


def make_integer(string):
    """Extract the interger from a string.

    :param str string: the string to make to an integer
    :return: the string as an integer
    :rtype: str
    """
    return _make_integer_pattern.sub("", string)


class IntInput(TextInput):

    """An input that only takes integers.

    .. seealso:: :mod:`kivy.uix.textinput`
    """

    #: the value as an integer
    value = NumericProperty(0)

    def insert_text(self, substring, from_undo=False):
        """When text is inserted."""
        string = make_integer(substring)
        return super().insert_text(string, from_undo=from_undo)

    def on_text(self, instance, text):
        """When the text changes, change the :attr:`value`."""
        if str(self.value) != text:
            self.value = int(text or 0)

    def on_value(self, instance, value):
        """when the :attr:`value` changes, change the text."""
        if self.text != str(int(value)):
            self.text = str(int(value))


Factory.register('IntInput', cls=IntInput)

__all__ = ["make_integer", "IntInput"]
