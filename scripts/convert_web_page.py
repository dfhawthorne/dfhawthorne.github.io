#!/usr/bin/env python3
# ------------------------------------------------------------------------------
# Convert a Classic Google Sites page to a Jekyll formatted one
# ------------------------------------------------------------------------------

import argparse
import bs4
import os
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

url_prefix = os.path.dirname(args.input_html_file_name[0])
if args.verbose: print(f"url_prefix='{url_prefix}'")

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
    page_header += f'title: {title}\n'

if args.verbose: print(f"title='{title}'\n")

page_header += f'base-url: {args.input_html_file_name[0]}\n'
if args.verbose: print(f"base-url='{args.input_html_file_name[0]}'")

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

if len(breadcrumbs) > 0: page_header += 'breadcrumbs:\n'
for crumb in breadcrumbs:
    page_header += f"- title: {crumb['title']}\n"
    if crumb['path'].endswith('.html'):
        page_header += f"  url: {crumb['path']}\n"
    else:
        page_header += f"  url: {crumb['path']}.html\n"

# ------------------------------------------------------------------------------
# Table of Contents
# Only descend two (2) levels
# ------------------------------------------------------------------------------
    
all_toc = soup.find_all('div', 'goog-toc')
if all_toc is not None and len(all_toc) > 0:
    page_header += 'table-of-contents:\n'
    toc_root = all_toc[0].ol
    for toc_level_1 in toc_root.children:
        if args.verbose: print(toc_level_1)
        if toc_level_1.name == "li":
            page_header += f"- toc-url: {toc_level_1.a['href'].split('#TOC-')[1]}\n"
            page_header += f"  toc-text: "
            if toc_level_1.a.string is not None:
                page_header += f"{toc_level_1.a.string.strip()}\n"
            else:
                page_header += f"{toc_level_1.a.contents[2].string.strip()}\n"
        if toc_level_1.name == "ol":
            for toc_level_2 in toc_level_1.children:
                if args.verbose: print(toc_level_2)
                if toc_level_2.name == "li":
                    page_header += f"  - toc-url: {toc_level_2.a['href'].split('#TOC-')[1]}\n"
                    page_header += f"  toc-text: "
                    if toc_level_2.a.string is not None:
                        page_header += f"{toc_level_2.a.string.strip()}\n"
                    else:
                        page_header += f"{toc_level_2.a.contents[2].string.strip()}\n"

# ------------------------------------------------------------------------------
# Sub-pages
# ------------------------------------------------------------------------------

all_sub_pages = soup.find_all('div', id='sites-toc-undefined')
if all_sub_pages is not None and len(all_sub_pages) > 0:
    sub_page = all_sub_pages[0]
    page_header += f"sub-pages-title: {sub_page.h4.string.strip()}\nsub-pages:\n"
    for menu in sub_page.find_all('li'):
        entry = menu.a
        page_header += f"- title: {entry.string.strip()}\n  url: {url_prefix}/{entry['href']}\n"

# ------------------------------------------------------------------------------
# Extracts contents
# ------------------------------------------------------------------------------

all_content = soup.find_all("td","sites-tile-name-content-1")

# ------------------------------------------------------------------------------
# Print out YAML data
# ------------------------------------------------------------------------------

page_header += '---\n'
if args.replace:
    with open(args.input_html_file_name[0],'w') as f:
        f.write(page_header)
        for content in all_content:
            f.write(content.div.prettify())
else:
    print(page_header)
    for content in all_content:
        print(content.div.prettify())
