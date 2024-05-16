#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Finds all PRE tags
# ------------------------------------------------------------------------------

scripts_base=$(dirname $(realpath $0))
docs_base=$(dirname "${scripts_base}")/docs

find "${docs_base}" \
    -regextype posix-extended \
    -type d -name '_*' -prune -false -o \
    -type f -name '*.html' \
        -not -regex '.*/(AWR|ASH|workload)_report_[^/]*.html' \
        -print0 | \
    xargs --null -I@ \
        hxnormalize -x '@' | \
    hxselect -s '\n' pre | \
    sed -nre 's!^<pre style="([^"]*)">.*!\1!p' | \
    sort | \
    uniq -c
