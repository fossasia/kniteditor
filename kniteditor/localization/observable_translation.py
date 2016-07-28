"""Observable Translations for kivy that change when the language changes.

The functionality of this module is highly inspired by
`kivy-gettext-example <https://github.com/tito/kivy-gettext-example>`.

"""
from kivy.lang import Observable


class ObservableTranslation(Observable):

    """This class allows kivy translations to be updated with the language."""

    def __init__(self, translate):
        """Create a new translation object with a translation function.

        :param translate: a callable that translates the text. Even when the
          language is changed, it returns the text for the currrent language.
        """
        super().__init__()
        self._translate = translate
        self._observers = []

    def __call__(self, text):
        """Call this object to translate text.

        :param str text: the text to translate
        :return: the text translated to the current language
        """
        return self._translate(text)

    def fbind(self, name, func, args, **kwargs):
        """Add an observer. This is used by kivy."""
        self._observers.append((name, func, args, kwargs))

    def funbind(self, name, func, args, **kwargs):
        """Remove an observer. This is used by kivy."""
        key = (name, func, args, kwargs)
        if key in self._observers:
            self._observers.remove(key)

    def language_changed(self):
        """Update all the kv rules attached to this text."""
        for name, func, args, kwargs in self._observers:
            func(args, None, None)

__all__ = ["ObservableTranslation"]
