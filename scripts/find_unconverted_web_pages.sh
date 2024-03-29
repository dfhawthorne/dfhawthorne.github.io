#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Lists all file names in the docs directory (excluding the _site sub-directory)
# that have not been converted to the Jekyll format.
# Assumes that the scripts and docs sub-directories are siblings.
# ------------------------------------------------------------------------------

docs_path="$(dirname $(dirname $(realpath $0)))/docs"

while read file_name
do 
    [[ "${file_name}" =~ /_site/ ]] && continue
    case "$(head -n 1 ""${file_name}"")" in
        '---') ;;
        '<meta content="text/html; charset=utf-8" http-equiv="content-type"/>') ;;
        *)     printf "%s\n" "${file_name}" ;;
    esac
done < <(find "${docs_path}" -name "*.html" -type f)

exit 0
