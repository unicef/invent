#!/usr/bin/env bash -eo pipefail

# needs autotag to be installed
# curl -O https://raw.githubusercontent.com/MichaelCurrin/auto-tag/v1.2.0/autotag
# chmod +x autotag

if git diff --quiet django/translations/master.pot; then
   echo "No changes in translations"
   exit 0
else
   echo "Translation have been updated, we need to commit them"
   git checkout dev
   git pull origin dev
   git add django/translations/master.pot
   git commit -m "update translations [AUTO] [ci skip]"
   ./autotag b  # increment bug version X.X.THIS
   git push && git push --tags
   exit 1
fi
