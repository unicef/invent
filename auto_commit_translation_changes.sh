#!/usr/bin/env bash -eo pipefail

if git diff --quiet django/translations/master.pot; then
   echo "No changes"
else
   echo "Translation have been updated, we need to commit them"
   git add django/translations/master.pot
   git commit -am "update translations"
fi
