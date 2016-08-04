from kivy.factory import Factory
from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty
import re

_make_integer_pattern = re.compile('[^0-9]')


def make_integer(string):
    return _make_integer_pattern.sub("", string)


class IntInput(TextInput):

    """An input that only takes integers.

    .. seealso:: :mod:`kivy.uix.textinput`
    """

    value = NumericProperty(0)

    def insert_text(self, substring, from_undo=False):
        string = make_integer(substring)
        return super().insert_text(string, from_undo=from_undo)

    def on_text(self, instance, text):
        if str(self.value) != text:
            self.value = int(text or 0)

    def on_value(self, instance, value):
        if self.text != str(int(value)):
            self.text = str(int(value))


Factory.register('IntInput', cls=IntInput)
