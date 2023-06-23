#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Fixes missing images (issue #6)
# ------------------------------------------------------------------------------

pgm_dir=$(dirname $0)
${pgm_dir}/fix_issue_6.py \
    --img-dir "/home/douglas/Documents/yaocm/sites.google.com/site/yetanotherocmoriginal/_/rsrc/" \
    /home/douglas/Documents/dfhawthorne.github.io/docs \
    >${pgm_dir}/../test/fix_issue_6.log \
    2>${pgm_dir}/../test/fix_issue_6.err
