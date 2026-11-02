#!/usr/bin/env -S bash -l
#SBATCH --nodes=1  --ntasks=1
#SBATCH --time=00:05:00
#
# Same as test.slurm, but using arun, which defines the work item
# parameters and, by default, logs start and end of each work item.
# Submit with
#   sbatch --array=$(arange --data data.csv) test_arun.slurm
# or, to run 5 work items per array job,
#   sbatch --array=$(arange --data data.csv --group_size 5) test_arun.slurm

# not needed in real script, this is only to localize test
PATH="../bin:$PATH"

# do actual work for each work item, note the single quotes so that
# the variables are expanded by arun for each work item
arun --data data.csv -- '
    echo "alpha = $alpha"
    echo "beta = $beta"
    echo "gamma = $gamma"
    result=$(echo "$alpha + $beta + $gamma" | bc -l)
    echo "$alpha,$beta,$gamma,$result" > "out-${ATOOLS_TASK_ID}.txt"
    exit $(( $RANDOM % 2 ))
'
