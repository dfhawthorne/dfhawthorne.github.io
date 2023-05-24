#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Find the latest Googles Site resource
# ------------------------------------------------------------------------------

old_path_name=""
matched=1
while read path_name
do 
    if [[ -z "${old_path_name}" ]]
    then
        old_path_name="${path_name}"
    elif [[ "${old_path_name}" = "${path_name}" ]]
    then
        [[ ! matched ]] && printf "%s\n" "${path_name}"
        matched=0
    else
        old_path_name="${path_name}"
        matched=1
    fi
done < <(find . -type f | \
            sed --regexp-extended \
                --expression='s!\./[[:digit:]]+/(.*)!"\1"!' | \
            sort ) 