#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Script to do changes to fix issue #2
# ------------------------------------------------------------------------------

pushd ~/Documents/dfhawthorne.github.io/docs

while read file_name
do
    sed -i \
        -e 's!https://sites.google.com/site/yetanotherocmoriginal/!https://dfhawthorne.github.io/!g' \
        -e 's!"/site/yetanotherocmoriginal/!"/!g' \
        -e 's!"/site/yetanotherocmoriginal"!"/"!g' \
        -e 's!_/rsrc/[0-9][0-9]*/!!g' \
        "${file_name}"
done < <(find . -type f -name "*.html")

while read file_name
do 
    new_file_name=$(echo "${file_name}" | sed -e 's!_/rsrc/[0-9][0-9]*/!!g')
    dir_name=$(dirname "${new_file_name}")
    [[ -d "${dir_name}" && ! -f "${new_file_name}" ]] && \
        git mv "${file_name}" "${new_file_name}"
done < <(find _ -type f)

popd 

