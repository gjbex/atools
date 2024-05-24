#!/usr/bin/env -S bash -l

# set PATH to find arange executable
PATH="../bin:$PATH"

array_ids=$(arange --data data.csv)
sbatch --array=${array_ids} test.slurm
