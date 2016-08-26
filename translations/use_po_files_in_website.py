#!/usr/bin/python3

import os
import re
import json
from collections import defaultdict
import pprint
import operator

# user defined constants
TRANSLATIONS = "../_data/translations.yml"

# computed constants
HERE = os.path.abspath(os.path.dirname(__file__))
TRANSLATIONS_PATH = os.path.join(HERE, TRANSLATIONS)

strings = defaultdict(dict)  # string : {language : translation}

translation_pattern = re.compile("^msgid((?:[^\n]|\n[^\n])*)\nmsgstr((?:[^\n]|\n[^\n])*)(?:\n\n|\n?$)", re.MULTILINE)
string_pattern = re.compile("\"((?:[^\"]|\\\\|\\\")*?)\"")

def string_from(translation_match):
    return json.loads("\"" + "".join(string_pattern.findall(translation_match)) + "\"")

for file_name in os.listdir(HERE):
    language, ext = os.path.splitext(file_name)
    if ext.lower() == ".po":
        file_path = os.path.join(HERE, file_name)
        with open(file_path, encoding="UTF-8") as file:
            for id, translation in translation_pattern.findall(file.read()):
                _id = string_from(id)
                if not _id:
                    continue
                _translation = string_from(translation)
                print("{}: {} => {}".format(language, repr(_id), repr(_translation)))
                strings[_id][language] = _translation


first = operator.itemgetter(0)

with open(TRANSLATIONS_PATH, "w", encoding="UTF-8") as file:
    for string, languages in sorted(strings.items(), key=first):
        file.write("\n")
        json.dump(string, file)
        file.write(":\n")
        for language, translation in sorted(languages.items(), key=first):
            file.write("  ")
            json.dump(language, file)
            file.write(": ")
            json.dump(translation, file)
            file.write("\n")
        

