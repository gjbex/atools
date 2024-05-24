#!/usr/bin/env -S bash -l
#SBATCH --nodes=1  --ntasks=1
#SBATCH --time=00:05:00

# not needed in real script, this is only to localize test
PATH="../bin:$PATH"

# log start of work item execution
alog --state start

# define work item parameters
source <(aenv --data data.csv)

# do actual work, i.e., original Slurm script
echo "alpha = $alpha"
echo "beta = $beta"
echo "gamma = $gamma"
exit_code=$(( $RANDOM % 2 ))

result=$(echo "$alpha + $beta + $gamma" | bc -l)
echo "$alpha,$beta,$gamma,$result" > "out-${PBS_ARRAYID}.txt"

# log end of work item execution
alog --state end --exit "$exit_code"
