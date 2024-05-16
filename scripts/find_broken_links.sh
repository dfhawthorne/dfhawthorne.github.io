#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Lists all file names in the docs directory (excluding the _site sub-directory)
# that have been converted to the Jekyll format.
# Assumes that the scripts and docs sub-directories are siblings.
# ------------------------------------------------------------------------------

docs_path="$(dirname $(dirname $(realpath $0)))/docs"

while read file_name
do 
    [[ ! -f "${docs_path}/${file_name}" ]] && \
        printf "%s\n" "${file_name}"
done < <( \
    find "${docs_path}" \
        -regextype posix-extended -a \
        -type d -a \
            -regex '.*/(_|\.).*' -a \
            -prune -a \
            -false -o \
        -name "*.html" -a \
            -type f -a \
            -not -regex '.*/(google|((ASH|AWR|workload)_report_))[^/]*.html$' -a \
            -print0 | \
            xargs --null -I@ hxnormalize -xdL '@' 2>/dev/null | \
            hxselect -s '\n' a | \
            sed -nre 's!^<a[ ]+href="/?(home/[^"#]*).*!\1!p' | \
            sort -u \
        )

exit 0
