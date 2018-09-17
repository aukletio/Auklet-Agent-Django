#!/bin/bash
set -e
THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Get the version and drop all build metadata from it.
VERSION=$(cat ~/.version | xargs | cut -f1 -d"+")
# Revert to a pristine checkout.
echo 'Reverting to pristine checkout...'
git reset --hard HEAD
git clean -qfdx || true
# Create release in JIRA.
JIRA_PROJECT='APM'
echo "Creating release in JIRA project '$JIRA_PROJECT'..."
JIRA_DATE=$(date +'%d/%b/%Y')
PAYLOAD="{\"name\": \"$CIRCLE_PROJECT_REPONAME $VERSION\", \"released\": true, \"userReleaseDate\": \"$JIRA_DATE\", \"project\": \"$JIRA_PROJECT\"}"
HEADERS_FILE="/tmp/jira-$RANDOM"
BODY_FILE="/tmp/jira-$RANDOM"
set +e
curl -D $HEADERS_FILE -sS -u "$JIRA_USERNAME:$JIRA_PASSWORD" -H "Content-Type: application/json" -X POST -d "$PAYLOAD" "$JIRA_URL/rest/api/2/version" > $BODY_FILE
RESULT=$?
set -e
cat -s $HEADERS_FILE
cat $BODY_FILE | jq .
if [[ "$RESULT" != "0" ]]; then
  exit $RESULT
fi
# Make and push the tag.
echo
echo 'Tagging release...'
git checkout $CIRCLE_BRANCH
git tag -a $VERSION -m "$VERSION"
git push origin $VERSION
# Fetch all tags so that the changelog generator can see them.
echo
echo 'Fetching all Git tags for changelog generation...'
git fetch --tags
# Generate the changelogs.
echo
echo 'Generating changelog updates...'
CURRENT_DIR="$(pwd)"
cd ~ # Prevents codebase contamination.
npm install --no-spin bluebird any-promise request-promise-any request semver semver-extra semver-sort parse-link-header > /dev/null 2>&1
node $THIS_DIR/calculateChangelogs.js $CURRENT_DIR
eval cd $CURRENT_DIR
# Push the changelog to GitHub.
echo
echo 'Updating changelog and pushing to GitHub...'
git checkout changelog
git branch -u origin/changelog changelog
git pull
mv -t . ~/README.md ~/README-WITH-RC.md
git add README.md README-WITH-RC.md
git commit -m "$VERSION [skip ci]"
git push
