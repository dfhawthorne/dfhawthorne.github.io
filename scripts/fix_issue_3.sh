#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Finds missing pages from newer Google Sites Wiki (issue #3)
# ------------------------------------------------------------------------------

pgm_dir=$(dirname $0)
${pgm_dir}/fix_issue_3.py \
    --wiki-dir "/home/douglas/Documents/YAOCM_new_site/sites.google.com/view/yetanotherocm/" \
    /home/douglas/Documents/dfhawthorne.github.io/docs \
    >${pgm_dir}/../test/fix_issue_3.log \
    2>${pgm_dir}/../test/fix_issue_3.err
