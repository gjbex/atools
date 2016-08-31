# atools
`atools` is intended to facilitate working with job arrays, a feature
supported by a resource manager such as PBS torque, or a scheduler such
as Moab (Adaptive Computing).


## Description and how to use
Job arrays are intended to perform a potentially large number of similar,
but independent tasks.  An individual task is identified by a shell
variable `PBS_ARRAYID`, which can be used to determine task specific
aspects such as input or parameters.

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
```
#!/bin/bash
#PBS -l nodes=1:ppn=1

cd $PBS_O_WORKDIR
do_some_computation $alpha $beta $gamma
```
The `aenv` command makes this straightforward.
```
#!/bin/bash
#PBS -l nodes=1:ppn=1

source $(aenv --data data.csv)
cd $PBS_O_WORKDIR
do_some_computation $alpha $beta $gamma
```
To submit this job, first determine the relevant array ID range using the
`arange` command, i.e.,
```
$ arange --data data.csv
1-4
```
Now the job can be submitted as
```
$ qsub -t 1-4 my_job.pbs
```
The subsequent values of `PBS_ARRAYID` will be used under to hood as a
line index in the `data.csv` file.

PBS torque will create individual output and error files from which it may
be possible to gather statistics and exit status information, but again,
this requires tinkering by the user. `atools` provides a straightforward
logging mechanism using `alog`, e.g.,
```
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
```
$ arange --data data.csv --log my_job.pbs.log94894
```
The output can be used as an argument for the `-t` option of `qsub` or
`msub`.  By default, only jobs that were not completed will be included,
to also redo failed computations, add the `--redo` option to the `arange`
call.

Help on all command can be obtained using the `--help` option.


## Requirements
`atools` requires at least Python 2.7.x, but only uses the standard
library.

## Installing
After dropping the directory wherever convenient, review the bash scripts
in the `bin` directory to set a Python executable of your liking.
