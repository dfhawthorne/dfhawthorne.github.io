#!/usr/bin/env python3
# ------------------------------------------------------------------------------
# Fixes Google Sites HTML files with widgets that span multiple lines.
# Simple one-line widget fixes can be found in fix_issue_2.sed
# ------------------------------------------------------------------------------

import argparse
from bs4 import BeautifulSoup

# ------------------------------------------------------------------------------
# Parse arguments
# ------------------------------------------------------------------------------

parser = argparse.ArgumentParser(
        description='Fixes widgets for Google Sites migration'
        )
parser.add_argument('-r','--replace',action='store_true',help='Overwrite input file')
parser.add_argument(
    'input_file',
    nargs=1,
    type=str,
    help='source HTML file'
    )
args = parser.parse_args()

# ------------------------------------------------------------------------------
# Parse the source HTML file
# ------------------------------------------------------------------------------

with open(args.input_file[0], 'r') as f:
    b = f.read()
soup = BeautifulSoup(b, 'html.parser')

# ------------------------------------------------------------------------------
# Remove the sub-pages footer while keeping the 'div' tag
# ------------------------------------------------------------------------------

for div_tag in soup.find_all('div', 'sites-subpages'):
    div_tag.string = ''

# ------------------------------------------------------------------------------
# Clean up scripts
# ------------------------------------------------------------------------------

for script_tag in soup.find_all('script'):
    if script_tag.get('src') is not None:
        pass
    elif script_tag.string is None:
        script_tag.extract()
    elif 'search' in script_tag.string:
        script_tag.extract()

# ------------------------------------------------------------------------------
# Use Google search
# ------------------------------------------------------------------------------

""" search_box = soup.new_tag(
    'form',
     method='get',
     action="https://www.google.com/search")
search_img = soup.new_tag(
    'img',
    src="https://www.google.com/logos/Logo_40wht.gif",
    border="0",
    alt="Google",
    align="middle")
search_box_link = soup.new_tag(
    "a",
    href="https://www.google.com/search")
search_box_link.append(search_img)
attrs = {'type': "text", 'name':"q", 'size':"30", 'maxlength':"255", 'value':""}
search_input_q = soup.new_tag('input', attrs=attrs)
attrs = {'type':"hidden", 'name':"sitesearch", 'value':"dfhawthorne.github.io"}
search_input_sitesearch = soup.new_tag('input', attrs=attrs)
attrs = {'type':"submit", 'name':"sa", 'value':"Search online pages"}
search_input_sa = soup.new_tag('input', attrs=attrs)
search_box.append(search_box_link)
search_box.append(search_input_q)
search_box.append(search_input_sitesearch)
search_box.append(search_input_sa)
search_divs = soup.find_all('td', "sites-layout-searchbox")
search_cells = search_divs[0].find_all('div', "sites-header-cell-buffer-wrapper")
search_cells[0].append(search_box)
 """

# ------------------------------------------------------------------------------
# Remove recent activity widget
# ------------------------------------------------------------------------------

for a_link in soup.find_all('a',"sites-navigation-link"):
    if a_link.string is None: continue
    if 'Recent site activity' in a_link.string:
        a_link.extract()

# ------------------------------------------------------------------------------
# Write out the updated HTML page
# ------------------------------------------------------------------------------

if args.replace:
    with open(args.input_file[0], 'w') as f:
        f.write(soup.prettify())
else:
    print(soup.prettify())