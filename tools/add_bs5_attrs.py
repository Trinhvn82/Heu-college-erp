#!/usr/bin/env python3
"""
Add data-bs-* duplicates next to data-* attributes in template files under sms/templates.
This is safe (adds duplicates, doesn't remove old attrs) and idempotent.
"""
import re
from pathlib import Path

root = Path(r"d:/Coding/Python-Code/College-ERP-v1.1/sms/templates")
if not root.exists():
    print("sms/templates not found at expected path:", root)
    raise SystemExit(1)

patterns = {
    'toggle': r'data-toggle\s*=\s*("[^"]+"|\'[^\']+\')',
    'target': r'data-target\s*=\s*("[^"]+"|\'[^\']+\')',
    'dismiss': r'data-dismiss\s*=\s*("[^"]+"|\'[^\']+\')',
    'slide': r'data-slide\s*=\s*("[^"]+"|\'[^\']+\')',
    'ride': r'data-ride\s*=\s*("[^"]+"|\'[^\']+\')',
    'slide-to': r'data-slide-to\s*=\s*("[^"]+"|\'[^\']+\')',
}

# compile regexes
regexes = {k: re.compile(v) for k, v in patterns.items()}

modified_files = []
for path in root.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    orig = text
    offset = 0
    # We'll process each tag by searching for the attributes and inserting duplicates when missing
    for k, regex in regexes.items():
        # iterate matches using finditer on current text
        new_text = []
        last_idx = 0
        for m in regex.finditer(text):
            start, end = m.span()
            # find tag end '>' after match start
            tag_end = text.find('>', end)
            if tag_end == -1:
                tag_end = end
            tag_fragment = text[end:tag_end]
            bs_attr = f'data-bs-{k.replace("-","-")}'
            # if bs attribute already exists in this tag, skip
            if bs_attr in tag_fragment or f'{bs_attr}=' in tag_fragment:
                continue
            # extract the attribute value
            val = m.group(1)
            # build insertion string (preceded by a space)
            insertion = f' {bs_attr}={val}'
            # insert right after the matched attribute
            text = text[:end] + insertion + text[end:]
        # continue to next pattern
    if text != orig:
        # backup original
        bak = path.with_suffix(path.suffix + '.bak')
        bak.write_text(orig, encoding='utf-8')
        path.write_text(text, encoding='utf-8')
        modified_files.append(str(path))

print('Modified files:')
for f in modified_files:
    print(f)

if not modified_files:
    print('No template files needed changes.')
