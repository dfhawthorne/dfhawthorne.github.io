#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Convert any unconverted pages for issue #36 (11G OCM)
# ------------------------------------------------------------------------------

for f in $(find_unconverted_web_pages.sh | grep 11g-ocm)
do
    echo $f
    n=$(basename $f .html)
    convert_web_page.py -rg $f
    if [[ $? -ne 0 ]]
    then
        echo Failed
    fi
done
