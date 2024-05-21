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

exam_title    = ''
exam_topics   = ''
ext_exam_url  = ''
exam_home_url = ''

exec(args.parm_file[0].read())
args.parm_file[0].close()

exam_title_quoted = exam_title.replace("'","''")

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

exam_home_page_content  =  "---\n"                          + \
                           "layout: default\n"              + \
                          f"title: '{exam_title_quoted}'\n" + \
                          f"base-url: {exam_home_url}\n"    + \
                           "breadcrumbs:\n"                 + \
                           "- title: Home\n"                + \
                           "  url: index.html\n"            + \
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

exam_home_page_full_path_name = os.path.join(
                                    wiki_dir,
                                    exam_home_url
                                )
exam_home_dir_full_path_name  = os.path.join(
                                    wiki_dir,
                                    exam_home_url.removesuffix('.html')
                                )
if os.path.isfile(exam_home_page_full_path_name):
    error_msg = f"Error: Exam home page, '{exam_home_page_full_path_name}', already exists."
    if args.verbose:
        args.log.write(error_msg + '\n')
    print(error_msg, file=sys.stderr)
    exit(1)
if os.path.isdir(exam_home_dir_full_path_name):
    error_msg = f"Error: Exam home directory, '{exam_home_dir_full_path_name}', already exists."
    if args.verbose:
        args.log.write(error_msg + '\n')
    print(error_msg, file=sys.stderr)
    exit(1)
else:
    if args.dry_run:
        dry_run_msg = f"DRY-RUN: Exam home directory, '{exam_home_dir_full_path_name}', will be created."
        if args.verbose:
            args.log.write(dry_run_msg + '\n')
        print(dry_run_msg)
    else:
        if args.verbose:
            args.log.write(f"Exam home directory, '{exam_home_dir_full_path_name}', created.\n")
        os.mkdir(exam_home_dir_full_path_name)

# ------------------------------------------------------------------------------
# Populate table with exam objectives and topics
# ------------------------------------------------------------------------------

exam_obj_page_content = None
for line in exam_topics.split('\n'):
    if len(line.strip()) == 0: continue
    if args.verbose:
        args.log.write(f"line='{line}'\n")
    if line.startswith(' '):
        exam_topic_text      = line.strip()
        exam_topic_page_name = exam_topic_text.lower().translate(trans_table) + \
                               '.html'
        exam_topic_url       = os.path.join(
                                    exam_home_url.removesuffix('.html'),
                                    exam_obj_dir_name,
                                    exam_topic_page_name
                                    )
        exam_topic_full_path_name = os.path.join(
                                    exam_home_dir_full_path_name,
                                    exam_obj_dir_name,
                                    exam_topic_page_name
                                    )
        exam_topic_text_quoted    = exam_topic_text.replace("'","''")
        if args.verbose:
            args.log.write(f"exam_topic_text           = '{exam_topic_text}'\n")
            args.log.write(f"exam_topic_full_path_name = '{exam_topic_full_path_name}'\n")
            args.log.write(f"exam_topic_page_name      = '{exam_topic_page_name}'\n")
            args.log.write(f"exam_topic_url            = '{exam_topic_url}'\n")
        exam_home_page_content +=  '<tr><td>'                              + \
                                  f'<a href="{exam_topic_url}">'           + \
                                  f'{exam_topic_text}</a></td>'            + \
                                   '<td class="exam-rating-1">1</td>'      + \
                                   '<td></td></tr>\n'
        exam_obj_page_content  += f"- title: '{exam_topic_text_quoted}'\n" + \
                                  f"  url: {exam_topic_url}\n"
        exam_topic_page_content =  "---\n" + \
                                   "layout: default\n"                     + \
                                  f"title: '{exam_topic_text_quoted}'\n"   + \
                                  f"base-url: {exam_topic_url}\n"          + \
                                   "breadcrumbs:\n"                        + \
                                   "- title: Home\n"                       + \
                                   "  url: index.html\n"                   + \
                                  f"- title: '{exam_title_quoted}'\n"      + \
                                  f"  url: {exam_home_url}\n"              + \
                                  f"- title: '{exam_obj_text_quoted}'\n"   + \
                                  f"  url: {exam_obj_url}\n"               + \
                                   "---\n"
        if os.path.isfile(exam_topic_full_path_name):
            error_msg = f"ERROR: Exam topic page ('{exam_topic_full_path_name}') already exists."
            if args.verbose:
                args.log.write(error_msg + '\n')
            print(error_msg, file=sys.stderr)
            exit(1)
        else:
            if args.dry_run:
                dry_run_msg = f"DRY-RUN: Exam topic content written to '{exam_topic_full_path_name}'"
                if args.verbose:
                    args.log.write(dry_run_msg + '\n')
                print(dry_run_msg)
            else:
                if args.verbose:
                    args.log.write(f"Exam topic content written to '{exam_topic_full_path_name}'\n")
                with open(exam_topic_full_path_name, 'x') as f:
                    f.write(exam_topic_page_content)
    else:
        if exam_obj_page_content is not None:
            exam_obj_page_content += '---\n'
            if args.verbose:
                args.log.write("------------------ EXAM OBJ CONTENT (START) ----------------------\n")
                args.log.write(exam_obj_page_content)
                args.log.write("------------------- EXAM OBJ CONTENT (END) -----------------------\n")
            if args.dry_run:
                dry_run_msg = f"DRY-RUN: Exam objective content written to '{exam_obj_page_full_path_name}'"
                if args.verbose:
                    args.log.write(dry_run_msg + '\n')
                print(dry_run_msg)
            else:
                if args.verbose:
                    args.log.write(f"Exam objective content written to '{exam_obj_page_full_path_name}'\n")
                with open(exam_obj_page_full_path_name, 'x') as f:
                    f.write(exam_obj_page_content)
        exam_obj_text                = line.strip()
        exam_obj_text_quoted         = exam_obj_text.replace("'","''")
        exam_obj_dir_name            = exam_obj_text.lower().translate(trans_table)
        exam_obj_page_name           = exam_obj_dir_name + '.html'
        exam_obj_url                 = os.path.join(
                                            exam_home_url.removesuffix('.html'),
                                            exam_obj_page_name
                                            )
        exam_obj_page_full_path_name = os.path.join(wiki_dir,exam_obj_url)
        exam_obj_dir_full_path_name  = os.path.join(exam_home_dir_full_path_name,exam_obj_dir_name)
        if args.verbose:
            args.log.write(f"exam_obj_text                = '{exam_obj_text}'\n")
            args.log.write(f"exam_obj_dir_name            = '{exam_obj_dir_name}'\n")
            args.log.write(f"exam_obj_url                 = '{exam_obj_url}'\n")
            args.log.write(f"exam_obj_page_name           = '{exam_obj_page_name}'\n")
            args.log.write(f"exam_obj_page_full_path_name = '{exam_obj_page_full_path_name}'\n")
            args.log.write(f"exam_obj_dir_full_path_name  = '{exam_obj_dir_full_path_name}'\n")
        if os.path.isdir(exam_obj_dir_full_path_name):
            error_msg = f"ERROR: Exam objective directory ('{exam_obj_dir_full_path_name}')"
            if args.verbose:
                args.log.write(error_msg + '\n')
            print(error_msg, file=sys.stderr)
            exit(1)
        else:
            if args.dry_run:
                dry_run_msg = f"DRY-RUN: Exam objective directory ('{exam_obj_dir_full_path_name}') created."
                if args.verbose:
                    args.log.write(dry_run_msg + '\n')
                print(dry_run_msg)
            else:
                if args.verbose:
                    args.log.write(f"Exam objective directory ('{exam_obj_dir_full_path_name}') created.\n")
                os.mkdir(exam_obj_dir_full_path_name)
        if os.path.isfile(exam_obj_page_full_path_name):
            error_msg = f"ERROR: Exam objective page ('{exam_obj_page_full_path_name}') already exists."
            if args.verbose:
                args.log.write(error_msg + '\n')
            print(error_msg, file=sys.stderr)
            exit(1)
        exam_obj_text_quoted  = exam_obj_text.replace("'","''")
        exam_obj_page_content =  "---\n"                               + \
                                 "layout: default\n"                   + \
                                f"title: '{exam_obj_text_quoted}'\n"   + \
                                f"base-url: {exam_obj_url}\n"          + \
                                 "breadcrumbs:\n"                      + \
                                 "- title: Home\n"                     + \
                                 "  url: index.html\n"                 + \
                                f"- title: '{exam_title_quoted}'\n"    + \
                                f"  url: {exam_home_url}\n"            + \
                                 "sub-pages-title: 'Exam Topics'\n"    + \
                                 "sub-pages:\n"
        exam_home_page_content += f'<tr><td colspan="3" class="exam-objective">'          + \
                                  f'<a href="{exam_obj_url}">{exam_obj_text}</a></td></tr>\n'

if exam_obj_page_content is not None:
    exam_obj_page_content += '---\n'
    if args.verbose:
        args.log.write("------------------ EXAM OBJ CONTENT (START) ----------------------\n")
        args.log.write(exam_obj_page_content)
        args.log.write("------------------- EXAM OBJ CONTENT (END) -----------------------\n")
    if args.dry_run:
        dry_run_msg = f"DRY-RUN: Exam objective content written to '{exam_obj_page_full_path_name}'"
        if args.verbose:
            args.log.write(dry_run_msg + '\n')
        print(dry_run_msg)
    else:
        if args.verbose:
            args.log.write(f"Exam objective content written to '{exam_obj_page_full_path_name}'\n")
        with open(exam_obj_page_full_path_name, 'x') as f:
            f.write(exam_obj_page_content)

exam_home_page_content += "</tbody></table>"

if args.verbose:
    args.log.write( "------------- Exam Home Page Content (START) ----------------\n")
    args.log.write(f"exam_home_page_content='{exam_home_page_content}'\n")
    args.log.write( "-------------- Exam Home Page Content (END) -----------------\n")

if args.dry_run:
    dry_run_msg = f"DRY-RUN: Exam Home Page content written to '{exam_home_page_full_path_name}'"
    if args.verbose:
        args.log.write(dry_run_msg + '\n')
    print(dry_run_msg)
else:
    if args.verbose:
        args.log.write(f"Exam Home Page content written to '{exam_home_page_full_path_name}'\n")
    with open(exam_home_page_full_path_name, 'x') as f:
        f.write(exam_home_page_content)
