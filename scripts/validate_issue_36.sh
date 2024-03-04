#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Validate unconverted pages for issue #36 (11G OCM)
# ------------------------------------------------------------------------------

for f in $(find_unconverted_web_pages.sh | grep 11g-ocm)
do
    n=$(basename $f .html)
    convert_web_page.py -vl /tmp/${n}.log $f >/tmp/${n}.html
    if [[ $? -ne 0 ]]
    then
        printf "%s failed\n" "${f}"
    fi
done
