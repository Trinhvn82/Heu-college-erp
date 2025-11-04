#!/usr/bin/env python3
"""
Repair malformed data-bs-* insertions where a bs-attribute was inserted inside another attribute's quoted value.
For each tag in templates, if any quoted attribute value contains a substring matching a bs-attribute (e.g. ' data-bs-dismiss="modal"'),
this script will remove that substring from the attribute value and append the bs-attribute to the tag (if not already present elsewhere in the tag).
Creates a .bak backup for each changed file.
"""
import re
from pathlib import Path

root = Path(r"d:/Coding/Python-Code/College-ERP-v1.1/sms/templates")
if not root.exists():
    print('sms/templates not found:', root)
    raise SystemExit(1)

tag_re = re.compile(r'<[^>]+>', flags=re.IGNORECASE)
# bs-attr pattern inside quotes
inside_bs_re = re.compile(r'\s+(data-bs-[a-z0-9-]+\s*=\s*("[^"]*"|\'[^\']*\'))', flags=re.IGNORECASE)

modified = []
for path in root.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    new_text = []
    last = 0
    changed = False
    for m in tag_re.finditer(text):
        tag_start, tag_end = m.span()
        tag = m.group(0)
        new_tag = tag
        # find all quoted attribute values
        # regex to find attributes (name="value" or name='value')
        attr_re = re.compile(r'([a-zA-Z0-9_-]+)\s*=\s*("[^"]*"|\'[^\']*\')')
        attrs = list(attr_re.finditer(tag))
        bs_to_append = []
        for am in attrs:
            attr_name = am.group(1)
            attr_val = am.group(2)
            # check if attr_val contains bs-attr snippet
            for bsmatch in inside_bs_re.finditer(attr_val):
                bs_full = bsmatch.group(1).strip()  # e.g. data-bs-dismiss="modal"
                # remove this substring from attr_val
                clean_val = attr_val.replace(bsmatch.group(0), '')
                # ensure quotes remain balanced
                # remove any double spaces created
                clean_val = re.sub(r'\s{2,}', ' ', clean_val)
                # replace original attr_val in tag
                # need to escape for replace
                new_tag = new_tag.replace(attr_val, clean_val)
                changed = True
                # if bs attribute not already in tag, schedule to append
                if bs_full not in new_tag:
                    bs_to_append.append(bs_full)
        if bs_to_append:
            # append bs attrs before closing >, but after any trailing / if self-closing
            if new_tag.endswith('/>'):
                new_tag = new_tag[:-2] + ' ' + ' '.join(bs_to_append) + ' />'
            else:
                new_tag = new_tag[:-1] + ' ' + ' '.join(bs_to_append) + '>'
        new_text.append(text[last:tag_start])
        new_text.append(new_tag)
        last = tag_end
    new_text.append(text[last:])
    new_content = ''.join(new_text)
    if changed and new_content != text:
        bak = path.with_suffix(path.suffix + '.bak2')
        bak.write_text(text, encoding='utf-8')
        path.write_text(new_content, encoding='utf-8')
        modified.append(str(path))

print('Repaired files:')
for p in modified:
    print(p)
if not modified:
    print('No repairs needed.')
