#!/usr/bin/env python3
# ------------------------------------------------------------------------------
# Rebuild Sub-Pages menu page
# ------------------------------------------------------------------------------

import argparse
import os
import re
import sys

# ------------------------------------------------------------------------------
# Parse arguments
# ------------------------------------------------------------------------------

parser = argparse.ArgumentParser(
    description='Rebuild Sub-Pages menu page using navigation data'
    )
parser.add_argument(
    'file_name',
    nargs=1,
    type=str,
    help='name of anchor file')
parser.add_argument(
    '-l',
    '--log',
    default=sys.stdout,
    type=argparse.FileType('w'),
    help='the file where the verbose logging should be written')
parser.add_argument(
    '-n',
    '--nav-data',
    type=str,
    help='the file containing the navigation data')
parser.add_argument(
    '-v',
    '--verbose',
    default=False,
    action='store_true',
    help='enables verbose logging')
parser.add_argument(
    '-r',
    '--replace',
    default=False,
    action='store_true',
    help='replaces input file with updated sub-pages menu')
args = parser.parse_args()

# ------------------------------------------------------------------------------
# Check input file name
# ------------------------------------------------------------------------------

if args.verbose:
    args.log.write(f"file_name={args.file_name}\n")

input_anchor_page_path = args.file_name[0]
if not os.path.isfile(input_anchor_page_path):
    error_message = f"'{input_anchor_page_path}' is not a file"
    if args.verbose:
        args.log.write(error_message+'\nExiting.\n')
    print(error_message,file=sys.stderr)
    exit(1)

# ------------------------------------------------------------------------------
#  Locate sub-pages within directory pointed to by input file name
# ------------------------------------------------------------------------------

scripts_dir           = os.path.dirname(os.path.realpath(__file__))
abs_anchor_page_path  = os.path.abspath(input_anchor_page_path)
docs_dir              = os.path.join(os.path.dirname(scripts_dir),'docs')
rel_anchor_page_path  = os.path.relpath(abs_anchor_page_path, start=docs_dir)
if rel_anchor_page_path.endswith(".md"):
    base_anchor_page_path, _ = os.path.splitext(rel_anchor_page_path)
    rel_anchor_page_path     = base_anchor_page_path + ".html"

if args.nav_data is not None:
    nav_data_path     = args.nav_data
else:
    nav_data_path     = os.path.join(docs_dir, '_data', 'navigation.yml')
if args.verbose:
    args.log.write(f"script_name={__file__}\n")
    args.log.write(f"scripts_dir={scripts_dir}\n")
    args.log.write(f"abs_anchor_page_path={abs_anchor_page_path}\n")
    args.log.write(f"docs_dir={docs_dir}\n")
    args.log.write(f"nav_data_path={nav_data_path}\n")
    args.log.write(f"rel_anchor_page_path='{rel_anchor_page_path}'\n")

# ------------------------------------------------------------------------------
# Split current content of the anchor page into several parts:
# (1) page header
#     (1.1) before sub-pages menu
#     (1.2) sub-pages menu
#     (1.3) after sub-pages menu
# (2) HTML content
# ------------------------------------------------------------------------------

with open(input_anchor_page_path) as f:
    in_file_buffer = f.read()
if args.verbose:
    args.log.write('in_file_buffer ================ (BEGIN) ================\n')
    args.log.write(in_file_buffer + '\n')
    args.log.write('in_file_buffer ================= (END) =================\n')
(old_page_header,partition_str,page_content) = in_file_buffer.partition('\n---\n')
# old_page_header += partition_str
if args.verbose:
    args.log.write('old_page_header =============== (BEGIN) ================\n')
    args.log.write(old_page_header + '\n')
    args.log.write('old_page_header ================ (END) =================\n')
    args.log.write('page_content ================== (BEGIN) ================\n')
    args.log.write(page_content + '\n')
    args.log.write('page_content =================== (END) =================\n')
page_header_keys = re.findall('\n([a-z][a-z-]*):',old_page_header)
if args.verbose:
    args.log.write(f'page_header_keys: {page_header_keys}\n')
if 'sub-pages' in page_header_keys:
    if page_header_keys.index('sub-pages') == len(page_header_keys) -1:
        (old_pre_page_header,partition_str,old_sub_pages_menu) = \
            old_page_header.partition('\nsub-pages:\n')
        old_sub_pages_menu = 'sub-pages:\n' + old_sub_pages_menu
        old_post_page_header = ''
    else:
        next_key = page_header_keys[page_header_keys.index('sub-pages')+1]
        (old_pre_page_header,partition_str,tail_page_header) = \
            old_page_header.partition('\nsub-pages:\n')
        (old_sub_pages_menu,partition_str,old_post_page_header) = \
            tail_page_header.partition(f"\n{next_key}:")
        old_sub_pages_menu = 'sub-pages:\n' + old_sub_pages_menu
        old_post_page_header = next_key + ':' + old_post_page_header
else:
    old_pre_page_header  = old_page_header
    old_sub_pages_menu   = ''
    old_post_page_header = ''        
if args.verbose:
    args.log.write('old_pre_page_header ============== (BEGIN) ==============\n')
    args.log.write(old_pre_page_header + '\n')
    args.log.write('old_pre_page_header =============== (END) ===============\n')
    args.log.write('old_sub_pages_menu =============== (BEGIN) ==============\n')
    args.log.write(old_sub_pages_menu + '\n')
    args.log.write('old_sub_pages_menu ================ (END) ===============\n')
    args.log.write('old_post_page_header ============== (BEGIN) =============\n')
    args.log.write(old_post_page_header + '\n')
    args.log.write('old_post_page_header =============== (END) ==============\n')

# ------------------------------------------------------------------------------
# Construct the new sub-pages menu using navigation data
# ------------------------------------------------------------------------------

new_sub_pages_menu = ''
copy_lines         = False
search_str         = '---'
with open(nav_data_path,'r') as f:
    for line in f:
        if args.verbose:
            args.log.write(f"NAV DATA: {line}")
        if line.find(rel_anchor_page_path) >= 0:
            indent = line.find('-') + 2
            search_str = ''.rjust(indent) + 'sub-pages:'
            if args.verbose:
                args.log.write(f"'{rel_anchor_page_path}' found in navigation data\n")
                args.log.write(f"indent={indent}\n")
                args.log.write(f"search_str='{search_str}'\n")
            continue
        if line.startswith(search_str):
            copy_lines = True
        if copy_lines:
            if len(line[:indent].strip()) != 0: break
            new_sub_pages_menu += line[indent:]

sub_pages_menu_changed =  old_sub_pages_menu.strip() != new_sub_pages_menu.strip()
if args.verbose:
    args.log.write('new_sub_pages_menu =============== (BEGIN) ==============\n')
    args.log.write(new_sub_pages_menu + '\n')
    args.log.write('new_sub_pages_menu ================ (END) ===============\n')
    if sub_pages_menu_changed:
        args.log.write('*** Sub-pages menu is changed ***\n')
    else:
        args.log.write('*** Sub-pages menu is unchanged ***\n')

# ------------------------------------------------------------------------------
# Rebuild page if changes are detected and replacement has been requested
# ------------------------------------------------------------------------------

if args.replace:
    if not sub_pages_menu_changed:
        warning_msg = 'No changes detected in sub-pages menu. Page is NOT replaced.'
        if args.verbose:
            args.log.write(warning_msg + '\n')
        print(warning_msg, file=sys.stderr)
        exit(0)
    out_buffer = old_pre_page_header + \
        '\n'                         + \
        new_sub_pages_menu           + \
        old_post_page_header         + \
        '---\n'                      + \
        page_content
    if args.verbose:
        args.log.write('out_buffer =================== (BEGIN) ==================\n')
        args.log.write(out_buffer + '\n')
        args.log.write('out_buffer ===================== (END) ==================\n')
    with open(input_anchor_page_path,'w') as f:
        f.write(out_buffer)
else:
    if sub_pages_menu_changed:
        warning_msg = 'Changes detected in sub-pages menu. Page is NOT replaced.'
        if args.verbose:
            args.log.write(warning_msg + '\n')
        print(warning_msg, file=sys.stderr)
        exit(0)


args.log.close()
