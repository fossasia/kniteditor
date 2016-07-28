import test_localization
from kniteditor.localization import _, change_language_to, list_languages, \
    DEFAULT_LANGUAGE, current_language, language_code_to_translation, \
    translation_to_language_code, list_translated_languages, \
    current_translated_language, change_language_to_translated
import pytest
from pytest import raises


def test_current_language_is_default_language():
    assert current_language() == DEFAULT_LANGUAGE


def test_default_language_is_english():
    assert DEFAULT_LANGUAGE == "en"


@pytest.mark.parametrize("language", ["de", "en"])
def test_languages_are_listed(language):
    assert language in list_languages()


@pytest.mark.parametrize("word,translation", [("yes", "yes"), ("no", "no")])
def test_translate_in_default_language(word, translation):
    assert _(word) == translation


@pytest.mark.parametrize("language,word,translation", [
    ("en", "Yes", "Yes"), ("en", "No", "No"),
    ("de", "Yes", "Ja"), ("de", "No", "Nein")])
def test_translate_in_default_language(language, word, translation):
    change_language_to(language)
    assert _(word) == translation


@pytest.mark.parametrize("language", ["de", "en", "en", "de", "de"])
def test_switching_language_sets_current_language(language):
    change_language_to(language)
    assert current_language() == language


@pytest.mark.parametrize("code,translation", [("de", "Deutsch"),
                                              ("en", "English")])
def test_language_translation(code, translation):
    assert language_code_to_translation(code) == translation
    assert translation_to_language_code(translation) == code


@pytest.mark.parametrize("code", ["invalid!!!!", "123"])
def test_value_error_in_language_code_to_translation(code):
    with raises(ValueError) as error:
        language_code_to_translation(code)
    message = "Invalid language code {}. Expected one of {}.".format(
        repr(code), ", ".join(map(repr, list_languages())))
    assert error.value.args[0] == message


@pytest.mark.parametrize("code", ["invalid!!!!", "123", "en"])
@pytest.mark.parametrize("function", [change_language_to_translated,
                                      translation_to_language_code])
def test_value_error_in_translation_to_language_code(code, function):
    with raises(ValueError) as error:
        function(code)
    message = "Invalid language name {}. Expected one of {}.".format(
        repr(code), ", ".join(map(repr, map(language_code_to_translation,
                                            list_languages()))))
    assert error.value.args[0] == message


@pytest.mark.parametrize("code", [None, object(), object])
@pytest.mark.parametrize("function", [language_code_to_translation,
                                      translation_to_language_code])
def test_type_error_in_language_code_to_translation(code, function):
    with raises(TypeError) as error:
        function(code)
    message = "Invalid argument {}. Expected str instance.".format(
        repr(code))
    assert error.value.args[0] == message


def test_list_translated_languages_have_no_duplicate():
    translated_languages = list_translated_languages()
    assert len(set(translated_languages)) == len(translated_languages)


@pytest.mark.parametrize("code", list_languages())
def test_all_languages_in_translated_languages(code):
    assert language_code_to_translation(code) in list_translated_languages()


@pytest.mark.parametrize("code", list_languages())
def test_can_set_translated_language(code):
    translated = language_code_to_translation(code)
    change_language_to_translated(translated)
    assert current_language() == code
    assert current_translated_language() == translated
