#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Lists all file names in the docs directory (excluding the _site sub-directory)
# that have been converted to the Jekyll format.
# Assumes that the scripts and docs sub-directories are siblings.
# ------------------------------------------------------------------------------

docs_path="$(dirname $(dirname $(realpath $0)))/docs"

while read file_name
do 
    [[ "${file_name}" =~ /_site/ ]] && continue
    [[ "$(head -n 1 ""${file_name}"")" == '---' ]] && \
        printf "%s\n" "${file_name}"
done < <(find "${docs_path}" -name "*.html" -type f)

exit 0
