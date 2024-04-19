#!/usr/bin/env python3
# ------------------------------------------------------------------------------
# Fixes issue #85:
# - Removes leading numbers from TOC 
# ------------------------------------------------------------------------------

import argparse
import bs4
import os
import sys

# ------------------------------------------------------------------------------
# Parse arguments
# ------------------------------------------------------------------------------

parser = argparse.ArgumentParser(
        description='Fixes issue #85'
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
    help='the file where verbose output will be written'
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
# Open and read HTML file. Exit if YAML header does not exist.
# ------------------------------------------------------------------------------

if args.verbose:
    args.log.write(f"Opening {args.input_html_file_name[0]} for conversion\n")
with open(args.input_html_file_name[0], 'r') as f:
    b = f.read()

if not b.startswith('---'):
    error_msg = f"{args.input_html_file_name[0]} has not been converted"
    print(error_msg,file=sys.stderr)
    if args.verbose:
        args.log.write(error_msg + "\n")
    exit(1)

# ------------------------------------------------------------------------------
# Locate the input file within:
# (1) documents base which is a sibling of the scripts directory (doc_base)
# (2) relative directory to where the script is invoked from (page_rel_url)
# (3) the whole file system (curr_dir)
#
# Change the working directory to where the input file is located. This is
# necessary as Classic Google Sites pages use page-relative URLs.
# ------------------------------------------------------------------------------

doc_base = os.path.dirname(
    os.path.dirname(
        os.path.realpath(
            sys.argv[0]
            )
        )
    ) + '/docs' # Get ../../docs
page_rel_url = os.path.relpath(
    os.path.realpath(
        args.input_html_file_name[0]
        ),
        start=doc_base
    )
curr_dir = os.path.dirname(os.path.realpath(args.input_html_file_name[0]))
os.chdir(curr_dir)
url_prefix = os.path.relpath(curr_dir,start=doc_base)
if args.verbose:
    args.log.write(f"doc_base='{doc_base}'\n")
    args.log.write(f"curr_dir='{curr_dir}\n")
    args.log.write(f"url_prefix='{url_prefix}'\n")

# ------------------------------------------------------------------------------
# Split the input file into a YAML header and a HTML body
# ------------------------------------------------------------------------------

(page_header, sep, content) = b[3:].partition('---')
soup = bs4.BeautifulSoup(content, 'html.parser')
if args.verbose:
    args.log.write('Before scroll bar extraction:\n')
    args.log.write(f'page_header: ============================\n{page_header}\n')
    args.log.write( '=========================================\n')
    args.log.write(f'content: ==============================\n{content}\n')
    args.log.write( '=========================================\n')

if '\ntable-of-contents:\n' in page_header:
    if args.verbose:
        args.log.write("*** TOC already created ***\n")
    print('TOC already created',file=sys.stderr)
    exit(1)

# ------------------------------------------------------------------------------
# Table of Contents
# Do not convert TOC if either:
# (1) There is displayable text preceding the TOC entries
# (2) There are multiple TOCs found
# ------------------------------------------------------------------------------

def extract_toc_level(toc_root, toc_level):
    if toc_root is None: return ''
    assert type(toc_level) == int and toc_level > 0, 'toc_level must be an integer > 0'

    if args.verbose:
        args.log.write(f'Extracting TOC at level {toc_level}\n')

    toc_children = [c for c in toc_root.children if c.name is not None]

    if args.verbose:
        args.log.write(f'len(toc_children)={len(toc_children)}\n')
        args.log.write(f'toc_children={str(toc_children)}\n')

    if len(toc_children) == 0:
        if args.verbose:
            args.log.write(f'No TOC children found at level {toc_level}\n')

    result = ''
    toc_indent = ''.ljust(2*(toc_level-1))
    if toc_level > 1:
        result += f'{toc_indent}toc-menu:\n'

    for toc_item in toc_children:
        if args.verbose:
            args.log.write(f'toc_item: {str(toc_item)}\n')
        if toc_item.name != "li": continue
        toc_url = toc_item.a['href'].split('#TOC-')[1]
        if toc_item.a.string is not None:
            toc_text = toc_item.a.string.strip()
        else:
            toc_text = toc_item.a.contents[2].string.strip()
        if args.verbose:
            args.log.write(f'  toc_url (L{toc_level}): {toc_url}\n')
            args.log.write(f'  toc_text (L{toc_level}): {toc_text}\n')
        result += f"{toc_indent}- toc-url: '{toc_url}'\n"
        result += f"{toc_indent}  toc-text: '{toc_text}'\n"
        result += extract_toc_level(toc_item.ol, toc_level+1)

    assert type(result) == str and len(result) > 0, 'result must be a non-zero string'
    return result

toc_widget = soup.find('div','sites-embed-toc-maxdepth-6')
if toc_widget is not None:
    toc_header  = 'table-of-contents:\n'
    toc_header += extract_toc_level(toc_widget.ol, 1)
    if args.verbose:
        args.log.write('TOC removed: '+str(toc_widget)+'\n')
    toc_widget.decompose()
else:
    toc_header  = ''

if args.verbose:
    args.log.write('============> Start of Main Content (after removal of TOC) <================\n')
    args.log.write(f'{str(content)}\n')
    args.log.write('============> End of Main Content (after removal of TOC) <==================\n')

page_header += toc_header
content    = str(soup)

if args.verbose:
    args.log.write('After TOC correction:\n')
    args.log.write(f'page_header: ============================\n{page_header}\n')
    args.log.write( '=========================================\n')
    args.log.write(f'content: ==============================\n{content}\n')
    args.log.write( '=========================================\n')

if args.replace:
    with open(args.input_html_file_name[0], 'w') as f:
        f.write(f"---{page_header}---{content}")
else:
    print(f"---{page_header}---{content}")
