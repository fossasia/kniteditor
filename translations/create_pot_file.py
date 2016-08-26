#!/usr/bin/python3

import os
import re
from pprint import pprint

ENDINGS = [".html"]

HERE = os.path.abspath(os.path.dirname(__file__))
TRANSLATION_ROOT = os.path.abspath(os.path.join(HERE, '..'))

os.chdir(TRANSLATION_ROOT)

translations = []

# search for these
# 
#   translations["..."]
#   translation["..."]
#
# and list them
translation_pattern = re.compile("((.*?\\{\\{[^\\}\\{]*?translat(?:ions?|e)\\s*\[\\s*)[\\s*'\"]([^\\}\\{]*?)[\\s*'\"]\\s*\\][^\}\{]*?\\}\\})", re.DOTALL)

for root, dirs, files in os.walk("."):
    for file in files:
        if any(file.lower().endswith(ending) for ending in ENDINGS):
            file_path = os.path.join(root, file)
            with open(file_path) as file:
                line_number = 1
                for all, before, string in translation_pattern.findall(file.read()):
                    current_line_number = line_number + before.count("\n")
                    line_number += all.count("\n")
                    translations.append((string, current_line_number, file_path))

pprint(translations)

