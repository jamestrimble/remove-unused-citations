import sys

with open(sys.argv[1], "r") as f:
    s = f.read()

with open(sys.argv[2], "r") as f:
    lines = [l.strip().split() for l in f.readlines()]
    unused_citations = [l[1] for l in lines if l and l[0]=="-"]

braced_strings = []
brace_depth = 0
in_braces = False
for c in s:
    if c == "{":
        brace_depth += 1
        if brace_depth == 2:
            in_braces = True
            braced_string = ""
    elif c == "}":
        brace_depth -= 1
        if brace_depth == 1:
            braced_strings.append(braced_string)
    elif in_braces:
        braced_string += c

brace_depth = 0
in_name = False
name = None
citation = None
for c in s:
    if c == "@" and brace_depth == 0:
        if citation and (name not in unused_citations or name in braced_strings):
            sys.stdout.write(citation)
        citation = ""
    elif c == "{":
        brace_depth += 1
        if brace_depth == 1:
            in_name = True
            name = ""
    elif c == "}":
        brace_depth -= 1
    elif in_name:
        if c == ",":
            in_name = False
        else:
            name += c
    if c != "\r":
        citation += c

if citation and (name not in unused_citations or name in braced_strings):
    sys.stdout.write(citation)
