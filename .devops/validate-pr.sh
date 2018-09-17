#!/bin/bash
set -e
THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo 'Initializing...'
cd ~ # Prevents codebase contamination.
rm -rf node_modules prnum.txt
npm install --no-spin request request-promise > /dev/null 2>&1
node $THIS_DIR/validatePr.js
