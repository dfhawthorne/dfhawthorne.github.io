#!/usr/bin/env bash

docs_path="$(dirname $(dirname $(realpath $0)))/docs"
if [[ ! -d "${docs_path}" ]]
then
    printf "%s: directory '%s' does not exist\n" "$0" "${docs_path}" >&2
    exit 1
fi

while read file_name
do 
    [[ "${file_name}" =~ /_site/ ]] && continue
    [[ "${file_name}" =~ /_includes/ ]] && continue
    [[ "${file_name}" =~ /_layouts/ ]] && continue
    [[ "${file_name}" =~ /google ]] && continue
    case "$(head -n 1 ""${file_name}"")" in
        '---') ;;
        '<meta content="text/html; charset=utf-8" http-equiv="content-type"/>'|'<!DOCTYPE html>'*) 
               ;;
        *)     printf "${file_name}\n" ;;
    esac
done < <(find "${docs_path}" -name "*.html" -type f)
