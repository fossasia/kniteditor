#!/usr/bin/python3

import os
import re
from pprint import pprint
import json
from collections import OrderedDict

# user defined constants
ENDINGS = [".html"]
POT_FILE_NAME = "website.pot"
EN_FILE_NAME = "en.po"
POT_HEADER = """
msgid ""
msgstr ""
"Project-Id-Version: \\n"
"POT-Creation-Date: \\n"
"PO-Revision-Date: \\n"
"Last-Translator: \\n"
"Language-Team: \\n"
"Language: en_US\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"""


# computed constants
HERE = os.path.abspath(os.path.dirname(__file__))
TRANSLATION_ROOT = os.path.abspath(os.path.join(HERE, '..'))
POT_FILE_PATH = os.path.join(HERE, POT_FILE_NAME)
EN_FILE_PATH = os.path.join(HERE, EN_FILE_NAME)


os.chdir(TRANSLATION_ROOT)


# search for these
# 
#   translations["..."]
#   translation["..."]
#
# and list them
translation_pattern = re.compile("((.*?\\{\\{[^\\}\\{]*?translat(?:ions?|e)\\s*\[\\s*)[\\s*'\"]([^\\}\\{]*?)[\\s*'\"]\\s*\\][^\}\{]*?\\}\\})", re.DOTALL)
title_pattern = re.compile("(^---(?:[^\n]|\n(?=[^-])|\n(?=-[^-])|\n(?=--[^-]))*)title:\s*([^\n]*?)\s*\n")

translations = OrderedDict()

def translate(string, file_path, line, note=""):
    translations.setdefault(string, [])
    translations[string].append((file_path, line, note))

for root, dirs, files in os.walk("."):
    for file in sorted(files):
        if any(file.lower().endswith(ending) for ending in ENDINGS):
            file_path = os.path.join(root, file)
            with open(file_path) as file:
                content = file.read()
            # title
            titles = title_pattern.findall(content)
            for before, title in titles:
                current_line_number = before.count("\n")
                translate(title, file_path, current_line_number)
            # content
            line_number = 1
            for all, before, string in translation_pattern.findall(content):
                current_line_number = line_number + before.count("\n")
                line_number += all.count("\n")
                translate(string, file_path, current_line_number)

potify = json.dumps

with open(POT_FILE_PATH, "w", encoding="UTF-8") as pot_file, \
     open(EN_FILE_PATH, "w", encoding="UTF-8") as en_file:
    pot_file.write(POT_HEADER)
    en_file.write(POT_HEADER)
    for string in translations:
        msgid = "msgid {}\n".format(potify(string))
        comment = ""
        for file_path, line, note in translations[string]:
            if file_path[:2] in ("./", ".\\"):
                file_path = file_path[2:]
            file_path = file_path.replace("\\", "/")
            comment += "# file {} line {}\t{}\n".format(file_path, line, note)
        
        pot_file.write("\n")
        pot_file.write(comment)
        pot_file.write(msgid)
        pot_file.write("msgstr \"\"\n")
        
        
        en_file.write("\n")
        en_file.write(comment)
        en_file.write(msgid)
        en_file.write("msgstr {}\n".format(potify(string)))

