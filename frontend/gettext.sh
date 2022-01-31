#!/usr/bin/env bash -eo pipefail
unset command_not_found_handle

input_vue_files="$(find ./components ./pages ./layouts -type f -name '*.vue')"
workdir=$(mktemp -d "${TMPDIR:-/tmp/}$(basename $0).XXXXXXXXXXXX") || exit 1

output_file="../django/translations/master.pot"

vue_translations=${workdir}/vue.pot

./node_modules/easygettext/src/extract-cli.js --startDelimiter '' --endDelimiter '' --output ${vue_translations} ${input_vue_files}

merged_pot=${workdir}/merged.pot
msgcat ${vue_translations} > ${merged_pot}

header=${workdir}/header.pot
sed -e '/^$/q' < ${vue_translations} > ${header}

body=${workdir}/body.pot
sed '1,/^$/d' < ${merged_pot} > ${body}

cat ${header} ${body} > ${output_file}

rm -r ${workdir}
