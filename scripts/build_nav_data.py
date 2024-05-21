#!/usr/bin/env python3
# ------------------------------------------------------------------------------
# Build navigation hierarchy in YAML format
# ------------------------------------------------------------------------------

import argparse
import os
import sys

# ------------------------------------------------------------------------------
# Parse arguments
# ------------------------------------------------------------------------------

parser = argparse.ArgumentParser(
        description='Build navigation hierarchy based on a hierarchy of web pages'
        )
parser.add_argument('-v','--verbose',action='store_true',help='Verbose output')
parser.add_argument(
    '-s',
    '--side-nav',
    default=sys.stdout,
    type=argparse.FileType('w'),
    help='Name of file for side navigation bar')
parser.add_argument(
    '-l',
    '--log',
    default=sys.stdout,
    type=argparse.FileType('w'),
    help='the file where the verbose logging should be written')
args = parser.parse_args()

# ------------------------------------------------------------------------------
# Find location of root directory for HTML documents based on the location of
# this program. The assumption is that the document root and
# script directories are siblings.
# ------------------------------------------------------------------------------

script_name = os.path.realpath(__file__)
script_dir  = os.path.dirname(script_name)
common_dir  = os.path.dirname(script_dir)
html_dir    = os.path.join(common_dir,'docs')

if args.verbose:
    args.log.write(f"""Constructing directories:
script_name = '{script_name}'
script_dir  = '{script_dir}'
common_dir  = '{common_dir}'
html_dir    = '{html_dir}'
""")

if not os.path.isdir(html_dir):
    error_msg = f"*** '{html_dir}' is not a directory ***"
    if args.verbose:
        args.log.write(error_msg + '\n')
    print(error_msg, file=sys.stderr)
    exit(1)

# ------------------------------------------------------------------------------
# Auxiliary function to convert a dictionary to a string
# ------------------------------------------------------------------------------

def dict_to_str(in_dict, in_depth):
    """
    Converts a dictionary object to a string

    Parameters:
    1. in_dict is a dictionary
    2. in_depth is how deep we are in the top-level dictionary

    Returns:
       a string
    """

    assert  in_dict is not None   and \
            type(in_dict) == dict and \
            len(in_dict) > 0,         \
        "in_dict must be a non-empty dictionary"
    assert  in_depth is not None  and \
            type(in_depth) == int and \
            in_depth >= 0,            \
        "in_depth must a non-negative integer"
    
    indent = ''.rjust(2*(in_depth+1))
    result = indent + "{\n"
    keys   = list(in_dict.keys())
    keys.sort()
    for key in keys:
        value   = in_dict[key]
        result += indent + key + ":"
        if type(value) == dict:
            if len(value) > 0:
                result += "\n" + dict_to_str(value,in_depth+1)
            else:
                result += "{},\n"
        else:
            result += " " + str(value) + ",\n"
        
    result += indent + "}\n"
    
    assert  result is not None  and \
            type(result) == str and \
            len(result) > 0,        \
        "result must be a non-empty string"
    return result

# ------------------------------------------------------------------------------
# Build a dictionary of web files and extract title
# ------------------------------------------------------------------------------

def get_page_title(web_page_name):
    """
    Extract page title

    Parameters:
    1. web_page_name

    Returns:
        result is the page title
    """
    assert  web_page_name is not None       and \
            type(web_page_name) == str      and \
            len(web_page_name.strip()) > 0,     \
            "web_page_name must a non-empty string"
    
    result = os.path.basename(web_page_name).removesuffix('.html').replace('-',' ').title()

    if args.verbose:
        args.log.write(f"get_page_title('{web_page_name}') called\n")
        args.log.write(f"    default result='{result}'\n")

    if os.path.isfile(web_page_name):
        with open(web_page_name,'r') as f:
            for line in f:
                if line.startswith('title: '):
                    result = line[len('title: '):-1]
                    break
    else:
        warn_msg = f">>> Missing anchor page, '{web_page_name}'"
        if args.verbose:
            args.log.write(warn_msg + '\n')
        print(warn_msg, file=sys.stderr)

    if args.verbose:
        args.log.write(f"get_page_title('{web_page_name}') returned\n")
        args.log.write(f"    result='{result}'\n")
    
    assert  result is not None             and \
            type(result) == str            and \
            len(result.strip()) > 0,           \
            "result must be a non-empty string"

    return result

web_tree          = dict()

for sub_pages_dir_name, sub_pages_sub_dirs, sub_pages_file_names in \
    os.walk(html_dir):
    if args.verbose:
        args.log.write(f"sub_pages_dir_name={str(sub_pages_dir_name)}\n")
        args.log.write(f"sub_pages_sub_dirs={str(sub_pages_sub_dirs)}\n")
        args.log.write(f"sub_pages_file_names={str(sub_pages_file_names)}\n")
    rel_dir_name = os.path.relpath(sub_pages_dir_name, html_dir)
    # Don't process Jekyll and Google Site files
    if rel_dir_name.startswith('.jekyll-cache') or \
       rel_dir_name.startswith('_data')         or \
       rel_dir_name.startswith('_drafts')       or \
       rel_dir_name.startswith('_includes')     or \
       rel_dir_name.startswith('_layouts')      or \
       rel_dir_name.startswith('_posts')        or \
       rel_dir_name.startswith('_sass')         or \
       rel_dir_name.startswith('_site')         or \
       rel_dir_name.startswith('assets')        or \
       rel_dir_name.startswith('system'):
        continue
    sub_pages_with_content = [pfn
        for pfn in sub_pages_file_names
        if pfn.endswith('.html') and 
            not (
                pfn.startswith('AWR_report_') or
                pfn.startswith('ASH_report_') or
                pfn.startswith('workload_report_') or
                pfn.startswith('google')
                ) and
            pfn.removesuffix('.html') not in sub_pages_sub_dirs or
            pfn.endswith('.md')
    ]
    if args.verbose:
        args.log.write(f"sub_pages_with_content={str(sub_pages_with_content)}\n")
    if len(sub_pages_with_content) + len(sub_pages_sub_dirs) == 0: continue
    if args.verbose:
        args.log.write(f"Sub-anchor directory found '{rel_dir_name}'\n")
    if rel_dir_name != '.':
        dir_levels = rel_dir_name.split('/')
        if args.verbose:
            args.log.write(f"DIR Levels={str(dir_levels)}\n")
        if web_tree.get(dir_levels[0]) is None:
            error_msg = f'*** Tree node for {dir_levels[0]} is not allocated'
            if args.verbose:
                args.log.write(error_msg + '\n')
            print(error_msg, file=sys.stderr)
            exit(1)
        sub_pages = web_tree[dir_levels[0]].get('sub-pages')
        if sub_pages is None:
            error_msg = f'*** Sub-pages node for {dir_levels[0]} is not allocated'
            if args.verbose:
                args.log.write(error_msg + '\n')
            print(error_msg, file=sys.stderr)
            exit(1)
        page_entry = web_tree[dir_levels[0]]
        for dir_entry in dir_levels[1:]:
            page_entry = sub_pages[dir_entry]
            if sub_pages.get(dir_entry) is None:
                error_msg = f"*** Missing dir_entry, '{dir_entry}' ***"
                if args.verbose:
                    args.log.write(error_msg + '\n')
                print(error_msg, file=sys.stderr)
                exit(1)
            sub_pages = sub_pages[dir_entry]['sub-pages']
        page_entry['url'] = rel_dir_name + '.html'
        for sub_dir in sub_pages_sub_dirs:
            sub_pages[sub_dir]              = dict()
            sub_pages[sub_dir]['sub-pages'] = dict()
            web_page_name = os.path.join(sub_pages_dir_name,sub_dir) + '.html'
            if args.verbose:
                args.log.write(f"Anchor page name='{web_page_name}'\n")
            sub_pages[sub_dir]['title'] = get_page_title(web_page_name)
            sub_pages[sub_dir]['url']   = os.path.relpath(web_page_name,start=html_dir)
        for page_name in sub_pages_with_content:
            sub_pages[page_name] = dict()
            web_page_name = os.path.join(sub_pages_dir_name,page_name)
            if args.verbose:
                args.log.write(f"Sub-page name='{web_page_name}'\n")
            if page_name.endswith('.md'):
                conv_page_name = page_name.removesuffix('.md') + '.html'
                sub_pages[page_name]['title'] = get_page_title(web_page_name)
                sub_pages[page_name]['url']   = os.path.relpath(
                                                    web_page_name.removesuffix('.md') + '.html',
                                                    start=html_dir
                                                )
            else:
                sub_pages[page_name]['title'] = get_page_title(web_page_name)
                sub_pages[page_name]['url']   = os.path.relpath(web_page_name,start=html_dir)
    else:
        for sub_dir in sub_pages_sub_dirs:
            if sub_dir in [
                    '.jekyll-cache', '_data', '_drafts', '_includes',
                    '_layouts', '_posts', '_sass', '_site', 'system',
                    'assets'
                ]: continue
            if sub_dir == 'home':
                web_tree[sub_dir]              = dict()
                web_tree[sub_dir]['sub-pages'] = dict()
                web_page_name                  = os.path.join(html_dir,'index.html')
                web_tree[sub_dir]['url']       = 'index.html'
            else:
                web_tree[sub_dir]              = dict()
                web_tree[sub_dir]['sub-pages'] = dict()
                web_page_name                  = os.path.join(html_dir,sub_dir) + '.html'
                web_tree[sub_dir]['url']       = sub_dir + '.html'
            if args.verbose:
                args.log.write(f"Anchor page name='{web_page_name}'\n")
            web_tree[sub_dir]['title'] = get_page_title(web_page_name)
            if args.verbose:
                args.log.write(f"web_tree['{sub_dir}'] = {str(web_tree[sub_dir])}\n")
        for page_name in sub_pages_with_content:
            if page_name == 'index.html': continue
            web_tree[page_name] = dict()
            web_page_name = os.path.join(html_dir,page_name)
            if args.verbose:
                args.log.write(f"Sub-page name='{web_page_name}'\n")
            web_tree[page_name]['title'] = get_page_title(web_page_name)
            web_tree[page_name]['url']   = os.path.relpath(web_page_name,start=html_dir)

if args.verbose:
    args.log.write(f'web_tree={dict_to_str(web_tree,0)}\n')

# ------------------------------------------------------------------------------
# Construct a navigation YAML structure from a dictionary
# ------------------------------------------------------------------------------

def dict_to_nav(in_dict, in_depth):
    """
    Converts a dictionary object to a navigation YAML structure

    Parameters:
    1. in_dict is a dictionary
    2. in_depth is how deep we are in the top-level dictionary

    Returns:
       a string
    """

    assert  in_dict is not None   and \
            type(in_dict) == dict and \
            len(in_dict) > 0,         \
        "in_dict must be a non-empty dictionary"
    assert  in_depth is not None  and \
            type(in_depth) == int and \
            in_depth >= 0,            \
        "in_depth must a non-negative integer"
    
    if args.verbose:
        args.log.write('Call to dict_to_nav:\n')
        args.log.write(f"keys={str(in_dict.keys())}\n")
        args.log.write(f"\nin_depth={in_depth}\n")
    
    indent    = ''.rjust(2*in_depth)
    keys      = list(in_dict.keys())
    keys.sort()
    result    = ''
    for key in keys:
        value     = in_dict[key]
        if args.verbose:
            args.log.write(f"in_dict['{key}'] = {str(value)}\n")
        if key == 'home':
            result   += indent + "- url: home.html\n"
            result   += indent + "  title: 'Home'\n"
        else:
            result   += indent + "- url: " + value.get('url','**** missing url ****') + "\n"
            title     = value.get('title','**** missing title ****')
            if title.startswith("'"):
                result   += indent + "  title: " + value.get('title',"'**** missing title ****'") + "\n"
            else:
                result   += indent + "  title: '" + value.get('title','**** missing title ****') + "'\n"
        sub_pages = value.get('sub-pages',{})
        if args.verbose:
            args.log.write(f"sub_pages={str(sub_pages)}\n")
        if len(sub_pages) > 0:
            result += indent + "  sub-pages:\n"
            result += dict_to_nav(sub_pages,in_depth+1)
    
    assert  result is not None  and \
            type(result) == str and \
            len(result) > 0,        \
        "result must be a non-empty string"
    return result

nav_data = dict_to_nav(web_tree, 0)

if args.verbose:
    args.log.write('============== NAV Data (START) ====================\n')
    args.log.write(nav_data)
    args.log.write('=============== NAV Data (END) =====================\n')

args.side_nav.write(nav_data)
