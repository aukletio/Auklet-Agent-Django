#!/bin/bash
set -e
THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Get the currently open prod release PR.
PROD_RELEASE_PR=$(curl -s -H "Authorization: Token $CHANGELOG_GITHUB_TOKEN" "https://api.github.com/repos/$CIRCLE_PROJECT_USERNAME/$CIRCLE_PROJECT_REPONAME/pulls?state=open&head=$CIRCLE_PROJECT_USERNAME:rc&base=release" | jq -r '.[0] | .number | select (.!=null)')
# If such a PR exists, erase its description so that its changelog will be regenerated.
if [[ "$PROD_RELEASE_PR" != "" ]]; then
  echo "Open prod release PR found: $PROD_RELEASE_PR"
  echo 'Triggering changelog update...'
  curl -s -H "Authorization: Token $CHANGELOG_GITHUB_TOKEN" -X PATCH --data '{"body":null}' "https://api.github.com/repos/$CIRCLE_PROJECT_USERNAME/$CIRCLE_PROJECT_REPONAME/pulls/$PROD_RELEASE_PR"
else
  echo 'No open prod release PR; nothing to do.'
fi
