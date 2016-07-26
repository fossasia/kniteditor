"""This module provides translation functionality.

Functions exported are:

- :func:`_(string) <_>` to translate strings
- :func:`change_language_to(language) <change_language_to>` to change the
  language of the entire application

"""
import os
import gettext
from os.path import abspath, join, dirname

_locale_dir = abspath(join(dirname(__file__), 'translations'))
_current_language = None
_locales = None
DEFAULT_LANGUAGE = "en"  #: the default language to use
DOMAIN = "kniteditor"  #: the name of the .po files


def _(string):
    """Translate a string using the current language.

    :param str string: the string to translate
    :return: the translated string
    :rtype: str
    """
    return _locales.gettext(string)


def change_language_to(new_language):
    """Change the language to a language folder in the translations folder.

    :param str new_language: The language code to translate everything into.
      This code must be listed in :func:`list_languages`.
    :raises ValueError: if :paramref:`new_language` is not listed by
      :func:`list_languages`
    """
    global _locales, _current_language
    _locales = gettext.translation(DOMAIN, _locale_dir,
                                   languages=[new_language])
    _current_language = new_language


def list_languages():
    """Return a list of all supported languages.

    :return: a list of :class:`strings <str>` of language codes that can be
      passed as an argument to :func:`change_language_to`
    :rtype: list
    """
    supported_languages = []
    for folder_name in os.listdir(_locale_dir):
        folder = os.path.join(_locale_dir, folder_name)
        if os.path.isdir(folder):
            if "LC_MESSAGES" in os.listdir(folder):
                supported_languages.append(folder_name)
    return supported_languages


def current_language():
    """Return the current language.

    :return: a language listed by :func:`list_languages`
    :rtype: str
    """
    return _current_language

change_language_to(DEFAULT_LANGUAGE)

__all__ = ["_", "change_language_to", "list_languages", "DEFAULT_LANGUAGE",
           "current_language"]
