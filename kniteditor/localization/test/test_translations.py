from kniteditor.localization import _, change_language_to, list_languages, \
    DEFAULT_LANGUAGE, current_language
import pytest


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
def test_switching_lamguage_sets_current_language(language):
    change_language_to(language)
    assert current_language() == language
