#!/bin/bash
if [[ ! -f ~/.localCircleBuild && ! -f ~/.prCircleBuild ]]; then
  set +e
  dpkg -l awscli > /dev/null 2>&1
  RESULT=$?
  set -e
  if [[ "$RESULT" != "0" ]]; then
    echo 'Installing AWS CLI...'
    sudo apt -y install awscli > /dev/null 2>&1
  fi
  BUILD_STATUS_PATH="s3://$BUILD_STATUS_BUCKET/$CIRCLE_PROJECT_USERNAME/$CIRCLE_PROJECT_REPONAME/$CIRCLE_SHA1"
  if [[ "$1" == 'done' ]]; then
    echo 'Flagging build as complete...'
    echo 'DONE' | aws s3 cp - $BUILD_STATUS_PATH
  else
    ACTIVE_BUILD_FILE='/home/circleci/.activeBuild'
    set +e
    aws s3 cp $BUILD_STATUS_PATH $ACTIVE_BUILD_FILE >/dev/null 2>&1
    set -e
    touch $ACTIVE_BUILD_FILE
    ACTIVE_BUILD_NUM=$(cat $ACTIVE_BUILD_FILE)
    if [[ "$ACTIVE_BUILD_NUM" == '' ]]; then
      echo 'This is the first build for this VCS revision.'
      echo $CIRCLE_BUILD_NUM | aws s3 cp - $BUILD_STATUS_PATH
    elif [[ "$ACTIVE_BUILD_NUM" == 'DONE' ]]; then
      echo 'INFO: a CircleCI build has already completed for this commit hash. This build will finish immediately.'
      circleci step halt
    elif (( $CIRCLE_BUILD_NUM < $ACTIVE_BUILD_NUM )); then
      echo 'INFO: there is a newer CircleCI build for this commit hash. This build will finish immediately.'
      circleci step halt
    else
      echo 'This is the newest build for this VCS revision.'
      echo $CIRCLE_BUILD_NUM | aws s3 cp - $BUILD_STATUS_PATH
    fi
  fi
else
  echo 'This is a local/PR CircleCI build; skipping duplicate build check.'
fi
