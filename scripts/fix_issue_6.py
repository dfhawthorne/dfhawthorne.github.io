#!/usr/bin/env python3
# ------------------------------------------------------------------------------
# Find missing images (issue #6)
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
        description='Find missing images'
        )
parser.add_argument('-v','--verbose',action='store_true',help='Verbose output')
parser.add_argument('-n','--dry-run',action='store_true',help='Do a dry run')
parser.add_argument('-d','--img-dir',help='Root of directory tree for images')
parser.add_argument(
    'html_dir',
    nargs=1,
    type=str,
    help='Root of directory tree containing HTML files'
    )
args = parser.parse_args()

# ------------------------------------------------------------------------------
# Build a dictionary of image files if required.
# ------------------------------------------------------------------------------

image_files = dict()
if args.verbose: print(dir(args))
if args.img_dir is not None:
    if args.verbose: print(f'Root of directory tree for images is ''{args.img_dir}''')
    img_dir = subprocess.run(
            ['find',args.img_dir,'-type','f'],
            capture_output=True,
            check=True)
    for path_name in str(img_dir.stdout)[2:-3].split('\\n'):
        if args.verbose: print(f"image path name='{path_name}'")
        file_name = os.path.basename(os.path.realpath(path_name))
        if image_files.get(file_name) is None:
            image_files[file_name] = [path_name]
        else:
            image_files[file_name].append(path_name)
            if args.verbose: print(f"duplicate image found: '{file_name}'")

# ------------------------------------------------------------------------------
# Parse the source HTML file
# ------------------------------------------------------------------------------

html_dir = subprocess.run(
        ['find',args.html_dir[0],'-name','*.html','-type','f'],
        capture_output=True,
        check=True)
for input_file in str(html_dir.stdout)[2:-3].split('\\n'):
    if args.verbose: print(f"input_file='{input_file}'")
    with open(input_file, 'r') as f:
        b = f.read()
    soup = BeautifulSoup(b, 'html.parser')

    html_dir = os.path.dirname(os.path.realpath(input_file))
    if args.verbose: print(f"html_dir='{html_dir}")
    os.chdir(html_dir)

    for img_tag in soup.find_all('img'):
        uri = img_tag.get('src')
        if uri is None: continue
        if args.verbose: print(f"URI='{uri}'")
        if uri.split(':')[0] in ['http','https','javascript','ftp']: continue
        img_path = os.path.realpath(uri)
        if args.verbose: print(f"real path='{img_path}'")
        if os.path.exists(img_path): continue
        print(f"'{input_file}' is missing an image file, '{img_path}'", file=sys.stderr)
        img_file_name = os.path.basename(img_path)
        img_file_dir  = os.path.dirname(img_path)
        src_img_files = image_files.get(img_file_name)
        if src_img_files is None:
            print(f"Image file, '{img_file_name}', not found", file=sys.stderr)
            continue
        elif len(src_img_files) > 1:
            print(f"Duplicate image files found: {','.join(src_img_files)}", file=sys.stderr)
        if not os.path.exists(img_file_dir):
            if args.verbose: print(f"Directory, '{img_file_dir}', is missing.")
            if args.dry_run:
                print(f"Directory, '{img_file_dir}', will be created.")
            else:
                os.makedirs(img_file_dir)
        else:
            if args.verbose: print(f"Directory, '{img_file_dir}', exists.")
        if args.dry_run:
            print(f"Copy '{src_img_files[0]}' to '{img_path}' will be done.")
        else:
            with open(img_path,'wb') as dst:
                with open(src_img_files[0],'rb') as src:
                    dst.write(src.read())
            print(f"Copy '{src_img_files[0]}' to '{img_path}' done.")
