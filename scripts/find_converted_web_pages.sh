#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Lists all file names in the docs directory (excluding the _site sub-directory)
# that have been converted to the Jekyll format.
# Assumes that the scripts and docs sub-directories are siblings.
# ------------------------------------------------------------------------------

docs_path="$(dirname $(dirname $(realpath $0)))/docs"

while read file_name
do 
    echo "${file_name}" | grep -qE '/_site/'
    [[ $? -eq 0 ]] && continue
    head -n 1 "${file_name}" | grep -qE '^---$'
    [[ $? -eq 0 ]] && printf "%s\n" "${file_name}"
done < <(find "${docs_path}" -name "*.html" -type f)
