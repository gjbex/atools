# Getting your parameters: `aenv`
A resource manager or scheduler that support job arrays typically
exposes a task identifier to the job script as an environment variable.
This is simply a number out of a range specified when the job is submitted.

For the resource managers and schedulers supported by `atools`, that would
be
* `PBS_ARRAYID` for PBS torque,
* `MOAB_JOBARRAYINDEX` for Adaptive's Moab, and
* `SGE_TASKID` for SUN Grid Engine (SGE).

Typically, this task identifier is then use to determine, e.g., the
specific input file for this task in the job script:
```bash
...
INPUT_FILE="input-${PBS_ARRAYID}.csv"
...
```

Although this is fine for simple scenarios, it quickly becomes a nuisance
for more sophisticated problems, especially in parameter exploration type
computations.  `atools` aims to eliminate as much as possible of the
boiler plate code you have to write over and over again.

The parameters can be stored in an CSV file, where the first row is simply
the names of the parameters, and each consecutive row represents the
values of these parameters for a specfic experiment, i.e., computational
task.

`aenv` will use the task identifier as an index into this CSV file, and
define environment variables with the appropriate values for that task.
As an example, consider the following PBS script:
```bash
#!/bin/bash
...
alpha=0.5
beta=-1.3
Rscript bootstrap.R $alpha $beta
...
```
However, this approach would lead to as many job scripts are there are
parameter instances, which is inconvenient to say the least.

This computation would have to be done for many values for `alpha` and
`beta`.  These values can be represented in an CSV file, `data.csv`:
```
alpha,beta
0.5,-1.3
0.5,-1.5
0.5,-1.9
0.6,-1.3
...
```
The job script can be modified to automatically define the appropriate
values for `alpha` and `beta`

