#!/bin/bash
set -e
if [[ "$1" == "" ]]; then
  echo "ERROR: env not provided."
  exit 1
fi
ENVDIR=$1
VERSION="$(cat VERSION)"
VERSION_SIMPLE=$(cat VERSION | xargs | cut -f1 -d"+")
export TIMESTAMP="$(date --rfc-3339=seconds | sed 's/ /T/')"
