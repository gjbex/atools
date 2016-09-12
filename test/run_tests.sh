#!/bin/bash

source ../conf/atools_python.sh

python -m unittest discover -p '*_test.py'
