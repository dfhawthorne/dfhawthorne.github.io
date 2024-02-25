#!/usr/bin/env python3
# ------------------------------------------------------------------------------
# Convert a Classic Google Sites page to a Jekyll formatted one
# ------------------------------------------------------------------------------

import argparse
import bs4
import os
import re
import subprocess
import sys
from urllib.parse import urlparse

# ------------------------------------------------------------------------------
# Parse arguments
# ------------------------------------------------------------------------------

parser = argparse.ArgumentParser(
        description='Convert a Classic Google Sites page to a Jekyll formatted one'
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
    '-g',
    '--git-remove',
    action='store_true',
    help='Removed extra files that are no longer linked to'
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
    git-remove={args.git_remove}
    input_html_file_name={args.input_html_file_name}
""")

# ------------------------------------------------------------------------------
# Open and read HTML file. Exit if YAML header exists.
# ------------------------------------------------------------------------------

if args.verbose:
    args.log.write(f"Opening {args.input_html_file_name[0]} for conversion\n")
with open(args.input_html_file_name[0], 'r') as f:
    b = f.read()

if b.startswith('---'):
    print(f"{args.input_html_file_name[0]} has been already converted")
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
# Parse the input file as a HTML file
# Exit if the format is from the new Google Sites
# ------------------------------------------------------------------------------

soup = bs4.BeautifulSoup(b, 'html.parser')
doctype_items = [item for item in soup.contents if isinstance(item, bs4.Doctype)]
if args.verbose:
    args.log.write('DOCTYPE Entries found:\n')
    for item in doctype_items:
        args.log.write(item)
        args.log.write('\n')
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

if args.verbose: args.log.write(f"title='{title}'\n")

page_header += f'base-url: {page_rel_url}\n'
if args.verbose:
    args.log.write(f"base-url='{page_rel_url}'\n")

# ------------------------------------------------------------------------------
# Extract Breadcrumbs
# ------------------------------------------------------------------------------

breadcrumbs = list()
pattern = 'breadcrumbs = (.*);'

all_scripts = soup.find_all('script')
if all_scripts is not None:
    for script in all_scripts:
        if args.verbose: args.log.write(script.string + '\n')
        if match := re.search(pattern, script.string, re.IGNORECASE):
            breadcrumbs_var = match.group(1)
            if args.verbose: args.log.write(f"breadcrumbs_var={breadcrumbs_var}")
            breadcrumbs = eval(breadcrumbs_var.replace('false','False'))
            break
        else:
            if args.verbose: args.log.write(f"No breadcrumbs found\n")

if len(breadcrumbs) > 0:
    page_header += 'breadcrumbs:\n'
    for crumb in breadcrumbs:
        if args.verbose:
            args.log.write(f"Breadcrumb: '{crumb['title']}' '{crumb['path']}'\n")
        page_header += f"- title: {crumb['title']}\n"
        if crumb['path'].endswith('.html'):
            page_header += f"  url: {crumb['path'][1:]}\n"
        else:
            page_header += f"  url: {crumb['path'][1:]}.html\n"

# ------------------------------------------------------------------------------
# Table of Contents
# Only descend two (2) levels
# ------------------------------------------------------------------------------
    
all_toc = soup.find_all('div', 'goog-toc')
if all_toc is not None and len(all_toc) > 0:
    page_header += 'table-of-contents:\n'
    toc_root = all_toc[0].ol
    if toc_root is None:
        if args.verbose:
            args.log.write('TOC has no ordered list\n')
        toc_root = all_toc[0].ul
        if toc_root is None:
            if args.verbose:
                args.log.write('TOC has no unordered list\n')
            print('TOC has no list')
            exit(1)
    toc_children = [c for c in toc_root.children]
    if args.verbose:
        args.log.write(f'toc_children={str(toc_children)}\n')
    if len(toc_children) == 0:
        if args.verbose:
            args.log.write('No TOC children found\n')
    for toc_level_1 in toc_root.children:
        if args.verbose:
            args.log.write('toc_level_1: '+str(toc_level_1)+'\n')
        if toc_level_1.name == "li":
            page_header += f"- toc-url: {toc_level_1.a['href'].split('#TOC-')[1]}\n"
            page_header += f"  toc-text: "
            if toc_level_1.a.string is not None:
                page_header += f"{toc_level_1.a.string.strip()}\n"
            else:
                page_header += f"{toc_level_1.a.contents[2].string.strip()}\n"
        if toc_level_1.name == "ol":
            for toc_level_2 in toc_level_1.children:
                if args.verbose:
                    args.log.write('toc_level_2: '+str(toc_level_2)+'\n')
                if toc_level_2.name == "li":
                    page_header += f"  - toc-url: {toc_level_2.a['href'].split('#TOC-')[1]}\n"
                    page_header += f"  toc-text: "
                    if toc_level_2.a.string is not None:
                        page_header += f"{toc_level_2.a.string.strip()}\n"
                    else:
                        page_header += f"{toc_level_2.a.contents[2].string.strip()}\n"
    for toc_entry in all_toc:
        if args.verbose:
            args.log.write('TOC removed: '+str(toc_entry)+'\n')
        toc_entry.decompose()

# ------------------------------------------------------------------------------
# Remove empty headers of the type:
# <h3>
#  <a name="TOC-1">
#  </a>
#  <br/>
# </h3>
# ------------------------------------------------------------------------------

for h3 in soup.find_all('h3'):
    if args.verbose:
        args.log.write('h3: '+str(h3)+'\n')
    children = [child for child in h3.children]
    if len(children) == 0:
        if args.verbose:
            args.log.write('h3 removed\n')
        h3.decompose()
        continue
    if len(children) < 2: continue
    if children[0].name is not None and children[0].name == 'a':
        addr_children = [child for child in children[0].children]
        if len(addr_children) > 0: continue
    if len(children) == 2 and children[1].name == 'br':
        if args.verbose:
            args.log.write('h3 removed\n')
        h3.decompose()

# ------------------------------------------------------------------------------
# Auxiliary function to convert URL into one relative to the base of the Wiki
# (1) Remove prefixes of the form
#     - http://dfhawthorne.github.io/'
#     - https://dfhawthorne.github.io/'
#     - http://sites.google.com/view/yetanotherocm/'
#     - https://sites.google.com/view/yetanotherocm/'
# (2) Convert relative paths from the current page to the documents base
# (3) Leave other URLs unchanged
# (4) Change URL encoding: %2F to '?'
# ------------------------------------------------------------------------------

bigblog_redirects = {
    "id=121586": "home/10g-ocm/10g-system-builds/miscellaneous/first-vm-created.html",
    "id=121648": "home/10g-ocm/10g-system-builds/miscellaneous/vmware-clustering-problem.html",
    "id=200037": "home/10g-ocm/10g-system-builds/miscellaneous/cluvfy-crsinst.html"
    }

def normalise_url(href):
    assert href is not None, "href parameter expected"
    assert type(href) == str, "expected href to be passed as a string"

    href = href.replace('%2F','?')
    url_parts = urlparse(href)
    if args.verbose:
        args.log.write(f'URL_parts: {str(url_parts)}\n')
    if url_parts.scheme in ['http','https']:
        if args.verbose:
            args.log.write(f'URL is external: {url_parts.scheme}\n')
        if url_parts.netloc == 'dfhawthorne.github.io':
            if args.verbose:
                args.log.write(f'URL is from GITHub: {url_parts.path}\n')
            normalised_url = url_parts._replace(
                scheme='',
                netloc='').geturl()
        elif url_parts.netloc == 'sites.google.com':
            if args.verbose:
                args.log.write(f'URL is from Google Sites: {url_parts.path}\n')
            new_addr_path = os.path.relpath(
                            url_parts.path,
                            start='/view/yetanotherocm')
            if args.verbose:
                args.log.write(f'URL converted to: {new_addr_path}\n')
            normalised_url = url_parts._replace(
                scheme='',
                netloc='',
                path=new_addr_path).geturl()
        elif url_parts.netloc == 'yaocm.bigblog.com.au':
            if args.verbose:
                args.log.write(f'BigBlog URL found: \n')
            new_addr_path = bigblog_redirects.get(
                url_parts.query,
                "home/10g-ocm/missing-bigblog-links.html"
                )
            if args.verbose:
                args.log.write(f'URL converted to: {new_addr_path}\n')
            normalised_url = url_parts._replace(
                scheme='',
                netloc='',
                query='',
                path=new_addr_path).geturl()
        else:
            if args.verbose:
                args.log.write(f'External URL unchanged\n')
            return href
    else:
        old_url_path = url_parts.path.replace('../yetanotherocm/','')
        if args.verbose:
            args.log.write(f'Internal URL found: {old_url_path}\n')
        if old_url_path is not None and old_url_path != '':
            new_url_path = os.path.relpath(
                os.path.realpath(
                    old_url_path
                    ),
                    start=doc_base
                )
            if args.verbose:
                args.log.write(f'Internal URL changed to {new_url_path}\n')
            normalised_url = url_parts._replace(path=new_url_path).geturl()
        else:
            if args.verbose:
                args.log.write(f'Internal URL unchanged\n')
            normalised_url = href

    # Check the suffixes for internal URLs
    
    if normalised_url.endswith('.html'):
        return normalised_url
    elif normalised_url.endswith('.gif'):
        return normalised_url
    elif normalised_url.endswith('.png'):
        return normalised_url
    else:
        return normalised_url + '.html'

# ------------------------------------------------------------------------------
# Auxiliary function to determine if the file referenced by a URL needs to be
# removed. The following suffixes are considered for removal:
# - .png.html
# - .gif.html
# - attredirects=0
# ------------------------------------------------------------------------------

def need_to_remove_url(url):
    assert url is not None, 'URL is required'
    assert type(url) == str, 'URL is string'

    need_to_remove = False
    if href.endswith('.png.html'):
        need_to_remove = True
    elif href.endswith('.gif.html'):
        need_to_remove = True
    elif href.endswith('attredirects=0'):
        need_to_remove = True
    else:
        need_to_remove = False
    
    if args.verbose:
        args.log.write(f'URL: {str(url)} needs to be removed={str(need_to_remove)}\n')
    
    return need_to_remove

# ------------------------------------------------------------------------------
# Extracts contents
# (1) Change URL to relative to Wiki base
# (2) Remove links with imageanchor
# (3) Remove links to *%3Fattredirects=0 files
# (4) Remove links to *png.html pages
# (5) Remove links to *gif.html pages
# (6) Convert Sub-pages Plug-in to YAML menu entries, unless content follows
# ------------------------------------------------------------------------------

tags_to_be_deleted = list() # Tags to be deleted

try:
    content = soup.find("table",xmlns='http://www.w3.org/1999/xhtml').tbody.tr.td.div
except:
    print("Unable to find the table containing the main content")
    exit(1)

content_parts = [c.name for c in content.children if c.name is not None]
top_text      = list()
for tag in content.children:
    if tag.name == 'div': continue
    top_text.extend([s for s in tag.stripped_strings])
if args.verbose:
    args.log.write(f'Major tags in content are: {str(content_parts)}\n')
    args.log.write(f'Top level text in content are: {str(top_text)}\n')

sub_page = content.find('div', id='sites-toc-undefined')
if sub_page is not None and len(top_text) == 1:
    if args.verbose:
        args.log.write('Sub-page widget without following content found.\n')
    page_header += f"sub-pages-title: {sub_page.h4.string.strip()}\n"
    page_header += f"sub-pages:\n"
    for menu in sub_page.find_all('li'):
        entry = menu.a
        page_header += f"- title: {entry.string.strip()}\n"
        page_header += f"  url: {url_prefix}/{entry['href']}\n"
        if args.verbose:
            args.log.write(f"Menu item added: '{entry.string.strip()}', '{url_prefix}/{entry['href']}'\n")
    if args.verbose:
        args.log.write(f"Sub page removed: '{sub_page}'\n")
    sub_page.decompose()

for addr in content.find_all('a'):
    if addr.get('imageanchor') is not None:
        tags_to_be_deleted.append(addr)
    href         = addr.get('href')
    if href is None: continue
    # Regularise the URL to be relative to the documents base
    if args.verbose:
        args.log.write(f'A HREF Before: {str(href)}\n')
    addr['href'] = normalise_url(href)
    if args.verbose:
        args.log.write(f"A HREF After: {str(addr['href'])}\n")
    if need_to_remove_url(addr['href']):
        tags_to_be_deleted.append(addr)

for addr in content.find_all('img'):
    href = addr.get('src')
    # Regularise the URL to be relative to the documents base
    if href is None: continue
    if args.verbose:
        args.log.write(f'IMG SRC Before: {str(href)}\n')
    new_url_path = normalise_url(href)
    addr['src'] = new_url_path
    if args.verbose:
        args.log.write(f"IMG SRC After: {str(new_url_path)}\n")
    local_image_path = doc_base + '/' + new_url_path
    if local_image_path is not None and not os.path.exists(local_image_path):
        print(
            f"{args.input_html_file_name[0]}: Unable to locate image file, '{local_image_path}'"
            )
        if args.verbose:
            args.log.write(
                f"Unable to locate image file, '{local_image_path}'"
                )
    if need_to_remove_url(new_url_path):
        tags_to_be_deleted.append(addr)

if args.verbose:
    args.log.write('============> Start of Main Content (after rebasing of URLs) <================\n')
    args.log.write(f'{str(content)}\n')
    args.log.write('============> End of Main Content (after rebasing of URLs) <==================\n')

# ------------------------------------------------------------------------------
# Remove unnecessary tags
# ------------------------------------------------------------------------------

git_removals = list()
if args.verbose:
    args.log.write(f"Tags to be deleted: {str(tags_to_be_deleted)}\n")
for tag in tags_to_be_deleted:
    num_children = len([child for child in tag.children if child.name is not None])
    num_strings  = len([child for child in tag.stripped_strings])
    child_names  = [child.name for child in tag.children]
    if args.verbose:
        args.log.write(f"Tag found: {str(tag)}\n")
        args.log.write(f"num_children={num_children}\n")
        args.log.write(f"num_strings={num_strings}\n")
        args.log.write(f"child_names={str(child_names)}\n")
    if tag.name == "a":
        href = tag.get('href')
        if href is not None:
            file_name = doc_base + '/' + href.replace('%3F','?')
            if file_name not in git_removals and os.path.exists(file_name):
                git_removals.append(file_name)
    elif tag.name == "img":
        src = tag.get('src')
        if src is not None:
            file_name = doc_base + '/' + src.replace('%3F','?')
            if file_name not in git_removals and os.path.exists(file_name):
                git_removals.append(file_name)
    if num_children == 0 and num_strings == 0:
        if args.verbose:
            args.log.write(f"Removed empty tag: {str(tag)}\n")
        tag.decompose()
    else:
        if args.verbose:
            args.log.write(f"Unwrapped tag: {str(tag)}\n")
        tag.unwrap()

if args.verbose:
    args.log.write('============> Start of Main Content (after removal of unneeded tags) <================\n')
    args.log.write(f'{str(content)}\n')
    args.log.write('============> End of Main Content (after removal of unneeded tags) <==================\n')

# ------------------------------------------------------------------------------
# Remove Empty DIV tags in up to four (4) levels
# ------------------------------------------------------------------------------
                
for retries in range(4):
    all_div_tags = content.find_all('div')
    for tag in all_div_tags:
        num_children = len([child for child in tag.children if child.name is not None])
        num_strings  = len([child for child in tag.stripped_strings])
        child_names  = [child.name for child in tag.children  if child.name is not None]
        if args.verbose:
            args.log.write(f"DIV tag found: {str(tag)}\n")
            args.log.write(f"num_children={num_children}\n")
            args.log.write(f"num_strings={num_strings}\n")
            args.log.write(f"child_names={str(child_names)}\n")
        if num_children == 0 and num_strings == 0:
            if args.verbose:
                args.log.write(f"Removed empty DIV tag: {str(tag)}\n")
            tag.decompose()
        elif num_children == 1 and num_strings == 0:
            if child_names[0] == 'br':
                if args.verbose:
                    args.log.write(f"Removed DIV with solitary BR tag: {str(tag)}\n")
                tag.decompose()

if args.verbose:
    args.log.write('============> Start of Main Content (after removal of empty DIV tags) <================\n')
    args.log.write(f'{str(content)}\n')
    args.log.write('============> End of Main Content (after removal of empty DIV tags) <==================\n')

# ------------------------------------------------------------------------------
# Detect and Convert Journal Scroll Bar
# ------------------------------------------------------------------------------

req_attrs  = dict()
req_attrs['border']      = "0"
req_attrs['cellspacing'] = "10"
req_attrs['width']       = "100%"
all_tables = soup.find_all('table',attrs=req_attrs)
first_table = True
for tag in all_tables:
    if args.verbose:
        args.log.write(f">>> table=\n{str(tag)}\n>>>")
    if first_table:
        first_col = True
        for col in tag.find_all('td'):
            align = col.get('align')
            url   = col.find('a')
            if url is None: continue
            title = ' '.join([s for s in url.stripped_strings])
            if first_col:
                page_header += "scroll-bar:\n"
                first_col = False
            if align is None or align == "left":
                page_header += f"  left-link:\n"
            elif align == "right":
                page_header += f"  right-link:\n"
            link = url.get('href')
            if link is None:
                print("missing URL for journal link")
            elif link.endswith('.html'):
                pass
            else:
                link += '.html'
            page_header += f"    url: {link}\n    title: {title}\n"
        first_table = False
    tag.decompose()

if args.verbose:
    args.log.write('============> Start of Main Content (after Journal Scroll Bar) <================\n')
    args.log.write(f'{str(content)}\n')
    args.log.write('============> End of Main Content (after Journal Scroll Bar) <==================\n')

# ------------------------------------------------------------------------------
# Print out YAML data
# ------------------------------------------------------------------------------

page_header += '---\n'
if args.replace:
    with open(os.path.basename(args.input_html_file_name[0]),'w') as f:
        f.write(page_header)
        f.write(content.prettify())
else:
    print(page_header)
    print(content.prettify())

# ------------------------------------------------------------------------------
# GIT Removals
# ------------------------------------------------------------------------------

cmd = ['git', 'rm']
cmd.extend(git_removals)
cmd_str = ' '.join(cmd)

if args.verbose:
    args.log.write(f"GIT command: {str(cmd_str)}\n")
if args.git_remove and len(git_removals) > 0:
    p = subprocess.run(cmd, capture_output=True)
    if args.verbose:
        args.log.write(f"GIT STDOUT:\n{p.stdout}\n\nGIT STDERR:\n{p.stderr}")
