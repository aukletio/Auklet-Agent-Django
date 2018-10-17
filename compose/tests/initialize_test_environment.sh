#!/bin/sh

python3 set_config.py

coverage3 run --rcfile=".coveragerc" setup.py test
coverage3 report -m