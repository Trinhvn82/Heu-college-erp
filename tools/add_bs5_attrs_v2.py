#!/usr/bin/env python3
"""
Safer BS5 attribute inserter.
For each HTML file under sms/templates, performs non-overlapping replacements:
- data-toggle -> data-toggle + data-bs-toggle (if data-bs-toggle not present in the same tag)
- data-target -> data-target + data-bs-target
- data-dismiss -> data-dismiss + data-bs-dismiss
- data-slide -> data-slide + data-bs-slide
- data-ride -> data-ride + data-bs-ride
- data-slide-to -> data-slide-to + data-bs-slide-to
This version operates per-tag and uses a callback to avoid inserting inside other attributes.
Creates a .bak backup for each changed file.
"""
import re
from pathlib import Path

root = Path(r"d:/Coding/Python-Code/College-ERP-v1.1/sms/templates")
if not root.exists():
    print('sms/templates not found:', root)
    raise SystemExit(1)

# Patterns we want to duplicate
attrs = [
    ('data-toggle', 'data-bs-toggle'),
    ('data-target', 'data-bs-target'),
    ('data-dismiss', 'data-bs-dismiss'),
    ('data-slide', 'data-bs-slide'),
    ('data-ride', 'data-bs-ride'),
    ('data-slide-to', 'data-bs-slide-to'),
]

# Regex to find a tag <...>
tag_re = re.compile(r'<[^>]+>', flags=re.IGNORECASE)

# For each attribute, build a regex to find attr=VALUE (with single or double quotes)
attr_regexes = [(a, b, re.compile(r'(' + re.escape(a) + r')\s*=\s*("[^"]*"|\'[^\']*\')', flags=re.IGNORECASE)) for a, b in attrs]

modified = []
for path in root.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    new_text = []
    last = 0
    changed = False
    for m in tag_re.finditer(text):
        tag_start, tag_end = m.span()
        tag = m.group(0)
        orig_tag = tag
        # For each attr pattern, decide whether to insert the bs-attr
        for a, b, are in attr_regexes:
            # if bs attr already present, skip
            if b in tag:
                continue
            # find a in tag
            am = are.search(tag)
            if am:
                # ensure we are not inside another attribute value (we are within tag so OK)
                val = am.group(2)
                # insert after the matched attribute (i.e., after am.end())
                insert_pos = am.end()
                # construct insertion with a single space before
                insertion = f' {b}={val}'
                tag = tag[:insert_pos] + insertion + tag[insert_pos:]
                changed = True
        new_text.append(text[last:tag_start])
        new_text.append(tag)
        last = tag_end
    new_text.append(text[last:])
    new_content = ''.join(new_text)
    if changed and new_content != text:
        bak = path.with_suffix(path.suffix + '.bak')
        bak.write_text(text, encoding='utf-8')
        path.write_text(new_content, encoding='utf-8')
        modified.append(str(path))

print('Modified files (v2):')
for p in modified:
    print(p)
if not modified:
    print('No template files changed by v2.')
