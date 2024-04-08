#!/usr/bin/env python3
# ------------------------------------------------------------------------------
# Fixes issue #84:
# - Adds YAML scroll bars for already converted pages
# - Removes HTML snippets for scroll bars
# ------------------------------------------------------------------------------

import argparse
import bs4
import os
import sys

# ------------------------------------------------------------------------------
# Parse arguments
# ------------------------------------------------------------------------------

parser = argparse.ArgumentParser(
        description='Fixes issue #84'
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

(page_header, sep, html_body) = b[3:].partition('---')
soup = bs4.BeautifulSoup(html_body, 'html.parser')
if args.verbose:
    args.log.write('Before scroll bar extraction:\n')
    args.log.write(f'page_header: ============================\n{page_header}\n')
    args.log.write( '=========================================\n')
    args.log.write(f'html_body: ==============================\n{html_body}\n')
    args.log.write( '=========================================\n')

if '\nscroll-bar:\n' in page_header:
    if args.verbose:
        args.log.write("*** Scroll bar already created ***\n")
    print('Scroll bar already created',file=sys.stderr)
    exit(1)

# ------------------------------------------------------------------------------
# Detect and Convert Journal Scroll Bar
# ------------------------------------------------------------------------------

first_block = True

def extract_journal_links(tag):
    assert tag is not None and type(tag) == bs4.element.Tag, \
        "Tag must be a BeautifulSoup Tag Element"

    scroll_bar  = ''

    if args.verbose:
        args.log.write(f">>> div=\n{str(tag)}\n>>>\n")
    if first_block:
        first_col = True
        for col in tag.find_all('div'):
            style = col.get('style')
            url   = col.find('a')
            if args.verbose:
                args.log.write(f"DIV: style='{style}'\nurl='{url}'\n")
            if url is None: continue
            if style is None: continue
            title = ' '.join([s for s in url.stripped_strings])
            if first_col:
                scroll_bar += "scroll-bar:\n"
                first_col = False
            if "left" in style:
                scroll_bar += f"  left-link:\n"
            elif "right" in style:
                scroll_bar += f"  right-link:\n"
            link = url.get('href')
            if args.verbose:
                args.log.write(f"A: link='{link}'\n")
            if link is None:
                if args.verbose:
                    args.log.write("missing URL for journal link\n")
                print("missing URL for journal link",file=sys.stderr)
                exit(1)
            elif link.endswith('.html'):
                pass
            else:
                link += '.html'
            scroll_bar += f"    url: {link}\n    title: '{title}'\n"
        first_block = False
    tag.decompose()

    assert scroll_bar is not None and type(scroll_bar) == str, \
        "scroll_bar must a string"
    return scroll_bar

req_attrs          = dict()
div_styles         = ["display:block;width:100%", "display:block", "display:grid"]
scroll_bar         = ''
for style in div_styles:
    req_attrs['style'] = style
    all_blocks         = soup.find_all('div', req_attrs)
    for tag in all_blocks:
        scroll_bar += extract_journal_links(tag)
    if scroll_bar != '': break

if args.verbose:
    args.log.write(f"scroll_bar: ====================================\n{scroll_bar}")
    args.log.write( "================================================\n")

if scroll_bar == '':
    if args.verbose:
        args.log.write("*** No scroll bar found ***\n")
    print('No scroll bar found',file=sys.stderr)
    exit(1)

page_header += scroll_bar
html_body    = str(soup)

if args.verbose:
    args.log.write('After scroll bar extraction:\n')
    args.log.write(f'page_header: ============================\n{page_header}\n')
    args.log.write( '=========================================\n')
    args.log.write(f'html_body: ==============================\n{html_body}\n')
    args.log.write( '=========================================\n')

if args.replace:
    with open(args.input_html_file_name[0], 'w') as f:
        f.write(f"---{page_header}---{html_body}")
else:
    print(f"---{page_header}---{html_body}")
