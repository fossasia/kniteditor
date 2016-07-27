"""This module provides translation functionality.

Functions exported are:

- :func:`_(string) <_>` to translate strings
- :func:`change_language_to(language) <change_language_to>` to change the
  language of the entire application

"""
import os
import gettext
from os.path import abspath, join, dirname

_here = dirname(__file__)
_locale_dir = abspath(join(_here, 'translations'))
_current_language = None
_locales = None
DOMAIN = "kniteditor"  #: the name of the .po files

_languages_dir = "languages"
_languages_locales = gettext.translation(_languages_dir, _locale_dir,
                                         languages=[_languages_dir])


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


_supported_languages = []
for folder_name in os.listdir(_locale_dir):
    folder = os.path.join(_locale_dir, folder_name)
    if os.path.isdir(folder):
        if "LC_MESSAGES" in os.listdir(folder):
            _supported_languages.append(folder_name)
    del folder, folder_name


def list_languages():
    """Return a list of all supported languages.

    :return: a list of :class:`strings <str>` of language codes that can be
      passed as an argument to :func:`change_language_to`
    :rtype: list
    """
    return _supported_languages.copy()


def language_code_to_translation(language_code):
    """Translate a language code.
    
    Note that all language names are written in their language so that
    people can read them in their language.
    
    :rtype: str
    :return: the translated language
    :param str language_code: a language code from :func:`list_languages`
    :raises ValueError: if the code is not in :func:`list_languages`
    :raises TypeError: if the code is not a string
    
    .. note:: this operation can be reversed by
      :func:`translation_to_language_code`
      
    .. code:: python
    
        c2 = language_code_to_translation(language_code_to_translation(c1))
        assert c1 == c2

    """
    if not isinstance(language_code, str):
        message = "Invalid argument {}. Expected str instance.".format(
            repr(language_code))
        raise TypeError(message)
    if language_code not in list_languages():
        message = "Invalid language code {}. Expected one of {}.".format(
            repr(language_code), ", ".join(map(repr, list_languages())))
        raise ValueError(message)
    return _languages_locales.gettext(language_code)


def translation_to_language_code(translated_language_code):
    """Translate a language back to a langugage code.
    
    :param str translated_language_code: a language returned by
      :func:`language_code_to_translation`
    :rtype: str
    :return: a language code in :func:`list_languages`
    :raises ValueError: if this translation is not known
    """
    if not isinstance(translated_language_code, str):
        message = "Invalid argument {}. Expected str instance.".format(
            repr(translated_language_code))
        raise TypeError(message)
    expected = []
    for language_code in list_languages():
        translation = language_code_to_translation(language_code)
        expected.append(translation)
        if translation == translated_language_code:
            return language_code
    message = "Invalid language name {}. Expected one of {}.".format(
        repr(translated_language_code), ", ".join(map(repr, expected)))
    raise ValueError(message)


def current_language():
    """Return the current language.

    :return: a language listed by :func:`list_languages`
    :rtype: str
    """
    return _current_language


def kivy(string):
    """Return a translated, displayable object for the UI.
    
    .. seealso:: :func:`_`
    """
    return _(string)
    

DEFAULT_LANGUAGE = "en"  #: the default language to use
change_language_to(DEFAULT_LANGUAGE)

__all__ = ["_", "change_language_to", "list_languages", "DEFAULT_LANGUAGE",
           "current_language", "kivy", "translate_language", 
           "language_code_to_translation", "translation_to_language_code"]
