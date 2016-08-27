#!/usr/bin/python3

import os
import re
import json
from collections import defaultdict, OrderedDict
import pprint
import operator

# user defined constants
TRANSLATIONS = "../_data/translations.yml"
DEFAULT_LANGUAGE = "en"

# computed constants
HERE = os.path.abspath(os.path.dirname(__file__))
TRANSLATIONS_PATH = os.path.join(HERE, TRANSLATIONS)


translation_pattern = re.compile("^msgid((?:[^\n]|\n[^\n])*)\nmsgstr((?:[^\n]|\n[^\n])*)(?:\n\n|\n?$)", re.MULTILINE)
string_pattern = re.compile("\"((?:\\\\\\\\|\\\\[^\\\\]|[^\"\\\\])*)\"")

def string_from(translation_match):
    matches = string_pattern.findall(translation_match)
    return json.loads("\"" + "".join(matches) + "\"")


strings = defaultdict(OrderedDict)  # language : {id : translation}
po_files = {file for file in os.listdir(HERE) if file.lower().endswith(".po")}
all_languages = set()
ids = set()

for file_name in sorted(po_files):
    language, ext = os.path.splitext(file_name)
    all_languages.add(language)
    file_path = os.path.join(HERE, file_name)
    with open(file_path, encoding="UTF-8") as file:
        content = file.read()
        for id, translation in translation_pattern.findall(content):
            print("{} id: {} => {}".format(language, repr(id), repr(translation)))
            _id = string_from(id)
            if not _id:
                continue
            _translation = string_from(translation)
            strings[language][_id] = _translation
            ids.add(_id)


first = operator.itemgetter(0)
def dump_translation(file, key, value):
    file.write("  ")
    json.dump(key, file)
    file.write(": ")
    json.dump(value, file)
    file.write("\n")
    
with open(TRANSLATIONS_PATH, "w", encoding="UTF-8") as file:
    for language in sorted(all_languages):
        file.write("\n")
        json.dump(language, file)
        file.write(":\n")
        for id, translation in strings[language].items():
            dump_translation(file, id, translation)
        not_translated = ids - set(strings[language])
        if not_translated:
            file.write("  # missing translation:\n")
            for id in not_translated:
                if id not in strings[DEFAULT_LANGUAGE]:
                    print("Obsolete translation: {}".format(repr(id)))
                else:
                    dump_translation(file, id, strings[DEFAULT_LANGUAGE][id])