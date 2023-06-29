#!/usr/bin/env python3
# ------------------------------------------------------------------------------
# Find newer Wiki pages (issue #3)
# ------------------------------------------------------------------------------


import argparse
from bs4 import BeautifulSoup
import os
import subprocess
import sys

# ------------------------------------------------------------------------------
# Parse arguments
# ------------------------------------------------------------------------------

parser = argparse.ArgumentParser(
        description='Find newer Wiki pages'
        )
parser.add_argument('-v','--verbose',action='store_true',help='Verbose output')
parser.add_argument('-n','--dry-run',action='store_true',help='Do a dry run')
parser.add_argument('-d','--wiki-dir',help='Root of directory tree for new Wiki')
parser.add_argument(
    'html_dir',
    nargs=1,
    type=str,
    help='Root of directory tree containing HTML files'
    )
args = parser.parse_args()

# ------------------------------------------------------------------------------
# Build a dictionary of new Wiki files.
# ------------------------------------------------------------------------------

new_wiki_files = dict()
if args.verbose: print(dir(args))
if args.wiki_dir is None:
    print("--wiki-dir=<dir> is a required parameter.", file=sys.stderr)
    exit(1)

if args.verbose: print(f"Root of directory tree for new Wiki pages is '{args.wiki_dir}'")
wiki_dir = subprocess.run(
        ['find',args.wiki_dir,'-type','f'],
        capture_output=True,
        check=True)
for path_name in str(wiki_dir.stdout)[2:-3].split('\\n'):
    if args.verbose: print(f"new Wiki page path name='{path_name}'")
    file_name = os.path.realpath(path_name).replace(
        '/home/douglas/Documents/YAOCM_new_site/sites.google.com/view/yetanotherocm/',
        '/home/douglas/Documents/dfhawthorne.github.io/docs/') + ".html"
    new_wiki_files[file_name] = path_name

# ------------------------------------------------------------------------------
# Build a dictionary of new Wiki files.
# ------------------------------------------------------------------------------

if args.verbose: print(f"Root of directory tree for old Wiki pages is '{args.html_dir[0]}'")
html_dir = subprocess.run(
        ['find',args.html_dir[0],'-name','*.html','-type','f'],
        capture_output=True,
        check=True)
old_wiki_files = str(html_dir.stdout)[2:-3].split('\\n')

# ------------------------------------------------------------------------------
# Find newer Wiki Files
# ------------------------------------------------------------------------------

for new_file in new_wiki_files.keys():
    if new_file in old_wiki_files: continue
    if args.verbose:
        print(f"Newer Wiki file, '{new_wiki_files[new_file]}', needs to be copied to '{new_file}'.")
    new_wiki_file = new_wiki_files[new_file]
    wiki_dir = os.path.dirname(new_file)
    if not os.path.exists(wiki_dir):
        if args.verbose:
            print(f"Wiki directory, '{wiki_dir}', needs to be created.")
        if args.dry_run:
            print(f"mkdir -p {wiki_dir}")
        else:
            os.makedirs(wiki_dir)
            print(f"Wiki directory, '{wiki_dir}', created.")
    if args.dry_run:
        print(f"cp {new_wiki_file} {new_file}")
    else:
        with open(new_file,'wb') as dst:
            with open(new_wiki_file,'rb') as src:
                dst.write(src.read())
        print(f"Copy '{new_wiki_file}' to '{new_file}' done.")
