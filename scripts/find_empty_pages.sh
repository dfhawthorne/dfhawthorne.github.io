#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Find all empty pages that have been converted
# ------------------------------------------------------------------------------

test_dir="$(dirname $(dirname $(realpath $0)))/test"
if [[ ! -d "${test_dir}" ]]
then
    printf "%s: directory '%s' does not exist\n" "$0" "${test_dir}" >&2
    exit 1
fi
base_dir="$(dirname $(dirname $(realpath $0)))/docs"
if [[ ! -d "${base_dir}" ]]
then
    printf "%s: directory '%s' does not exist\n" "$0" "${base_dir}" >&2
    exit 1
fi
empty_pages_fn="${test_dir}/empty_pages.dat"
empty_page_addr_fn="${test_dir}/empty_page_addr.dat"
cp /dev/null "${empty_pages_fn}"
cp /dev/null "${empty_page_addr_fn}"

while read file_name
do
    num_content_lines=$( \
        sed --regexp-extended \
            --expression '/^---$/,/^---$/d' \
            "${file_name}" | \
        wc --lines \
        )
    [[ ${num_content_lines} -gt 0 ]] && continue
    grep --quiet \
         --extended-regexp \
         '^sub-pages:' \
         "${file_name}"
    [[ $? -eq 0 ]] && continue
    printf 'href="%s"\n' "${file_name}" >> "${empty_page_addr_fn}"
    printf '%s\n' "${file_name}" >> "${empty_pages_fn}"
done < <(find_converted_web_pages.sh)

for edit_file in "${empty_pages_fn}" "${empty_page_addr_fn}"
do  sed --in-place \
        --regexp-extended \
        --expression "s!${base_dir}/!!" \
        "${edit_file}"
done

printf "Web Pages With No Content That Are Not Sub-pages Menus\n"
printf "======================================================\n\n"

cat "${empty_pages_fn}"

printf "\nWeb Pages With References To Empty Web Pages\n"
printf   "============================================\n\n"

find_converted_web_pages.sh | \
    xargs --max-args=1 \
        grep --files-with-matches \
             --file="${empty_page_addr_fn}" | \
    sed --regexp-extended \
        --expression "s!${base_dir}/!!" \
