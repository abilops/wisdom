#! /usr/bin/python

import os
import sys
import re

ROOT = "."
if len(sys.argv) == 2:
    ROOT = sys.argv[1]

INPUT=os.path.join(ROOT, "wisdom.md")
DIR = os.path.dirname(INPUT)
BASE = os.path.basename(INPUT)
OUTPUT = os.path.join(DIR, 'ebooks', BASE+".tex")
print(f"Reading from {INPUT}")

ESCAPE=['%', '\\$', '#', '@', '&','\\^']

class LatexWriter():
    def __init__(self):
        last_top_index = None
        return
    def top(self):
        pass
    def bottom(self):
        pass
    def hrule(self, line):
        return "\dashdash"
    def wisdom(self, lines):
        # Escape all bad stuff
        for c in ESCAPE:
            lines = re.sub(c, '\\' + c, lines)
        # TODO:Process basic basic markdown
        if lines.startswith(("Related", 
                             "Corollary", 
                             "Relatedly related", 
                             "Thus"
                             "But",
                             "Alternatively",
                             "Unrelated",)):
            if ':' in lines:
                colon = lines.find(':')
            elif '.' in lines:
                colon = lines.find('.')
            command = lines[:colon]
            lines = lines[colon+1:]
            lines = lines.strip()
        else:
            command = ''
        return "\\wisdom" + "[" + command + "]" + "{" + lines + "}" 
        # return "\\" + command + "{" + lines + "}" 

with open(INPUT, 'r') as f:
    wisdoms = f.readlines()

# Ignore everything above this line
start = wisdoms.index("## The Wisdom So Far\n")
wisdoms = wisdoms[start:]

Writer = LatexWriter()
out = []
for i in range(len(wisdoms)):
    line = wisdoms[i]
    # Remove whitespace from both sides
    line = line.strip()
    # Empty lines
    if line == '':
        continue
    # hrules
    elif line.startswith('---'):
        out.append(Writer.hrule(line))
    elif line.startswith('<hr'):
        out.append(Writer.hrule(line))
    elif line.startswith('- '):
        out.append(Writer.wisdom(line[2:]))

with open(OUTPUT, 'w') as f:
    f.write('\n'.join(out))
print(f"Wrote to {OUTPUT}")
