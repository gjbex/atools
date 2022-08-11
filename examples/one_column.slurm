#!/usr/bin/env bash
#SBATCH -A lpt2_sysadmin
#SBATCH --nodes=1 --cpus-per-task=72
#SBATCH --time=00:02:00

module purge
module use /apps/leuven/icelake/2021a/modules/all
module load atools/1.5.0

source <(aenv --data data_one_column.csv --no_sniffer)

echo "running on $(hostname)"
echo "file = $file"
