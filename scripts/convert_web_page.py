#!/usr/bin/env python3
# ------------------------------------------------------------------------------
# Convert a Classic Google Sites page to a Jekyll formatted one
# ------------------------------------------------------------------------------

import argparse
import bs4
import re

# ------------------------------------------------------------------------------
# Parse arguments
# ------------------------------------------------------------------------------

parser = argparse.ArgumentParser(
        description='Convert a Classic Google Sites page to a Jekyll formatted one'
        )
parser.add_argument('-v','--verbose',action='store_true',help='Verbose output')
parser.add_argument('-r','--replace',action='store_true',help='Replaces input file with converted one')
parser.add_argument(
    'input_html_file_name',
    nargs=1,
    type=str,
    help='Input HTML file name'
    )
args = parser.parse_args()
if args.verbose:
    print(f"""Passed arguments:
    replace={args.replace}
    input_html_file_name={args.input_html_file_name}""")

# ------------------------------------------------------------------------------
# Open and read HTML file. Exit if YAML header exists.
# ------------------------------------------------------------------------------

if args.verbose: print(f"Opening {args.input_html_file_name[0]} for conversion")
with open(args.input_html_file_name[0], 'r') as f:
    b = f.read()

if b.startswith('---'):
    print(f"{args.input_html_file_name[0]} has been already converted")
    exit(1)

soup = bs4.BeautifulSoup(b, 'html.parser')
doctype_items = [item for item in soup.contents if isinstance(item, bs4.Doctype)]
if args.verbose:
    print('DOCTYPE Entries found:')
    for item in doctype_items:
        print(item)
if len(doctype_items) > 0 and doctype_items[0] == 'html':
    print(f"{args.input_html_file_name[0]} is a New Google Sites page")
    exit(1)

page_header = "---\nlayout: default\n"

# ------------------------------------------------------------------------------
# Extract the title
# ------------------------------------------------------------------------------

all_titles = soup.find_all('title')
if all_titles is not None and len(all_titles) > 0:
    title = all_titles[0].text.strip()
else:
    all_headers = soup.find_all('h1')
    if all_headers is not None and len(all_headers) > 0:
        title = all_headers[0].text.strip()
    else:
        all_span_titles = soup.find_all('span', id="sites-page-title")
        if all_span_titles is not None and len(all_span_titles) > 0:
            title = all_span_titles[0].text.strip()
        else:
            title = None

if title is not None:
    title = title.replace(' - Yet Another OCM','')
    page_header += 'title: ' + title + '\n'

if args.verbose: print(f"title='{title}'")

# ------------------------------------------------------------------------------
# Extract Breadcrumbs
# ------------------------------------------------------------------------------

breadcrumbs = list()
pattern = 'breadcrumbs = (.*);'

all_scripts = soup.find_all('script')
if all_scripts is not None:
    for script in all_scripts:
        if args.verbose: print(script.string)
        if match := re.search(pattern, script.string, re.IGNORECASE):
            breadcrumbs_var = match.group(1)
            if args.verbose: print(f"breadcrumbs_var={breadcrumbs_var}")
            breadcrumbs = eval(breadcrumbs_var.replace('false','False'))
            break
        else:
            if args.verbose: print(f"No breadcrumbs found")

page_header += 'breadcrumbs:\n'
for crumb in breadcrumbs:
    page_header += f"- title: {crumb['title']}\n  url: {crumb['path']}\n"

# ------------------------------------------------------------------------------
# Table of Contents
# Only descend two (2) levels
# ------------------------------------------------------------------------------
    
all_toc = soup.find_all('div', 'goog-toc')
if all_toc is not None and len(all_toc) > 0:
    page_header += 'table-of-contents:'
    toc_root = all_toc[0].ol
    for toc_level_1 in toc_root.children:
        if toc_level_1.name == "li":
            page_header += f"- toc-url: {toc_level_1.a['href']}\n"
            page_header += f"  toc-text: {toc_level_1.a.string.strip()}"
        if toc_level_1.name == "ol":
            for toc_level_2 in toc_level_1.children:
                if toc_level_2.name == "li":
                    page_header += f"  - toc-url: {toc_level_2.a['href']}\n"
                    page_header += f"    toc-text: {toc_level_2.a.string.strip()}"

# ------------------------------------------------------------------------------
# Sub-pages
# ------------------------------------------------------------------------------

all_sub_pages = soup.find_all('div', id='sites-toc-undefined')
if all_sub_pages is not None:
    sub_page = all_sub_pages[0]
    page_header += f"sub-pages-title: {sub_page.h4.string.strip()}\nsub-pages:\n"
    for menu in sub_page.find_all('li'):
        entry = menu.a
        page_header += f"- title: {entry.string.strip()}\n  url: {entry['href']}\n"

# ------------------------------------------------------------------------------
# Extracts contents
# ------------------------------------------------------------------------------

all_content = soup.find_all("div","sites-tile-name-content-1")

# ------------------------------------------------------------------------------
# Print out YAML data
# ------------------------------------------------------------------------------

page_header += '---\n'
print(page_header)
if all_content is not None and len(all_content) > 0:
    print(all_content[0].prettify())