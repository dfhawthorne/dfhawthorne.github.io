#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Classify pages as:
# (1) Empty converted pages
# (2) Sub-pages converted pages
# (3) Content converted pages
# (4) Classic unconverted pages
# (5) New unconverted pages
# ------------------------------------------------------------------------------

docs_path="$(dirname $(dirname $(realpath $0)))/docs"
if [[ ! -d "${docs_path}" ]]
then
    printf "%s: directory '%s' does not exist\n" "$0" "${docs_path}" >&2
    exit 1
fi

num_empty_pages=0
num_sub_pages_menus=0
mum_content_pages=0
num_classic_unconv_pages=0
num_new_unconv_pages=0

while read file_name
do
    num_content_lines=$( \
        sed --regexp-extended \
            --expression '/^---$/,/^---$/d' \
            "${file_name}" | \
        wc --lines \
        )
    if [[ ${num_content_lines} -gt 0 ]]
    then
        (( num_content_pages++ ))
        continue
    fi
    grep --quiet \
         --extended-regexp \
         '^sub-pages:' \
         "${file_name}"
    if [[ $? -eq 0 ]]
    then
        (( num_sub_pages_menus++ ))
    else
        (( num_empty_pages++ ))
    fi
done < <(find_converted_web_pages.sh)

while read file_name
do 
    [[ "${file_name}" =~ /_site/ ]] && continue
    [[ "${file_name}" =~ /_includes/ ]] && continue
    [[ "${file_name}" =~ /_layouts/ ]] && continue
    [[ "${file_name}" =~ /google ]] && continue
    [[ "${file_name}" =~ /ASH_report_ ]] && continue
    [[ "${file_name}" =~ /workload_report_ ]] && continue
    case "$(head -n 1 ""${file_name}"")" in
        '---') ;;
        '<meta content="text/html; charset=utf-8" http-equiv="content-type"/>'|'<!DOCTYPE html>'*) 
               (( num_new_unconv_pages++ )) ;;
        *)     (( num_classic_unconv_pages++ )) ;;
    esac
done < <(find "${docs_path}" -name "*.html" -type f)


printf "Empty converted pages:     %6d\n" ${num_empty_pages}
printf "Sub-pages converted pages: %6d\n" ${num_sub_pages_menus}
printf "Content converted pages:   %6d\n" ${num_content_pages}
printf "Classic unconverted pages: %6d\n" ${num_classic_unconv_pages}
printf "New unconverted pages:     %6d\n" ${num_new_unconv_pages}

