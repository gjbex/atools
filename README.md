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

Help on all command can be obtained using the `--help` option.


### Parameter exploration
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


### Logging
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


### Monitoring and resuming computations
if `do_some_computation` in the previous examples fails, or the job is
aborted for some reason, this log can be used to determine which
computation have to be redone using `arange`, e.g.,
```bash
$ arange  --data data.csv  --log my_job.pbs.log94894
```
The output can be used as an argument for the `-t` option of `qsub`.
By default, only jobs that were not completed will be included,
to also redo failed computations, add the `--redo` option to the `arange`
call.

`arange` doubles as a job summary utility that can be used as soon as a
log file is created, so also for a job in progress.  Adding the `--summary`
flag will print the number of tasks completed, failed, and still to do.
```bash
$ arange  --data data.csv  --log my_job.pbs.log94894  --summary
```
The `--list_failed` and `--list_completed` options will explicitely show
the array ranges for those categories.


### Aggregating output
Aggregating the output produced by each task can be somewhat annoying.  The
`areduce` command helps to do this pretty effortlessly for many cases.
As the name implies, the aggregation is done through reduction, the
mathematical model is a monoid.
A number of simple cases are preprogrammed, requiring no work from the
user.  For instance, concatenation of text files and CSV files (for the
latter, the field names have to be present only as the first line of the
file, not replicated throughout the aggregated file.  More complicated
aggregations, e.g., into an R dataframe required some programming.

Suppose that the output of each task is stored in a file with name
`out-{PBS_ARRAYID}.txt` where `PBS_ARRAYID` represents the array ID of
the respective task, and the final output should be a file `out.txt` that
is the concatenation of all the individual files.
```bash
$ areduce  -t 1-4  --pattern 'out-{PBS_ARRAYID}.txt'  --out out.txt
```
Although this could be easily achieved with `cat`, there are nevertheless
advantages to using `areduce` even in this very simple case.  `areduce`
handles missing files (failed tasks) gracefully, whereas the corresponding
shell script would get somewhat tedious.  `areduce` also takes care of the
proper order of the files, while this would be cumbersome to do by hand.

If each of the output files were CSV files, the first line of each file
would contain the field names, that in te aggregated file should occur
only once as the first line.
```bash
$ areduce  -t 1-100  --pattern 'out-{t}.csv'  --out out.csv  --mode csv
```
The command above will produce the desired CSV file without any hassle.
Note that the shorthand `t` for `PBS_ARRAYID` has been used in the file
name pattern specification.

To handle more intresting cases, the user can supply two scripts that
each take two arguments: the name of the resulting file, and the name of
a single data file.  The first script creates an empty result file (in
case of CSV data, that would be a file containing a sinle line with the
field names).  The second appends the data file to the output file,
respecting the semantics of the data.  The scripts to use can be passed
to `areduce` using the `--empty` and `--reduce` options.

Examples can be found in the `reduce` directory.


### Analizing peformance and load balance
The log files generated by `alog` contain sufficient information for a
more detailed analysis of the performance and load balance.  When called
with the log files of interest as arguments, the `aload` command will
return overall statistics on the average, mininum, maximum and total
run time of tasks, and that of slaves.
```bash
$ aload  --log my_job.pbs.log94894
```
Since failed tasks may distort the statistics, they can be excluded
by specifying the `--no_failed` option.
A more detailed analysis can be done by creating an SQLite3 database to
analyse using SQL queryies (`--db` option), or by listing information
explicitely either by task (`--list_tasks`) or by slave (`--list_slaves`).
To make import into statistical or plotting softwaare easier, the `--csv`
option will create output in CSV format.


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
* Template based job script creation
* Add unit tests


## Change log

### Release 1.2
* Added `aload` to easily analyse load balance and task run time
    distributions.

### Release 1.1
* Added `areduce` to easily aggregate individual task output into a single
    file.
* Minor bug fixes.

### Release 1.0
