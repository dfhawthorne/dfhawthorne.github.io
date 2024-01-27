#!/usr/bin/env python3
# ------------------------------------------------------------------------------
# Build navigation hierarchy in YAML format
# ------------------------------------------------------------------------------

import argparse
from bs4 import BeautifulSoup
import subprocess

# ------------------------------------------------------------------------------
# Parse arguments
# ------------------------------------------------------------------------------

parser = argparse.ArgumentParser(
        description='Build navigation hierarchy based on a hierarchy of web pages'
        )
parser.add_argument('-v','--verbose',action='store_true',help='Verbose output')
parser.add_argument('-s','--side-nav',help='Name of file for side navigation bar')
parser.add_argument('-t','--top-nav',help='Name of file for top navigation bar')
parser.add_argument('-d','--max-depth',help='Maximum depth to descend',type=int,default=2)
parser.add_argument(
    'html_dir',
    nargs=1,
    type=str,
    help='Root of directory tree containing HTML files'
    )
args = parser.parse_args()
if args.verbose:
    print(f"""Passed arguments:
    side-nav={args.side_nav}
    top-nav={args.top_nav}
    max-depth={str(args.max_depth)}""")

# ------------------------------------------------------------------------------
# Build a dictionary of web files and extract title and heading #1
# ------------------------------------------------------------------------------

web_titles = dict()
file_name_pref_len  = len(args.html_dir[0]) + 1

html_dir = subprocess.run(
        [
            'find',
            args.html_dir[0],
            '-maxdepth',
            str(args.max_depth+1),
            '-name',
            '*.html',
            '-type',
            'f'
        ],
        capture_output=True,
        check=True)

for input_file in str(html_dir.stdout)[2:-3].split('\\n'):
    if args.verbose: print(f"input_file='{input_file}'")
    rel_path_name = input_file[file_name_pref_len:]
    if args.verbose: print(f"rel_path_name='{rel_path_name}'")
    # Don't process Jekyll and Google Site files
    if rel_path_name.startswith('system'):        continue
    if rel_path_name.startswith('_site'):         continue
    if rel_path_name.startswith('_sass'):         continue
    if rel_path_name.startswith('_includes'):     continue
    if rel_path_name.startswith('_layouts'):      continue
    if rel_path_name.startswith('.jekyll-cache'): continue

    with open(input_file, 'r') as f:
        b = f.read()
    soup = BeautifulSoup(b, 'html.parser')

    titles = soup.find_all('title')
    if titles is not None and len(titles) > 0:
        title = titles[0].text.strip()
    else:
        headers = soup.find_all('h1')
        if headers is not None and len(headers) > 0:
            title = headers[0].text.strip()
        else:
            span_titles = soup.find_all('span', id="sites-page-title")
            if span_titles is not None and len(span_titles) > 0:
                title = span_titles[0].text.strip()
            else:
                title = None

    if title is not None:
        title = title.replace(' - Yet Another OCM','')
    if args.verbose: print(f"title='{title}'")

    web_titles[rel_path_name] = title

if args.verbose: print(web_titles)

# ------------------------------------------------------------------------------
# Build directory tree of web pages
# ------------------------------------------------------------------------------

web_tree              = dict()
web_tree['title']     = 'Root'
web_tree['url']       = '/'
web_tree['sub_pages'] = dict()
web_keys = list(web_titles.keys())
web_keys.sort()

for page in web_keys:
    if args.verbose: print(f"page='{page}'")
    dir_path = page.split('/')
    if args.verbose: print(f"dir_path={dir_path}")
    if len(dir_path) < 2: continue
    partial_path = ''
    dir_level    = web_tree
    for dir_entry in dir_path[:-1]:
        if partial_path == '':
            partial_path = dir_entry
        else:
            partial_path = partial_path + '/' + dir_entry
        if dir_level['sub_pages'].get(dir_entry) is None:
            new_entry                         = dict()
            new_entry['title']                = web_titles.get(partial_path+'.html')
            new_entry['sub_pages']            = dict()
            new_entry['url']                  = partial_path
            dir_level['sub_pages'][dir_entry] = new_entry
            dir_level                         = new_entry
            if args.verbose:
                print(f"dir_level[{dir_entry}]={new_entry}")
        else:
            dir_level    = dir_level['sub_pages'][dir_entry]

if args.verbose:
    print(f"web_tree={web_tree}")

# ------------------------------------------------------------------------------
# Produce navigation bars as YAML
# ------------------------------------------------------------------------------

def get_side_nav_level(web_dict, indent=0):
    """
    get_side_nav_level(web_dict, indent)
      web_dict is a dictionary
      indent
    """
    assert type(web_dict) == dict and len(web_dict) > 0, \
        "<web_dict> must be a non-empty dictionary"
    assert type(indent) == int and indent >= 0, \
        "<indent> must be an non-negative integer"

    if args.verbose: print(f"web_dict={web_dict}")
    web_keys = list(web_dict.keys())
    web_keys.sort()
    if args.verbose: print(f"web_keys={web_keys}")
    result   = ''

    for page in web_keys:
        result += ''.ljust(indent)+'- name: '+page+'\n'
        item = web_dict[page]
        if item.get('url') is None or item.get('title') is None:
            continue
        for key in ['url','title']:
            result += ''.ljust(indent)+'  '+key+': '+item[key]+'\n'
        sub_pages = item.get('sub_pages')
        if sub_pages is None or len(sub_pages) == 0: continue
        result += ''.ljust(indent)+'  sub_pages:'+'\n'
        result += get_side_nav_level(sub_pages,indent+2)
    
    return result

def get_top_nav_level(web_dict, stack=[]):
    """
    get_top_nav_level(web_dict, indent)
      web_dict is a dictionary
      indent
    """
    assert type(web_dict) == dict and len(web_dict) > 0, \
        "<web_dict> must be a non-empty dictionary"
    assert type(stack) == list, \
        "<stack> must be a list"

    web_keys = list(web_dict.keys())
    web_keys.sort()
    result   = ''

    for page in web_keys:
        page_entry          = dict()
        item                = web_dict[page]
        page_entry['url']   = item['url']
        page_entry['title'] = item.get('title','UKNOWN')
        stack.append(page_entry)
        sub_pages           = item.get('sub_pages')
        if sub_pages is not None and len(sub_pages) > 0:
            result += get_top_nav_level(sub_pages,stack)
        nav_bar = ''
        for page_entry in stack:
            if nav_bar != '': nav_bar += ' &gt; '
            nav_bar += f'<a href="{page_entry["url"]}">{page_entry["title"]}</a>'
        page_entry = stack.pop()
        result    += f"- url: {page_entry['url']}\n  nav_bar: '{nav_bar}'\n"
    
    return result

if args.side_nav is not None:
    with open(args.side_nav,'w') as f:
        f.write(get_side_nav_level(web_tree['sub_pages']))

if args.top_nav is not None:
    with open(args.top_nav,'w') as f:
        f.write(get_top_nav_level(web_tree['sub_pages']))
