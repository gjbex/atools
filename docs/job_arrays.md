# What are job arrays?
A resource manager or scheduler that support job arrays typically
exposes a task identifier to the job script as an environment variable.
This is simply a number out of a range specified when the job is submitted.

For the resource managers and schedulers supported by `atools`, that would
be
* `PBS_ARRAYID` for PBS torque,
* `MOAB_JOBARRAYINDEX` for Adaptive's Moab, and
* `SGE_TASKID` for SUN Grid Engine (SGE),
* `SLURM_ARRAY_TASK_ID` for Slurm workload manager.

Typically, this task identifier is then use to determine, e.g., the
specific input file for this task in the job script:
```bash
...
INPUT_FILE="input-${PBS_ARRAYID}.csv"
...
```

Submitting arrays jobs is quite simple.  For each of the supported queue
systems and schedulers, one simply adds the `-t <int-range>` options to
the submission command, `qsub` for PBS torque and SUN grid engine, `msub`
for Moab, e.g., for PBS torque:
```bash
$ qsub  -t 1-250  bootstrap.pbs
```
The submission command above would create a job array of 250 tasks, and
for each the `PBS_ARRAYID` environment variable would be assigned a unique
value between 1 and 250, inclusive.

Although job arrays provide sufficient features for simple scenarios, it
quickly becomes a nuisance for more sophisticated problems, especially in
parameter exploration type computations.  `atools` aims to eliminate as
much as possible of the boiler plate code you have to write over and over
again.
