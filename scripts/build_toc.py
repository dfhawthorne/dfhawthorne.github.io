#!/usr/bin/env python3
# ------------------------------------------------------------------------------
# Update TOC in a Jekyll formatted page
# ------------------------------------------------------------------------------

import argparse
from bs4 import BeautifulSoup
import re
import sys

# ------------------------------------------------------------------------------
# Parse arguments
# ------------------------------------------------------------------------------

parser = argparse.ArgumentParser(
        description='Update TOC in a Jekyll formatted page'
        )
parser.add_argument(
    '-v',
    '--verbose',
    action='store_true',
    help='Verbose output'
    )
parser.add_argument(
    '-r',
    '--replace',
    action='store_true',
    help='Replaces input file with converted one'
    )
parser.add_argument(
    '-l',
    '--log',
    default=sys.stdout,
    type=argparse.FileType('w'),
    help='the file where verbose output be written'
    )
parser.add_argument(
    'input_html_file_name',
    nargs=1,
    type=str,
    help='Input HTML file name'
    )
args = parser.parse_args()
if args.verbose:
    args.log.write(f"""Passed arguments:
    replace={args.replace}
    input_html_file_name={args.input_html_file_name}
""")

# ------------------------------------------------------------------------------
# Open and read HTML file. Exit if YAML header does not exists.
# ------------------------------------------------------------------------------

if args.verbose:
    args.log.write(f"Opening {args.input_html_file_name[0]} for conversion\n")
with open(args.input_html_file_name[0], 'r') as f:
    b = f.read()

if not b.startswith('---'):
    error_msg = f"{args.input_html_file_name[0]} has not been already converted"
    print(error_msg,file=sys.stderr)
    if args.verbose:
        args.log.write(error_msg + "\n")
    exit(1)

# ------------------------------------------------------------------------------
# Split file into header (YAML) and body (HTML)
# ------------------------------------------------------------------------------

b_eot       = '\n---\n'
eot_pos     = b.index(b_eot) + len(b_eot)
page_header = b[:eot_pos]
page_body   = b[eot_pos:]

if args.verbose:
    args.log.write(f"Page Header:\n{page_header}\nPage Body:\n{page_body}\n")

# ------------------------------------------------------------------------------
# Rebuild page header
# ------------------------------------------------------------------------------

new_page_header = f"---\n"
skip_lines      = False
regexp          = re.compile('^[ -]')
for line in page_header.splitlines():
    if line == "---": continue
    if line == "table-of-contents:":
        skip_lines = True
        continue
    if skip_lines:
        if regexp.match(line): continue
        skip_lines = False
    new_page_header += f"\n{line}"

# ------------------------------------------------------------------------------
# Find all HTML headers:
# - Add any missing ID attributes using the header text
# ------------------------------------------------------------------------------

soup = BeautifulSoup(page_body, 'html.parser')

trans_tbl = str.maketrans(" :.", "---")
toc_header = f"table-of-contents:\n"

prev_tag_level = 1
for tag in soup.find_all(re.compile('^h[1-6]')):
    if args.verbose:
        args.log.write(f"Heading: {tag.name}['id']='{tag.get('id')}' '{str(tag.string)}'\n")
    if tag.get('id') is None and tag.string is not None:
        tag['id'] = "TOC-" + tag.string.translate(trans_tbl)
        if args.verbose:
            args.log.write(f"Heading: {tag.name}['id'] updated to '{tag.get('id')}'\n")
    if tag.get('id') is not None:
        url = tag.get('id')[4:]
    else:
        url = ""
    curr_tag_level = int(tag.name[1:])
    if args.verbose:
        args.log.write(f"curr_tag_level: {curr_tag_level} prev_tag_level: {prev_tag_level}\n")
    if curr_tag_level > prev_tag_level and prev_tag_level > 1:
        indent      = ''.ljust((prev_tag_level-2)*2)
        toc_header += f"{indent}  toc-menu:\n"
    indent         = ''.ljust((curr_tag_level-2)*2)
    prev_tag_level = curr_tag_level
    toc_header    += f"{indent}- toc-url: '{url}'\n{indent}  toc-text: '{tag.string}'\n"

new_page_header += f"\n{toc_header}---\n"

if args.verbose:
    args.log.write(f"new_page_header: {new_page_header}\n")

# ------------------------------------------------------------------------------
# 
# ------------------------------------------------------------------------------

if args.replace:
    with open(args.input_html_file_name[0],'w') as f:
        f.write(new_page_header)
        f.write(str(soup))
else:
    print(new_page_header + str(soup))
