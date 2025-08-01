#! /usr/bin/python

import os
import sys
import re

ROOT = "."
# If a single argument is provided, use it. Otherwise ignore
if len(sys.argv) == 2:
    ROOT = sys.argv[1]

# Infer all paths from the root directory
INPUT = os.path.join(ROOT, "wisdom.md")
DIR = os.path.dirname(INPUT)
BASE = os.path.basename(INPUT)
OUTPUT = os.path.join(DIR, 'ebooks', BASE+".tex")
PRE = os.path.join(DIR, 'ebooks', "pre.tex")
print(f"Reading from {INPUT}")

# All symbols that trip up the LaTeX compiler
ESCAPE=['%', '\\$', '#', '@', '&','\\^']

# Class allows me to easily define a new output format later
class LatexWriter():
    def __init__(self):
        last_top_index = None
        return
    # TODO: At the top of the file
    def top(self):
        pass
    # TODO: At the bottom of the file
    def bottom(self):
        pass
    def hrule(self, line):
        return "\dashdash"
    # Function for each wisdom line
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
            # Because one "Related" has a full stop instead of a colon
            if ':' in lines:
                colon = lines.find(':')
            elif '.' in lines:
                colon = lines.find('.')
            # Remove the "Related: "
            command = lines[:colon]
            lines = lines[colon+1:]
            lines = lines.strip()
        else:
            command = ''
        return "\\wisdom" + "[" + command + "]" + "{" + lines + "}" 
        # return "\\" + command + "{" + lines + "}" 
    def item(self, line):
        return "\\remark{" + line + "}"
    def by(self, line):
        return "\\byline{" + line + "}"
    def text(self, line):
        return line + "\\\\"
    def section(self, line):
        return "\\section*{" + line + "}"

# Read input
with open(INPUT, 'r') as f:
    wisdoms = f.readlines()

# Ignore everything above this line
start = wisdoms.index("## Voi ch'entrate…\n")
wstart = wisdoms.index("## The Wisdom So Far\n")

Writer = LatexWriter()
pre = []
for i in range(start, wstart):
    line = wisdoms[i]
    # Remove whitespace from both sides
    line = line.strip()
    if line.startswith('- '):
        pre.append(Writer.item(line[2:]))
    elif line.startswith('---'):
        continue
    elif line.startswith('—'):
        pre.append(Writer.by(line[1:]))
    elif line.startswith('## '):
        pre.append(Writer.section(line[3:]))
    elif line == '':
        continue
    else:
        pre.append(Writer.text(line))

# Write pre
with open(PRE, 'w') as f: 
    f.write('\n'.join(pre))
print(f"Wrote to {PRE}")


out = []
for i in range(wstart, len(wisdoms)):
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
    # Most popular
    elif line.startswith('- '):
        out.append(Writer.wisdom(line[2:]))
    elif line.startswith('## '):
        out.append(Writer.section(line[3:]))
    else:
        continue

# Write out
with open(OUTPUT, 'w') as f:
    f.write('\n'.join(out))
print(f"Wrote to {OUTPUT}")
