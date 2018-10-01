#!/bin/bash
set -e
THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VERSION=$(cat ~/.version)
cd ~
node $THIS_DIR/semverTo440.js $VERSION
