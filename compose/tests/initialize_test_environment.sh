#!/bin/sh

python3 tests/set_config.py

coverage3 run --rcfile=".coveragerc" setup.py test
coverage3 report -m

rm settings.py