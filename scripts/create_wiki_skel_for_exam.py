#!/usr/bin/env python3
# ------------------------------------------------------------------------------
# Creates a skeleton of web pages for an examination within my Wiki.
# ------------------------------------------------------------------------------

import argparse
import os.path
import sys
import time

# ------------------------------------------------------------------------------
# Parse passed arguments
# ------------------------------------------------------------------------------

parser = argparse.ArgumentParser(
    description='Creates a skeleton of web pages for an examination within my Wiki'
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

exam_title   = ''
exam_topics  = ''
ext_exam_url = ''
exam_home_url     = ''

exec(args.parm_file[0].read())
args.parm_file[0].close()

if args.verbose:
    args.log.write("---------------- Input parameters (START) ----------------\n")
    args.log.write(f"exam_title='{exam_title}'\nexam_topics='{exam_topics}'\n")
    args.log.write(f"ext_exam_url='{ext_exam_url}'\nwiki_url='{exam_home_url}'\n")
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
# Build YAML Header for Exam home page
# ------------------------------------------------------------------------------

exam_home_page_content  =  "---\n"                       + \
                           "layout: default\n"           + \
                          f"title: '{exam_title}'\n"     + \
                          f"base-url: {exam_home_url}\n" + \
                           "breadcrumbs:\n"              + \
                           "- title: Home\n"             + \
                           "  url: index.html\n"         + \
                           "---\n"

if args.verbose:
    args.log.write("------------------ HEADER (START) ----------------------\n")
    args.log.write(exam_home_page_content)
    args.log.write("------------------- HEADER (END) -----------------------\n")

# ------------------------------------------------------------------------------
# Exam prologue
# ------------------------------------------------------------------------------

date_visited = time.strftime('%Y-%m-%d')
exam_home_page_content += f"""
    <p>Based on the <a href="{ext_exam_url}">{exam_title}</a> (visited
    {date_visited}). I rate myself as follows (1=poor to 5=good).</p>
    <table border="1">
      <thead>
        <tr><th>Exam Topic</th><th>My Rating (1-5)</th><th>Reference</th></tr>
      </thead>
      <tbody>
"""

# ------------------------------------------------------------------------------
# Create directory for exam objective anchor pages
# ------------------------------------------------------------------------------

if os.path.isfile(os.path.join(wiki_dir,exam_home_url)):
    error_msg = f"Error: '{os.path.join(wiki_dir,exam_home_url)}' already exists."
    if args.verbose:
        args.log.write(error_msg + '\n')
    print(error_msg, file=sys.stderr)
    exit(1)

# ------------------------------------------------------------------------------
# Populate table with exam topics
# ------------------------------------------------------------------------------

exam_obj_page_content = None
for line in exam_topics.split('\n'):
    if len(line.strip()) == 0: continue
    if args.verbose:
        args.log.write(f"line='{line}'\n")
    if line.startswith(' '):
        topic_text      = line.strip()
        topic_page_name = topic_text.lower().translate(trans_table) + '.html'
        topic_url       = os.path.join(exam_home_url,exam_obj_dir_name,topic_page_name)
        if args.verbose:
            args.log.write(f"topic_text      = '{topic_text}'\n")
            args.log.write(f"topic_page_name = '{topic_page_name}'\n")
            args.log.write(f"topic_url       = '{topic_url}'\n")
        exam_home_page_content +=  '<tr><td>'                         + \
                                  f'<a href="{topic_url}">'           + \
                                  f'{topic_text}</td>'                + \
                                   '<td class="exam-rating-1">1</td>' + \
                                   '<td></td></tr>\n'
        exam_obj_page_content  += f"- title: '{topic_text}'\n"        + \
                                  f"  url: {topic_url}\n"
    else:
        if exam_obj_page_content is not None:
            exam_obj_page_content += '---\n'
            if args.verbose:
                args.log.write("------------------ EXAM OBJ CONTENT (START) ----------------------\n")
                args.log.write(exam_obj_page_content)
                args.log.write("------------------- EXAM OBJ CONTENT (END) -----------------------\n")
            if args.dry_run:
                dry_run_msg = f"DRY-RUN: Content written to '{os.path.join(wiki_dir,exam_obj_url)}'"
                if args.verbose:
                    args.log.write(dry_run_msg + '\n')
                print(dry_run_msg)
            else:
                pass # TODO
        exam_obj_text      = line.strip()
        exam_obj_dir_name  = exam_obj_text.lower().translate(trans_table)
        exam_obj_page_name = exam_obj_dir_name + '.html'
        exam_obj_url       = os.path.join(exam_home_url,exam_obj_page_name)
        if args.verbose:
            args.log.write(f"exam_obj_text      = '{exam_obj_text}'\n")
            args.log.write(f"exam_obj_dir_name  = '{exam_obj_dir_name}'\n")
            args.log.write(f"exam_obj_page_name = '{exam_obj_page_name}'\n")
            args.log.write(f"exam_obj_url       = '{exam_obj_url}'\n")
        if os.path.isfile(os.path.join(wiki_dir,exam_obj_url)):
            error_msg = f"ERROR: Exam objective page ('{os.path.join(wiki_dir,exam_obj_url)}') already exists."
            if args.verbose:
                args.log.write(error_msg + '\n')
            print(error_msg, file=sys.stderr)
            exit(1)
        exam_obj_page_content =  "---\n"                               + \
                                 "layout: default\n"                   + \
                                f"title: '{exam_obj_text}'\n"          + \
                                f"base-url: {exam_obj_url}\n"          + \
                                 "breadcrumbs:\n"                      + \
                                 "- title: Home\n"                     + \
                                 "  url: index.html\n"                 + \
                                f"- title: '{exam_title}'\n"           + \
                                f"  url: {exam_home_url}\n"            + \
                                 "sub-pages-title: 'Exam Topics'\n"    + \
                                 "sub-pages:\n"
        exam_home_page_content += f'<tr><td colspan="3"><a href="{exam_obj_url}">{exam_obj_text}</td></tr>\n'

exam_home_page_content += "</tbody></table>"


if args.verbose:
    args.log.write( "------------------- Content (START) --------------------\n")
    args.log.write(f"exam_home_page_content='{exam_home_page_content}'\n")
    args.log.write( "-------------------- Content (END) ---------------------\n")
