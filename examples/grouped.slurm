#!/usr/bin/env -S bash -l
#SBATCH --nodes=1  --ntasks=1
#SBATCH --time=00:05:00
#
# Run 5 tasks (rows of data.csv) per array job, submit with:
#   sbatch --array=$(arange --data data.csv --group_size 5) grouped.slurm
# The group size is only given at submission, Slurm passes it to arun.

# not needed in real script, this is only to localize test
PATH="../bin:$PATH"

# arun runs the command for each task of this array job: it defines the
# task's parameters from data.csv, and by default logs the start and end of
# each task in the same log file alog would use, so no alog calls are needed
arun --data data.csv -- \
    'echo "$alpha + $beta + $gamma" | bc -l > "out-${ATOOLS_TASK_ID}.txt"'
