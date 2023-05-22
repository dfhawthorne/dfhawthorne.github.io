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
        "${file_name}"
done < <(find . -type f)

popd 

