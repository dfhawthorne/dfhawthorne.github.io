#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Creates a Jekyll format template based on an existing page
# ------------------------------------------------------------------------------

prog_name=$(basename "$0")
scripts_dir=$(dirname $(realpath "$0"))
base_dir=$(dirname "${scripts_dir}")/docs
if [[ -z "$1" ]]
then
    printf "%s: file name expected\n" "${prog_name} " >&2
    exit 1
fi

if [[ ! -r "$1" ]]
then
    printf "%s: '%s' is not readable\n" "${prog_name}" "$1" >&2
    exit 1
fi

base_url=$(realpath "$1" | sed -e "s!${base_dir}/!!")
title=$(hxnormalize -xe "$1" | hxselect -ic title | sed -e 's!Yet Another OCM - !!')

printf "%s\nlayout: default\ntitle: '%s'\nbase-url: '%s'\nbreadcrumbs:\n" '---' "${title}" "${base_url}"

IFS='/' read -ra file_name_array <<< "${base_url}"
bc_url=''
for file_name in "${file_name_array[@]}"
do
    [[ -n "${bc_url}" ]] && bc_url="${bc_url}/${file_name}" || bc_url="${file_name}"
    [[ "${base_url}" == "${bc_url}" ]] && break
    bc_fn="${base_dir}/${bc_url}.html"
    if [[ ! -r "${bc_fn}" ]]
    then
        printf "%s: '%s' is not readable\n" "${prog_name}" "${bc_fn}" >&2
        exit 1
    fi
    bc_title=$(sed -nre 's!^title: !!p' "${bc_fn}")
    printf "%s title: %s\n  url: %s\n" '-' "${bc_title}" "${bc_url}"
done

left_link_fn=''
right_link_fn=''
matched_fn=0
for file_name in $(dirname $1)/*
do
    [[ -d "${file_name}" ]] && continue
    if [[ "${file_name}" == "$1" ]]
    then
        matched_fn=1
        continue
    else
        if [[ ${matched_fn} -eq 0 ]]
        then
            left_link_fn="${file_name}"
        else
            right_link_fn="${file_name}"
            break
        fi
    fi
done

if [[ -n "${left_link_fn}" || -n "${right_link_fn}" ]]
then
    printf "scroll-bar:\n"
    if [[ -n "${left_link_fn}" ]]
    then
        left_url=$(realpath "${left_link_fn}" | sed -e "s!${base_dir}/!!")
        left_title=$(sed -nre 's!^title: !!p' "${left_link_fn}")
        [[ -z "${left_title}" ]] && \
            left_title=$(hxnormalize -xe "${left_link_fn}" | \
                hxselect -ic title | \
                sed -e 's!Yet Another OCM - !!')
        printf "  left-link:\n    url: %s\n    title: '%s'\n" \
            "${left_url}" "${left_title}"
    fi
    if [[ -n "${right_link_fn}" ]]
    then
        right_url=$(realpath "${right_link_fn}" | sed -e "s!${base_dir}/!!")
        right_title=$(sed -nre 's!^title: !!p' "${right_link_fn}")
        [[ -z "${right_title}" ]] && \
            right_title=$(hxnormalize -xe "${right_link_fn}" | \
                hxselect -ic title | \
                sed -e 's!Yet Another OCM - !!')
        printf "  right-link:\n    url: %s\n    title: '%s'\n" \
            "${right_url}" "${right_title}"
    fi
fi

printf "%s\n" '---'
