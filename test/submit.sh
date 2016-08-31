#!/bin/bash

# set PATH to find arange executable
PATH="../bin:$PATH"

array_ids=$(arange --data data.csv)
qsub -t ${array_ids} test.pbs
