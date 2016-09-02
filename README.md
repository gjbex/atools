# atools
`atools` is intended to facilitate working with job arrays, a feature
supported by a resource manager such as PBS torque, or a scheduler such
as Moab (Adaptive Computing) and SUN Grid Engine.


## Important note
If you use job arrays on a HPC system that accounts for compute time,
remember that each job in the array is account as an individual job.
Depending on the number of cores used by a job, this may increase the
cost by a large factor compared to using the
[worker framework](https://github.com/gjbex/worker).


## Description and how to use
Job arrays are intended to perform a potentially large number of similar,
but independent tasks.  An individual task is identified by a shell
variable identifying the task, and can be used to determine task specific
aspects such as input/output, or parameters.

Each batch system defines its own environment variable, i.e.,

1. PBS torque: `PBS_ARRAYID`
1. Adaptive Computing Moab: `MOAB_JOBARRAYINDEX`
1. SUN Grid Engine: `SGE_TASK_ID`

The command line options to specify a job array on the command line is
`-t` for all these batch systems though.
The example below is specific to PBS torque, and should be modified
appropriately for Adaptive Computing's Moab, or SUN Grid Engine

Although this allows for a very broad spectrum of applications, it
requires the user to write a lot of error-prone boiler plate code.
`atools` is developed to handle this gracefully.

The underlying assumption is that tasks are described in terms of a
number of parameters, which form the rows of a CSV file.  The latter's
first line contains the names of those parameters, e.g.,
```
alpha,beta,gamma
1.0,2.0,3.0
2.0,3.0,4.0
3.0,4.0,5.0
4.0,5.0,6.0
```
The file `data.csv` above describes four tasks, specified by three
parameters `alpha`, `beta`, and `gamma` respectively.
It would be convenient if the corresponding PBS script could be written as:
```bash
#!/bin/bash
#PBS -l nodes=1:ppn=1

cd $PBS_O_WORKDIR
do_some_computation $alpha $beta $gamma
```
The `aenv` command makes this straightforward.
```bash
#!/bin/bash
#PBS -l nodes=1:ppn=1

source $(aenv --data data.csv)
cd $PBS_O_WORKDIR
do_some_computation $alpha $beta $gamma
```
To submit this job, first determine the relevant array ID range using the
`arange` command, i.e.,
```bash
$ arange --data data.csv
1-4
```
Now the job can be submitted as
```bash
$ qsub -t 1-4 my_job.pbs
```
The subsequent values of `PBS_ARRAYID` will be used under to hood as a
line index in the `data.csv` file.

PBS torque will create individual output and error files from which it may
be possible to gather statistics and exit status information, but again,
this requires tinkering by the user. `atools` provides a straightforward
logging mechanism using `alog`, e.g.,
```bash
#!/bin/bash
#PBS -l nodes=1:ppn=1

alog --state start
source $(aenv --data data.csv)
cd $PBS_O_WORKDIR
do_some_computation $alpha $beta $gamma
alog --state end --exit "$?"
```
This will create a log file with a name following the pattern
`<job-name>.log<job-id>`, so a single file for the entire array job.

if `do_some_computation` in the previous examples fails, or the job is
aborted for some reason, this log can be used to determine which
computation have to be redone using `arange`, e.g.,
```bash
$ arange --data data.csv --log my_job.pbs.log94894
```
The output can be used as an argument for the `-t` option of `qsub`.
By default, only jobs that were not completed will be included,
to also redo failed computations, add the `--redo` option to the `arange`
call.

`arange` doubles as a job summary utility that can be used as soon as a
log file is created, so also for a job in progress.  Adding the `--summary`
flag will print the number of tasks completed, failed, and still to do.
```bash
$ arange --data data.csv --log my_job.pbs.log94894 --summary
```
The `--list_failed` and `--list_completed` options will explicitely show
the array ranges for those categories.

Help on all command can be obtained using the `--help` option.


## Requirements
`atools` requires at least Python 2.7.x, but only uses the standard
library.


## Installing
After dropping the directory wherever convenient, review the bash scripts
in the `bin` directory to set a Python executable of your liking.

Depending on the batch system you use, the `batch_system` option in
`conf/atools.conf` should be changed to:
* `torque` for PBS torque,
* `moab` for Adaptive Computing Moab,
* `sge` for SUN Grid Engine.


## FAQ
1. `aenv` is neat, but I don't care about job arrays, can it still be used?

   Yes, it can.  Simply use the `--id` option to specify a row in a CSV
   file.
1. It seems that `arange` isn't useful unless you work with a CSV file for
    variable initialization, but I simply use `PBS_ARRAYID` for bookkeeping,
    how can I use `arange`?

    `arange` also has the `-t` option that you can use as you would when
    submitting a job.
1. When using `arange` to compute which array IDs to redo it seems to
    return items that were done before, why?

    Remember to pass *all* relevant log files to `arange`, not only the
    last one.


## Planned features
In no particular order...
* Improve documentation for use with SUN Grid Engine.
* Conveniently combine output of an array job into a single file with and
    without user specified reductor.
* Load balance analysis based on the log file.


## Change log

### Release 1.0
