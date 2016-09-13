#!/bin/bash

source ../conf/atools_python.sh
export PYTHONPATH="../lib:${PYTHONPATH}"

python -m unittest discover -p '*_test.py'
