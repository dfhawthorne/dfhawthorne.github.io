#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Find sub-page menu pages that do not have a YAML-encoded widget
# ------------------------------------------------------------------------------

scripts_dir=$(dirname $(realpath $0))
docs_dir=$(dirname ${scripts_dir})/docs

temp_file=$(mktemp --suffix=.dat)
if [[ $? -ne 0 ]]
then
    printf "%s: Unable to create temporary file\n" "$0" >&2
    exit 1
fi

find "${docs_dir}" \
        -regextype posix-extended -a \
        -type d -a -name '_*' -a -prune -a -false -o \
        -type f -a -not -regex '.*/(ASH|AWR|workload)_.*.html' -a \
            -name '*.html' -a -exec dirname {} \; | \
    sort --unique | \
    sed --regexp-extended \
        --expression='/\/docs(\/home)?$/d' \
        --expression='s!$!.html!' >"${temp_file}"

diff "${temp_file}" \
        <(xargs \
            grep --extended-regexp \
                --files-with-matches \
                '^sub-pages:$' \
                <"${temp_file}" \
            ) | \
    sed --silent \
        --regexp-extended \
        --expression="s!^< ${docs_dir}/!!p"

rm -f "${temp_file}"

