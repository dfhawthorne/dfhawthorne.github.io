#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Script to do changes to fix issue #2
# ------------------------------------------------------------------------------

pushd ~/Documents/dfhawthorne.github.io/docs

# ------------------------------------------------------------------------------
# Update HTML files to point to away from _/rsrc
# ------------------------------------------------------------------------------

while read file_name
do
    sed -i \
        -e 's!https://sites.google.com/site/yetanotherocmoriginal/!https://dfhawthorne.github.io/!g' \
        -e 's!"/site/yetanotherocmoriginal/!"/!g' \
        -e 's!"/site/yetanotherocmoriginal"!"/"!g' \
        -e 's!_/rsrc/[0-9][0-9]*/!!g' \
        "${file_name}"
done < <(find . -type f -name "*.html")

# ------------------------------------------------------------------------------
# Move files from _/rsrc
# ------------------------------------------------------------------------------

while read file_name
do 
    new_file_name=$(echo "${file_name}" | sed -e 's!_/rsrc/[0-9][0-9]*/!!g')
    dir_name=$(dirname "${new_file_name}")
    if [[ -d "${dir_name}" ]]
    then
        [[ ! -f "${new_file_name}" || "${file_name}" -nt "${new_file_name}" ]] && \ 
            git mv -f "${file_name}" "${new_file_name}"
        [[ -f "${new_file_name}" ]] && \
            git rm -f "${file_name}"
    fi
done < <(find _ -type f)

# ------------------------------------------------------------------------------
# Remove empty directories from _/rsrc
# ------------------------------------------------------------------------------

for dir in _/rsrc/*
do
    count=$(find "${dir}" -type f | wc -l)
    [[ ${count} -eq 0 ]] && \
        git rm -f -r "${dir}"
done

popd 

