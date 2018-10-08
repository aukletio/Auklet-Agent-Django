#!/bin/bash
set -e
if [[ "$CIRCLE_BUILD_NUM" == '' ]]; then
  echo 'This is a local build.'
  touch ~/.localCircleBuild
elif [[ "$CIRCLE_PR_NUMBER" != '' ]]; then
  echo 'This is a PR build.'
  touch ~/.prCircleBuild
elif [[ "$CIRCLE_BRANCH" != 'master' && "$CIRCLE_BRANCH" != 'rc' && "$CIRCLE_BRANCH" != 'release' ]]; then
  echo 'This is a PR build.'
  touch ~/.prCircleBuild
else
  echo 'This is a main branch build.'
fi
