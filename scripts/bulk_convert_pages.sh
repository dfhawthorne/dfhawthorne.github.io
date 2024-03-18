#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Convert all pages in current directory
# ------------------------------------------------------------------------------

for f in *.html
do echo $f
   l=$(basename $f .html)
   convert_web_page.py -rgvl /tmp/${l}.log $f
done
