#!/bin/bash
set -e
THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
function abortIfModeNone {
  if [[ "$MODE" == "none" ]]; then
    echo 'WARNING: there were no meaningful changes found for this release. This build will now abort.'
    exit 1
  fi
}
# When running CircleCI locally, don't do anything and use a dummy app version.
# This skips unnecessary behaviors in a local build that won't work.
NEW_VERSION=
if [[ -f ~/.localCircleBuild ]]; then
  echo 'This is a local CircleCI build.'
  NEW_VERSION="0.1.0-a.local.circleci.build"
else
  # Initialize.
  echo 'Initializing...'
  cd ~ # Prevents codebase contamination.
  npm install --no-spin semver semver-extra > /dev/null 2>&1
  # Get PR number from the validation step.
  if [[ -f prnum.txt ]]; then
    PR_NUM=$(cat prnum.txt)
  fi
  # 1. Get all tags in the remote repo. Strip duplicate results for annotated tags.
  echo 'Getting latest production version...'
  TAGS=$(eval cd $CIRCLE_WORKING_DIRECTORY ; git ls-remote -q --tags | sed -E 's/[0-9a-f]{40}\trefs\/tags\/(.+)/\1/g;s/.+\^\{\}//g' | sed ':a;N;$!ba;s/\n/ /g')
  # 2. Get latest non-prerelease version, or default to 0.0.0.
  BASE_VERSION=$(node -e "var semver = require('semver-extra'); console.log(semver.maxStable(process.argv.slice(1)) || '0.0.0');" $TAGS)
  if [ "$BASE_VERSION" == '0.0.0' ]; then
    echo 'No production version yet (new codebase).'
    # No need to check changelogs/PRs, per SemVer.
    NEW_VERSION='0.1.0'
  else
    echo "Current production version: $BASE_VERSION"
    # Fetch all Git tags so we can get the SHA-1 of the latest prod version.
    echo 'Fetching all Git tags...'
    $(eval cd $CIRCLE_WORKING_DIRECTORY ; git fetch --tags)
    # 3. Determine the highest integer that should be bumped.
    echo 'Preparing to calculate next version...'
    npm install --no-spin parse-link-header > /dev/null 2>&1
    eval REPO_DIR=$CIRCLE_WORKING_DIRECTORY
    node $THIS_DIR/determineVersionChange.js $REPO_DIR $BASE_VERSION $PR_NUM
    MODE=$(cat mode.txt)
    # 4. Bump the version.
    if [[ "$MODE" == "none" ]]; then
      NEW_VERSION=$BASE_VERSION
    else
      NEW_VERSION=$(./node_modules/.bin/semver -i $MODE $BASE_VERSION)
    fi
  fi
  # 5. Add a prerelease identifier to the version if necessary.
  GIT_SHA=$(eval cd $CIRCLE_WORKING_DIRECTORY ; git rev-parse --short HEAD | xargs)
  if [ "$CIRCLE_BRANCH" == 'master' ]; then
    echo 'This is a beta release.'
    abortIfModeNone
    NEW_VERSION="${NEW_VERSION}-beta.${CIRCLE_BUILD_NUM}+${GIT_SHA}"
  elif [ "$CIRCLE_BRANCH" == 'rc' ]; then
    echo 'This is an RC release.'
    abortIfModeNone
    # Get the new RC version for this version (1 or greater).
    NEW_RC_VERSION=$(node -e "var semver = require('semver-extra'); var rcVersion = semver.maxPrerelease(process.argv.slice(1).filter(v => v.startsWith('$NEW_VERSION'))) || '.0'; rcVersion = rcVersion.substring(rcVersion.lastIndexOf('.') + 1); rcVersion = parseInt(rcVersion) + 1; console.log(rcVersion);" $TAGS)
    NEW_VERSION="${NEW_VERSION}-rc.${NEW_RC_VERSION}+${GIT_SHA}"
  elif [ "$CIRCLE_BRANCH" == 'release' ]; then
    echo 'This is a production release.'
    abortIfModeNone
    NEW_VERSION="${NEW_VERSION}+${GIT_SHA}"
  elif [[ "$PR_NUM" != "" ]]; then
    echo 'This is a PR build.'
    NEW_VERSION="${NEW_VERSION}-a.pr.${PR_NUM}+${GIT_SHA}"
  else
    echo 'No open PR from this branch to edge.'
    echo 'This is a branch build.'
    BRANCH_NAME=$(echo $CIRCLE_BRANCH | sed -E 's/[^a-zA-Z0-9]/\-/g')
    NEW_VERSION="${NEW_VERSION}-a.branch.${BRANCH_NAME}+${GIT_SHA}"
  fi
# Done.
fi
echo "New codebase version: $NEW_VERSION"
echo $NEW_VERSION > ~/.version
rm -rf node_modules mode.txt
