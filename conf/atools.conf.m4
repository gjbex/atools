[global]
# batch system to use
batch_system = BATCH_SYSTEM
# default reduce mode
mode = MODE
# default Linux shell
shell = SHELL

# do not modify below this point unless you are extending `atools`
# capabilities

[torque]
array_idx_var = PBS_ARRAYID
job_id_var = PBS_JOBID
job_name_var = PBS_JOBNAME

[moab]
array_idx_var = MOAB_JOBARRAYINDEX
job_id_var = MOAB_JOBID
job_name_var = MOAB_JOBNAME

[sge]
array_idx_var = SGE_TASK_ID
job_id_var = JOB_ID
job_name_var = JOB_NAME

[slurm]
array_idx_var = SLURM_ARRAY_TASK_ID
job_id_var = SLURM_ARRAY_JOB_ID
job_name_var = SLURM_JOB_NAME

# file formats for reduction
[text]
empty = empty_text
reduce = reduce_text

[csv]
empty = empty_csv
reduce = reduce_csv

[body]
empty = empty_body
reduce = reduce_body
