#!/bin/sh

coverage3 run --rcfile=".coveragerc" setup.py test
coverage3 report -m