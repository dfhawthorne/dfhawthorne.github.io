#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Script to do changes to fix issue #2
# ------------------------------------------------------------------------------

pgm_dir="$(dirname $(realpath $0))"
pushd "${pgm_dir}"/../docs

# ------------------------------------------------------------------------------
# Update HTML files:
# (1) to point to away from _/rsrc;
# (2) replace Google Sites URLs;
# (3) remove search bar
# (4) remove discussions widget
# (5) remove recent activity widget
# (6) remove subpages list in footer
# ------------------------------------------------------------------------------

while read file_name
do
    sed --in-place \
        --regexp-extended \
        --file="${pgm_dir}/fix_issue_2.sed" \
        "${file_name}"
    python3 "${pgm_dir}/fix_issue_2.py" --replace "${file_name}"
done < <(find . -type f -name "*.html")

# ------------------------------------------------------------------------------
# Move files from _/rsrc
# ------------------------------------------------------------------------------

while read old_file_name
do 
    new_file_name=$(echo "${old_file_name}" | sed -re 's!_/rsrc/[[:digit:]]+/!!g')
    new_dir_name=$(dirname "${new_file_name}")
    if [[ -d "${new_dir_name}" ]]
    then
        [[ ! -f "${new_file_name}" || "${old_file_name}" -nt "${new_file_name}" ]] && \ 
            git mv -f "${old_file_name}" "${new_file_name}"
        [[ -f "${new_file_name}" ]] && \
            git rm -f "${old_file_name}"
    fi
done < <(find _ -type f)

# ------------------------------------------------------------------------------
# Remove empty directories from _/rsrc
# ------------------------------------------------------------------------------

if [[ -d "_/rsrc" ]]
then
    for dir in _/rsrc/*
    do
        count=$(find "${dir}" -type f | wc -l)
        [[ ${count} -eq 0 ]] && \
            git rm -f -r "${dir}"
    done
fi

popd 

