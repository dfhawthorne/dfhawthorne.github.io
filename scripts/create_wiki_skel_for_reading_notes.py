#!/usr/bin/env python3
# ------------------------------------------------------------------------------
# Creates a skeleton of web pages for reading notes within my Wiki.
# ------------------------------------------------------------------------------

import argparse
import os.path
import sys
import time

# ------------------------------------------------------------------------------
# Parse passed arguments
# ------------------------------------------------------------------------------

parser = argparse.ArgumentParser(
    description='Creates a skeleton of web pages for reading notes within my Wiki'
)
parser.add_argument(
    'parm_file',
    nargs=1,
    type=argparse.FileType('r'),
    help='input parameter file'
)
parser.add_argument(
    '-v',
    '--verbose',
    action='store_true'
)
parser.add_argument(
    '-n',
    '--dry-run',
    action='store_true'
)
parser.add_argument(
    '-l',
    '--log',
    default=sys.stdout,
    type=argparse.FileType('w'),
    help='the file where the verbose logging should be written'
)
args = parser.parse_args()

# ------------------------------------------------------------------------------
# Read parameter file
# ------------------------------------------------------------------------------

use_markdown  = False
book_title    = ''
book_topics   = ''
ext_book_url  = ''
book_home_url = ''
book_author   = ''
book_date     = None

exec(args.parm_file[0].read())
args.parm_file[0].close()

book_title_quoted = book_title.replace("'","''")

if args.verbose:
    args.log.write("---------------- Input parameters (START) ----------------\n")
    args.log.write(f"book_title='{book_title}'\nbook_topics='{book_topics}'\n")
    args.log.write(f"ext_book_url='{ext_book_url}'\nwiki_url='{book_home_url}'\n")
    args.log.write(f"book_author='{book_author}'\nbook_date='{book_date}'\n")
    args.log.write(f"use_markdown={use_markdown}\n")
    args.log.write("----------------- Input parameters (END) -----------------\n")

# ------------------------------------------------------------------------------
# Build translation table for converting text to a file name
# - Removes characters other than white space, letters, and digits
# - Changes white space to a dash ('-')
# - Leaves letters and digits unchanged
# ------------------------------------------------------------------------------

trans_dict = dict()
for byte in str(bytes([b for b in range(256)])):
    if byte.isalnum(): continue
    if byte.isspace():
        trans_dict[byte] = '-'
    else:
        trans_dict[byte] = None # removes character

trans_table = str.maketrans(trans_dict)

# ------------------------------------------------------------------------------
# Discover Wiki location
# - assumes that the script and wiki directories are siblings
# ------------------------------------------------------------------------------

script_dir = os.path.dirname(os.path.realpath(__file__))
wiki_dir   = os.path.join(os.path.dirname(script_dir),'docs')

if args.verbose:
    args.log.write(f"script_dir='{script_dir}'\nwiki_dir='{wiki_dir}'\n")

# ------------------------------------------------------------------------------
# Build YAML Header for book home page
# ------------------------------------------------------------------------------

book_home_page_content  =  "---\n"                            + \
                           "layout: default\n"                + \
                          f"title: '{book_title_quoted}'\n"   + \
                          f"base-url: {book_home_url}\n"      + \
                           "breadcrumbs:\n"                   + \
                           "- title: Home\n"                  + \
                           "  url: index.html\n"              + \
                           "- title: Reading Notes\n"         + \
                           "  url: home/reading-notes.html\n" + \
                           "sub-pages-title: Chapters\n"      + \
                           "sub-pages:\n"            

if args.verbose:
    args.log.write("------------------ HEADER (START) ----------------------\n")
    args.log.write(book_home_page_content)
    args.log.write("------------------- HEADER (END) -----------------------\n")

# ------------------------------------------------------------------------------
# Create directory for book objective anchor pages
# ------------------------------------------------------------------------------

book_home_page_full_path_name = os.path.join(
                                    wiki_dir,
                                    book_home_url
                                )
book_home_dir_full_path_name  = os.path.join(
                                    wiki_dir,
                                    book_home_url.removesuffix('.html')
                                )
if os.path.isfile(book_home_page_full_path_name):
    error_msg = f"Error: book home page, '{book_home_page_full_path_name}', already exists."
    if args.verbose:
        args.log.write(error_msg + '\n')
    print(error_msg, file=sys.stderr)
    exit(1)
if os.path.isdir(book_home_dir_full_path_name):
    error_msg = f"Error: book home directory, '{book_home_dir_full_path_name}', already exists."
    if args.verbose:
        args.log.write(error_msg + '\n')
    print(error_msg, file=sys.stderr)
    exit(1)
else:
    if args.dry_run:
        dry_run_msg = f"DRY-RUN: book home directory, '{book_home_dir_full_path_name}', will be created."
        if args.verbose:
            args.log.write(dry_run_msg + '\n')
        print(dry_run_msg)
    else:
        if args.verbose:
            args.log.write(f"book home directory, '{book_home_dir_full_path_name}', created.\n")
        os.mkdir(book_home_dir_full_path_name)

# ------------------------------------------------------------------------------
# Populate table with book objectives and topics
# ------------------------------------------------------------------------------

book_obj_page_content = None
for line in book_topics.split('\n'):
    if len(line.strip()) == 0: continue
    if args.verbose:
        args.log.write(f"line='{line}'\n")
    if line.startswith(' '):
        book_topic_text      = line.strip()
        book_topic_page_name = book_topic_text.lower().translate(trans_table) + \
                               '.html'
        book_topic_url       = os.path.join(
                                    book_home_url.removesuffix('.html'),
                                    book_obj_dir_name,
                                    book_topic_page_name
                                    )
        if use_markdown:
            book_topic_full_path_name = os.path.join(
                                        book_home_dir_full_path_name,
                                        book_obj_dir_name,
                                        book_topic_page_name.removesuffix('.html')+'.md'
                                        )
        else:
            book_topic_full_path_name = os.path.join(
                                        book_home_dir_full_path_name,
                                        book_obj_dir_name,
                                        book_topic_page_name
                                        )
        book_topic_text_quoted    = book_topic_text.replace("'","''")
        if args.verbose:
            args.log.write(f"book_topic_text           = '{book_topic_text}'\n")
            args.log.write(f"book_topic_full_path_name = '{book_topic_full_path_name}'\n")
            args.log.write(f"book_topic_page_name      = '{book_topic_page_name}'\n")
            args.log.write(f"book_topic_url            = '{book_topic_url}'\n")
        book_home_page_content += f'  - url: {book_topic_url}\n'           + \
                                  f"    title: '{book_topic_text_quoted}'\n"
        book_obj_page_content  += f"- title: '{book_topic_text_quoted}'\n" + \
                                  f"  url: {book_topic_url}\n"
        book_topic_page_content =  "---\n" + \
                                   "layout: default\n"                     + \
                                  f"title: '{book_topic_text_quoted}'\n"   + \
                                  f"base-url: {book_topic_url}\n"          + \
                                   "breadcrumbs:\n"                        + \
                                   "- title: Home\n"                       + \
                                   "  url: index.html\n"                   + \
                                   "- title: Reading Notes\n"              + \
                                   "  url: home/reading-notes.html\n"      + \
                                  f"- title: '{book_title_quoted}'\n"      + \
                                  f"  url: {book_home_url}\n"              + \
                                  f"- title: '{book_obj_text_quoted}'\n"   + \
                                  f"  url: {book_obj_url}\n"               + \
                                   "---\n"
        if os.path.isfile(book_topic_full_path_name):
            error_msg = f"ERROR: book topic page ('{book_topic_full_path_name}') already exists."
            if args.verbose:
                args.log.write(error_msg + '\n')
            print(error_msg, file=sys.stderr)
            exit(1)
        else:
            if args.dry_run:
                dry_run_msg = f"DRY-RUN: book topic content written to '{book_topic_full_path_name}'"
                if args.verbose:
                    args.log.write(dry_run_msg + '\n')
                print(dry_run_msg)
            else:
                if args.verbose:
                    args.log.write(f"book topic content written to '{book_topic_full_path_name}'\n")
                with open(book_topic_full_path_name, 'x') as f:
                    f.write(book_topic_page_content)
    else:
        if book_obj_page_content is not None:
            book_obj_page_content += '---\n'
            if args.verbose:
                args.log.write("------------------ book OBJ CONTENT (START) ----------------------\n")
                args.log.write(book_obj_page_content)
                args.log.write("------------------- book OBJ CONTENT (END) -----------------------\n")
            if args.dry_run:
                dry_run_msg = f"DRY-RUN: book objective content written to '{book_obj_page_full_path_name}'"
                if args.verbose:
                    args.log.write(dry_run_msg + '\n')
                print(dry_run_msg)
            else:
                if args.verbose:
                    args.log.write(f"book objective content written to '{book_obj_page_full_path_name}'\n")
                with open(book_obj_page_full_path_name, 'x') as f:
                    f.write(book_obj_page_content)
        book_obj_text                = line.strip()
        book_obj_text_quoted         = book_obj_text.replace("'","''")
        book_obj_dir_name            = book_obj_text.lower().translate(trans_table)
        book_obj_page_name           = book_obj_dir_name + '.html'
        book_obj_url                 = os.path.join(
                                            book_home_url.removesuffix('.html'),
                                            book_obj_page_name
                                            )
        if use_markdown:
            book_obj_page_full_path_name = os.path.join(wiki_dir,book_obj_url.removesuffix('.html')+'.md')
        else:
            book_obj_page_full_path_name = os.path.join(wiki_dir,book_obj_url)
        book_obj_dir_full_path_name  = os.path.join(book_home_dir_full_path_name,book_obj_dir_name)
        if args.verbose:
            args.log.write(f"book_obj_text                = '{book_obj_text}'\n")
            args.log.write(f"book_obj_dir_name            = '{book_obj_dir_name}'\n")
            args.log.write(f"book_obj_url                 = '{book_obj_url}'\n")
            args.log.write(f"book_obj_page_name           = '{book_obj_page_name}'\n")
            args.log.write(f"book_obj_page_full_path_name = '{book_obj_page_full_path_name}'\n")
            args.log.write(f"book_obj_dir_full_path_name  = '{book_obj_dir_full_path_name}'\n")
        if os.path.isdir(book_obj_dir_full_path_name):
            error_msg = f"ERROR: book objective directory ('{book_obj_dir_full_path_name}')"
            if args.verbose:
                args.log.write(error_msg + '\n')
            print(error_msg, file=sys.stderr)
            exit(1)
        else:
            if args.dry_run:
                dry_run_msg = f"DRY-RUN: book objective directory ('{book_obj_dir_full_path_name}') created."
                if args.verbose:
                    args.log.write(dry_run_msg + '\n')
                print(dry_run_msg)
            else:
                if args.verbose:
                    args.log.write(f"book objective directory ('{book_obj_dir_full_path_name}') created.\n")
                os.mkdir(book_obj_dir_full_path_name)
        if os.path.isfile(book_obj_page_full_path_name):
            error_msg = f"ERROR: book objective page ('{book_obj_page_full_path_name}') already exists."
            if args.verbose:
                args.log.write(error_msg + '\n')
            print(error_msg, file=sys.stderr)
            exit(1)
        book_obj_text_quoted  = book_obj_text.replace("'","''")
        book_obj_page_content =  "---\n"                               + \
                                 "layout: default\n"                   + \
                                f"title: '{book_obj_text_quoted}'\n"   + \
                                f"base-url: {book_obj_url}\n"          + \
                                 "breadcrumbs:\n"                      + \
                                 "- title: Home\n"                     + \
                                 "  url: index.html\n"                 + \
                                 "- title: Reading Notes\n"            + \
                                 "  url: home/reading-notes.html\n"    + \
                                f"- title: '{book_title_quoted}'\n"    + \
                                f"  url: {book_home_url}\n"            + \
                                 "sub-pages-title: 'Chapters'\n"       + \
                                 "sub-pages:\n"
        book_home_page_content += f'- url: {book_obj_url}\n'           + \
                                  f"  title: '{book_obj_text_quoted}'\n" + \
                                   '  sub-pages:\n'

if book_obj_page_content is not None:
    book_obj_page_content += '---\n'
    if args.verbose:
        args.log.write("------------------ book OBJ CONTENT (START) ----------------------\n")
        args.log.write(book_obj_page_content)
        args.log.write("------------------- book OBJ CONTENT (END) -----------------------\n")
    if args.dry_run:
        dry_run_msg = f"DRY-RUN: book objective content written to '{book_obj_page_full_path_name}'"
        if args.verbose:
            args.log.write(dry_run_msg + '\n')
        print(dry_run_msg)
    else:
        if args.verbose:
            args.log.write(f"book objective content written to '{book_obj_page_full_path_name}'\n")
        with open(book_obj_page_full_path_name, 'x') as f:
            f.write(book_obj_page_content)

# ------------------------------------------------------------------------------
# book epilogue
# ------------------------------------------------------------------------------

book_home_page_content += f"""
---

<p>My reading notes for <a href="{ext_book_url}">{book_title}</a> by {book_author} ({book_date}).</p>
"""

if args.verbose:
    args.log.write( "------------- book Home Page Content (START) ----------------\n")
    args.log.write(f"book_home_page_content='{book_home_page_content}'\n")
    args.log.write( "-------------- book Home Page Content (END) -----------------\n")

if args.dry_run:
    dry_run_msg = f"DRY-RUN: book Home Page content written to '{book_home_page_full_path_name}'"
    if args.verbose:
        args.log.write(dry_run_msg + '\n')
    print(dry_run_msg)
else:
    if args.verbose:
        args.log.write(f"book Home Page content written to '{book_home_page_full_path_name}'\n")
    with open(book_home_page_full_path_name, 'x') as f:
        f.write(book_home_page_content)
