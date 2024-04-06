#!/usr/bin/env python3
# ------------------------------------------------------------------------------
# Convert a Classic Google Sites page to a Jekyll formatted one
# ------------------------------------------------------------------------------

import argparse
import bs4
import os
import re
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
    error_msg = f"{args.input_html_file_name[0]} has been already converted"
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
    error_msg = f"{args.input_html_file_name[0]} is a New Google Sites page"
    print(error_msg,file=sys.stderr)
    if args.verbose:
        args.log.write(error_msg + '\n')
    exit(1)

page_header = "---\nlayout: default\n"

# ------------------------------------------------------------------------------
# Find any auxiliary files:
# - If there are auxiliary files, then there a sibling directory with the name
#   with the '.html' suffix stripped.
# ------------------------------------------------------------------------------

(auxiliary_dir, suffix) = os.path.splitext(
        curr_dir + os.path.sep + os.path.basename(args.input_html_file_name[0])
    )
if args.verbose:
    args.log.write(f"auxiliary_dir='{auxiliary_dir}'\n")
if os.path.isdir(auxiliary_dir):
    auxiliary_files = [f 
                       for f in os.listdir(auxiliary_dir)
                         if os.path.isfile(auxiliary_dir + os.path.sep + f)]
    if args.verbose:
        args.log.write(f"auxiliary files found='{str(auxiliary_files)}'\n")
else:
    auxiliary_files = list()
    if args.verbose:
        args.log.write(f"NO auxiliary files were found\n")

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
    page_header += f"title: '{title}'\n"

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
        page_header += f"- title: '{crumb['title']}'\n"
        crumb_url = crumb['path'][1:].replace('/12-ocm','/12c-ocm')
        if crumb_url.endswith('.html'):
            page_header += f"  url: {crumb_url}\n"
        else:
            page_header += f"  url: {crumb_url}.html\n"

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

    href = href.replace('%3F','?').replace('/12-ocm/','/12c-ocm/')
    url_parts = urlparse(href)
    if args.verbose:
        args.log.write(f'URL_parts: {str(url_parts)}\n')
    if url_parts.scheme == 'javascript':
        error_msg = f'javascript link found: {str(href)}'
        print(error_msg,file=sys.stderr)
        if args.verbose:
            args.log.write(error_msg + '\n')
        exit(1)
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
    elif normalised_url.endswith('attredirects=0'):
        return normalised_url
    elif '#' in normalised_url:
        return normalised_url
    else:
        full_name_path = doc_base + os.path.sep + normalised_url
        if os.path.isfile(full_name_path):
            if args.verbose:
                args.log.write(f"URL: file '{normalised_url}' exists\n")
            return normalised_url
        elif os.path.isfile(full_name_path + '.html'):
            if args.verbose:
                args.log.write(f"URL: file '{normalised_url}.html' exists\n")
            return normalised_url + '.html'
        else:
            if args.verbose:
                args.log.write(f"URL: Neither '{normalised_url}' or '{normalised_url}.html' exist as a file\n")
            print(f"URL: Neither '{normalised_url}' or '{normalised_url}.html' exist\n", file=sys.stderr)
            exit(1)

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
    if url.endswith('.png.html'):
        need_to_remove = True
    elif url.endswith('.gif.html'):
        need_to_remove = True
    elif url.endswith('attredirects=0'):
        need_to_remove = True
    else:
        need_to_remove = False
    
    if args.verbose:
        args.log.write(f'URL: {str(url)} needs to be removed={str(need_to_remove)}\n')
    
    assert type(need_to_remove) == bool, "need_to_remove must be Boolean"

    return need_to_remove

# ------------------------------------------------------------------------------
# Extract and analyse the main content.
#
# In Classic Google Sites, the main content is in the first division of the
# first cell of the first row of the table with an XMLNS attribute.
#
# There are four (4) main parts of the main content to be identified:
# (1) Prologue (displayable text at start of main content)
# (2) TOC (Table of Contents) - optional
# (3) Sub-pages Menu - optional
# (4) Epilogue (displayable text after optional elements)
# ------------------------------------------------------------------------------

tags_to_be_deleted = list() # Tags to be deleted

try:
    content = soup.find("table",xmlns='http://www.w3.org/1999/xhtml').tbody.tr.td.div
except:
    error_msg = "Unable to find the table containing the main content"
    print(error_msg,file=sys.stderr)
    if args.verbose:
        args.log.write(error_msg + '\n')
    exit(1)

if args.verbose:
    args.log.write('============> Start of Main Content (initial) <================\n')
    args.log.write(f'{str(content)}\n')
    args.log.write('============> End of Main Content (initial) <==================\n')

sub_pages_widget_found    = False
antecedent_content_found  = False
subsequent_content_found  = False
any_content_found         = False
toc_widget_found          = False
multiple_toc_widget_found = False

sub_page                  = None
toc_widget                = None

if content is not None and content.children is not None:
    for tag in content.children:
        if args.verbose:
            if tag.name is None:
                args.log.write(f"tag: {str(tag)}\n")
            else:
                args.log.write(f"tag: name={tag.name}, id={tag.attrs.get('id')}\n")
        if tag.name == 'div':
            possible_sub_page   = tag.find('div',{'id': 'sites-toc-undefined'})
            possible_toc_widget = tag.find('div','sites-embed-toc-maxdepth-6')
            if possible_sub_page is not None and possible_toc_widget is not None:
                error_msg = 'Overlapping sub page and TOC widgets'
                print(error_msg,file=sys.stderr)
                if args.verbose:
                    args.log.write(error_msg + '\n')
                exit(1)
            if possible_sub_page is not None:
                if sub_pages_widget_found:
                    error_msg = 'Duplicate sub-page widget found'
                    print(error_msg,file=sys.stderr)
                    if args.verbose:
                        args.log.write(error_msg + '\n')
                    exit(1)
                else:
                    sub_pages_widget_found = True
                    sub_page               = possible_sub_page
                    continue
            if possible_toc_widget is not None:
                if toc_widget_found:
                    print('Multiple TOC widgets found',file=sys.stderr)
                    multiple_toc_widget_found = True
                else:
                    toc_widget_found = True
                    toc_widget       = possible_toc_widget
                continue
        if not toc_widget_found and not antecedent_content_found:
            for s in tag.stripped_strings:
                antecedent_content_found = True
                break
        if sub_pages_widget_found and not subsequent_content_found:
            for s in tag.stripped_strings:
                subsequent_content_found = True
                break

    if args.verbose:
        args.log.write(f'sub_pages_widget_found    = {sub_pages_widget_found}\n')
        args.log.write(f'toc_widget_found          = {toc_widget_found}\n')
        args.log.write(f'multiple_toc_widget_found = {multiple_toc_widget_found}\n')
        args.log.write(f'antecedent_content_found  = {antecedent_content_found}\n')
        args.log.write(f'subsequent_content_found  = {subsequent_content_found}\n')
        args.log.write(f'sub_page: {str(sub_page)}\n')
        args.log.write(f'toc_widget: {str(toc_widget)}\n')

# ------------------------------------------------------------------------------
# Convert Sub-pages Widget to YAML menu entries, unless content follows
#
# The sub-pages widget is implemented as a division that is either the first or
# element of the main content.
#
# If preceding content is present, this is kept as the main content with the
# sub-pages widget removed.
#
# However if there is content after the sub-pages widget, the widget is not
# converted to YML format, and the main content is undisturbed.
# ------------------------------------------------------------------------------

def extract_sub_menu_level( sub_page_menu, level ):
    assert sub_page_menu is not None, "sub_page_menu must not be None"
    assert type(level) == int and level > 0, "level must be a positive integer"

    indent = ''.ljust(2*(level-1))
    result = f"{indent}sub-pages:\n"
    for menu in sub_page_menu.children:
        if args.verbose:
            args.log.write(f'Sub-pages element: {menu.name}\n')
        if menu.name == 'li':
            entry = menu.a
            result += f"{indent}- title: '{entry.string.strip()}'\n"
            menu_url = normalise_url(entry['href'])
            if args.verbose:
                args.log.write(f"Sub-pages url is '{entry['href']}'\n")
                args.log.write(f"Sub-pages url normalised to '{menu_url}'\n")
            result += f"{indent}  url: {menu_url}\n"
            if args.verbose:
                args.log.write(f"Menu item added: '{entry.string.strip()}', '{menu_url}'\n")
            if menu.ul is not None:
                result += extract_sub_menu_level( menu.ul, level + 1 )
        elif menu.name in ['ol','ul']:
            result += extract_sub_menu_level( menu, level + 1 )

    assert type(result) == str and len(result) > 0, "Result must be a non-empty string"
    return result

if sub_pages_widget_found and not subsequent_content_found:
    if args.verbose:
        args.log.write('Sub-page widget without following content found.\n')
    page_header += f"sub-pages-title: '{sub_page.h4.string.strip()}'\n"
    sub_page_menu = sub_page.find('ul',{'jotid': "navList"})
    if sub_page_menu is None:
        error_msg = 'No sub-page menu found in sub-page widget'
        print(error_msg,file=sys.stderr)
        if args.verbose:
            args.log.write(error_msg + '\n')
        exit(1)
    page_header += extract_sub_menu_level( sub_page_menu, 1 )

    if args.verbose:
        args.log.write(f"Sub page removed: '{sub_page}'\n")
    sub_page.decompose()

if args.verbose:
    args.log.write('============> Start of Main Content (after removal of sub-page widget) <================\n')
    args.log.write(f'{str(content)}\n')
    args.log.write('============> End of Main Content (after removal of sub-page widget) <==================\n')

# ------------------------------------------------------------------------------
# Change URL to relative to Wiki base
# ------------------------------------------------------------------------------

if content is not None:
    for addr in content.find_all('a'):
        href         = addr.get('href')
        if href is None: continue
        # Regularise the URL to be relative to the documents base
        if args.verbose:
            args.log.write(f'A HREF Before: {str(href)}\n')
        addr['href'] = normalise_url(href)
        if args.verbose:
            args.log.write(f"A HREF After: {str(addr['href'])}\n")
        if need_to_remove_url(addr['href']) and addr not in tags_to_be_deleted:
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

# ------------------------------------------------------------------------------
# Replace '<A>' tags with imageanchor attributes with '<IMG>' tags
# ------------------------------------------------------------------------------

git_mv_cmds = list()
git_removals = list()

if content is not None:
    image_anchors = content.find_all('a', {'imageanchor': 1})
    for tag in image_anchors:
        if args.verbose:
            args.log.write(f'image anchor tag found: {str(tag)}\n')
        if tag.img is None:
            print(f"No <IMG> child found for <A> tag with imageanchor attribute", file=sys.stderr)
            exit(1)
        old_file_name = doc_base + os.path.sep + tag['href'].replace('%3F','?')
        if old_file_name.endswith('?attredirects=0'):
            new_file_name = old_file_name.replace('?attredirects=0','')
            if os.path.isfile(old_file_name):
                if os.path.isfile(new_file_name):
                    if args.verbose:
                        args.log.write(f"'{new_file_name}' already exists.\n")
                    print(f"'{new_file_name}' already exists", file=sys.stderr)
                    git_removals.append(old_file_name)
                    if args.verbose:
                        args.log.write(f"'{old_file_name}' scheduled for deletion.\n")
                else:
                    git_mv_cmd = f"git mv '{old_file_name}' '{new_file_name}'"
                    if args.verbose:
                        args.log.write(git_mv_cmd + '\n')
                    git_mv_cmds.append(git_mv_cmd)
            elif os.path.isfile(new_file_name):
                if args.verbose:
                    args.log.write(f"'{new_file_name}' already exists.\n")
            else:
                error_msg = f"Neither '{old_file_name}' nor '{new_file_name}' exist."
                if args.verbose:
                    args.log.write(error_msg + "\n")
                print(error_msg, file=sys.stderr)
                exit(1)
        else:
            new_file_name = old_file_name
        image_src = doc_base + os.path.sep + tag.img['src']
        if args.verbose:
            args.log.write(f"href='{old_file_name}'\nnew_file_name='{new_file_name}'\nimg_src='{image_src}'\n")
            args.log.write(f"image_src matched old_file_name='{old_file_name == image_src}'\n")
            args.log.write(f"new_file_name matched image_src='{new_file_name == image_src}'\n\n")
        if image_src not in git_removals and image_src not in [old_file_name, new_file_name]:
            if args.verbose:
                args.log.write(f"'{image_src}' to be removed\n")
            git_removals.append(image_src)
        tag.unwrap()
        tag['src'] = os.path.relpath(new_file_name, doc_base)
        if args.verbose:
            args.log.write(f"Tag after conversion: s{str(tag)}\n")

# ------------------------------------------------------------------------------
# (1) Remove links to *%3Fattredirects=0 files
# (2) Remove links to *png.html pages
# (3) Remove links to *gif.html pages
# ------------------------------------------------------------------------------

if content is not None:
    for addr in content.find_all('a'):
        if addr.get('href') is None: continue
        if need_to_remove_url(addr['href']) and addr not in tags_to_be_deleted:
            tags_to_be_deleted.append(addr)

    for addr in content.find_all('img'):
        href = addr.get('src')
        if href is None: continue
        if args.verbose:
            args.log.write(f"IMG SRC After: {str(href)}\n")
        local_image_path = doc_base + os.path.sep + href
        if need_to_remove_url(href) and addr not in tags_to_be_deleted:
            tags_to_be_deleted.append(addr)
        elif local_image_path is not None and not os.path.exists(local_image_path):
            print(f"Unable to locate image file, '{local_image_path}'",file=sys.stderr)
            if args.verbose:
                args.log.write(f"Unable to locate image file, '{local_image_path}'\n")
        else:
            if args.verbose:
                args.log.write(f"Will retain existing image file, '{local_image_path}'\n")

    if args.verbose:
        args.log.write(f'tags_to_be_deleted: --------->\n{str(tags_to_be_deleted)}\n<---------------\n')
        args.log.write('============> Start of Main Content (after rebasing of URLs) <================\n')
        args.log.write(f'{str(content)}\n')
        args.log.write('============> End of Main Content (after rebasing of URLs) <==================\n')

# ------------------------------------------------------------------------------
# Remove unnecessary tags
# ------------------------------------------------------------------------------

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
            file_name = doc_base + os.path.sep + href.replace('%3F','?')
            if file_name not in git_removals:
                if os.path.exists(file_name):
                    git_removals.append(file_name)
                    if args.verbose:
                        args.log.write(f"A HREF to be deleted: {str(file_name)}\n")
                else:
                    if args.verbose:
                        args.log.write(f"A HREF does not exist: {str(file_name)}\n")
            else:
                if args.verbose:
                    args.log.write(f"A HREF already in git_removal: {str(file_name)}\n")
        else:
            if args.verbose:
                args.log.write(f"A has no HREF attribute\n")
    elif tag.name == "img":
        src = tag.get('src')
        if src is not None:
            file_name = doc_base + os.path.sep + src.replace('%3F','?')
            if file_name not in git_removals:
                if os.path.exists(file_name):
                    git_removals.append(file_name)
                    if args.verbose:
                        args.log.write(f"IMG SRC to be deleted: {str(file_name)}\n")
                else:
                    if args.verbose:
                        args.log.write(f"IMG SRC does not exist: {str(file_name)}\n")
            else:
                if args.verbose:
                    args.log.write(f"IMG SRC already in git_removal: {str(file_name)}\n")
        else:
            if args.verbose:
                args.log.write(f"IMG has no SRC attribute\n")
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
            args.log.write(f'No TOC chscripts/convert_web_page.pyildren found at level {toc_level}\n')

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

if toc_widget_found and not antecedent_content_found and not multiple_toc_widget_found:
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
                print("missing URL for journal link",file=sys.stderr)
            elif link.endswith('.html'):
                pass
            else:
                link += '.html'
            page_header += f"    url: {link}\n    title: '{title}'\n"
        first_table = False
    tag.decompose()

if args.verbose:
    args.log.write('============> Start of Main Content (after Journal Scroll Bar) <================\n')
    args.log.write(f'{str(content)}\n')
    args.log.write('============> End of Main Content (after Journal Scroll Bar) <==================\n')

# ------------------------------------------------------------------------------
# Remove Empty DIV tags in up to four (4) levels
# ------------------------------------------------------------------------------

if content is not None:                
    for retries in range(5):
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

    num_children = len([child for child in content.children if child.name is not None])
    num_strings  = len([child for child in content.stripped_strings])
    child_names  = [child.name for child in content.children if child.name is not None]
    if args.verbose:
        args.log.write(f"num_children in content={num_children}\n")
        args.log.write(f"num_strings in content={num_strings}\n")
        args.log.write(f"child_names in content={str(child_names)}\n")
    if num_children == 0 and num_strings == 0:
        if args.verbose:
            args.log.write(f"Removed empty content: {str(content)}\n")
        content.decompose()
        content = None
    elif num_children == 1 and num_strings == 0:
        if child_names[0] == 'br':
            if args.verbose:
                args.log.write(f"Removed content with solitary BR tag: {str(tag)}\n")
            content.decompose()
            content = None

if args.verbose:
    args.log.write('============> Start of Main Content (after removal of empty DIV tags) <================\n')
    args.log.write(f'{str(content)}\n')
    args.log.write('============> End of Main Content (after removal of empty DIV tags) <==================\n')

# ------------------------------------------------------------------------------
# Detect and convert Uploaded Files
# ------------------------------------------------------------------------------

uploaded_files_widget = soup.find('div', {'id': 'sites-attachments-container'})
add_file_menu_toc     = False

if uploaded_files_widget is not None:
    if args.verbose:
        args.log.write(f'Uploaded files widget found: {str(uploaded_files_widget)}\n')

    uploaded_file_tags = uploaded_files_widget.find_all('div', 'sites-attachments-name')
    if args.verbose:
        if len(uploaded_file_tags) > 0:
            args.log.write(f'Uploaded file tags found: {str(uploaded_file_tags)}\n')
        else:
            args.log.write('No uploaded file tags found\n')
    if len(uploaded_file_tags) > 0 and len(auxiliary_files) == 0:
        error_msg = f"Uploaded files directory ('{auxiliary_dir}') does not exist and uploaded files found"
        print(error_msg, file=sys.stderr)
        if args.verbose:
            args.log.write(error_msg + "\n")
        exit(1)
    uploaded_file_list = list()
    for tag in uploaded_file_tags:
        if args.verbose:
            args.log.write(f'Uploaded file tag found: {str(tag)}\n')
        if tag.a is None:
            uploaded_file_name = [s for s in tag.stripped_strings][0]
        else:
            uploaded_file_name = tag.a.string.strip()
        if args.verbose:
            args.log.write(f'Uploaded file name: {str(uploaded_file_name)}\n')
        uploaded_file_list.append(uploaded_file_name)
        add_file_menu_toc = True
        download_file_tag = uploaded_files_widget.find('a', {'aria-label': "Download " + uploaded_file_name})
        if download_file_tag is not None:
            download_file_name = download_file_tag['href'].strip().replace('%3F','?').replace('/12-ocm/','/12c-ocm/')
            full_download_file_name = curr_dir + os.path.sep + download_file_name
            if args.verbose:
                args.log.write(f'Download file tag: {str(download_file_tag)}\n')
                args.log.write(f'Download file name: {download_file_name}\n')
                args.log.write(f'Full download file name: {full_download_file_name}\n')
            if os.path.basename(download_file_name) not in auxiliary_files:
                error_msg = f"Uploaded file ('{full_download_file_name}') does not exist"
                print(error_msg, file=sys.stderr)
                if args.verbose:
                    args.log.write(error_msg + "\n")
                exit(1)
            else:
                auxiliary_files.remove(os.path.basename(download_file_name))
            git_mv_cmds.append(f"git mv {full_download_file_name} {auxiliary_dir}/{uploaded_file_name}")
    
    for uploaded_file_name in uploaded_file_list:
        if args.verbose:
            args.log.write(f"Searching for occurrences of '{uploaded_file_name}':\n")
        occurrences = list()
        for descendant in content.descendants:
            if descendant.name is not None or \
               descendant.string is None or \
               descendant.string.count(uploaded_file_name) == 0: continue
            occurrences.append(descendant)
            if args.verbose:
                args.log.write(f'Occurrence found: {str(descendant)}\n')
        if args.verbose:
            args.log.write(f"{len(occurrences)} occurrences of '{uploaded_file_name}' found\n")
        wrapping_done = False
        for occurrence in occurrences:
            if occurrence.string.strip() != uploaded_file_name: continue
            wrapping_done = True
            new_a_tag = occurrence.string.wrap(soup.new_tag('a'))
            new_a_tag['href'] = os.path.relpath(auxiliary_dir + os.path.sep + uploaded_file_name,doc_base)
            if args.verbose:
                args.log.write(f'Occurrence wrapped: {str(occurrence)}\n')

        if not wrapping_done:
            error_msg = f"No occurrences of '{uploaded_file_name}' were wrapped."
            if args.verbose:
                args.log.write(error_msg + '\n')

    if args.verbose:
        args.log.write(f'GIT MV Cmds: {str(git_mv_cmds)}\n')
    
    if add_file_menu_toc:
        if len(toc_header) > 0:
            toc_header += "- toc-url: 'File-Downloads'\n  toc-text: 'File Downloads'\n"
            if args.verbose:
                args.log.write("TOC Header updated for file downloads:\n{toc_header}\n")
        file_downloads_tag = soup.new_tag('div')
        file_downloads_tag['class'] = 'file_downloads'
        content.append(file_downloads_tag)
        file_downloads_header = soup.new_tag('h2', id='TOC-File-Downloads')
        file_downloads_header.append('File Downloads')
        file_downloads_tag.append(file_downloads_header)
        file_downloads_list = soup.new_tag('ol')
        file_downloads_tag.append(file_downloads_list)
        for uploaded_file_name in uploaded_file_list:
            file_downloads_entry = soup.new_tag('li')
            file_downloads_list.append(file_downloads_entry)
            href = os.path.relpath(auxiliary_dir + os.path.sep + uploaded_file_name, doc_base)
            file_downloads_addr  = soup.new_tag('a', href=href)
            file_downloads_addr.append(uploaded_file_name)
            file_downloads_entry.append(file_downloads_addr)
        if args.verbose:
            args.log.write("Appended file downloads list to main content:\n")
            args.log.write("=============================================\n")
            args.log.write(str(file_downloads_tag))
            args.log.write("\n=============================================\n")
    
        # for file_name in auxiliary_files:
        #     git_removals.append(auxiliary_dir + os.path.sep + file_name)
        #     if args.verbose:
        #         args.log.write(f"Scheduling auxiliary file '{file_name}' for removal\n")

if args.verbose:
    args.log.write('============> Start of Main Content (after conversion of uploaded files) <================\n')
    args.log.write(f'{str(content)}\n')
    args.log.write('============> End of Main Content (after conversion of uploaded files) <==================\n')

# ------------------------------------------------------------------------------
# GIT Removals and Movements
#
# Because of an issue with process.run, GIT commands have to be run manually.
# Movement commands take precedence over removals. That is, if the source file
# is to be removed, it is dropped from the removal list.
# ------------------------------------------------------------------------------

for mv_cmd_str in git_mv_cmds:
    src_file_name = mv_cmd_str.split()[2].strip("'")
    if src_file_name in git_removals:
        git_removals.remove(src_file_name)
        if args.verbose:
            args.log.write(f"'{src_file_name}' removed from list of GIT RM commands\n")

if args.verbose:
    args.log.write(f"GIT commands:\n")
    for rm_file in git_removals:
        args.log.write(f"  git rm '{rm_file}'\n")
    for mv_cmd_str in git_mv_cmds:
        args.log.write(f"  {mv_cmd_str}\n")
if args.git_remove:
    print('Run the following commands manually:')
    for rm_file in git_removals:
        rm_cmd_str = f"git rm '{rm_file}'"
        print(rm_cmd_str)
        if args.verbose:
            args.log.write(f"rm_cmd_str: {rm_cmd_str}\n")
    for mv_cmd_str in git_mv_cmds:
        print(mv_cmd_str)
        if args.verbose:
            args.log.write(f"mv_cmd_str: {mv_cmd_str}\n")

# ------------------------------------------------------------------------------
# Print out YAML data
# ------------------------------------------------------------------------------

page_header += toc_header
page_header += '---\n'
if args.replace:
    with open(os.path.basename(args.input_html_file_name[0]),'w') as f:
        f.write(page_header)
        if content is not None:
            f.write(content.prettify())
else:
    print(page_header)
    if content is not None:
        print(content.prettify())
