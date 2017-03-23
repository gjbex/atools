# Logging for fun and profit
Often, it is useful to log information about the execution of individual
tasks.  This information can be used

* to monitor the progress of the array job in real time,
* to check which tasks completed, and whether that was successful, or
    whether some failure occurred, and
* to obtain statistics on the execution time of tasks, or the execution
    time per node that was runnings the job's tasks.

Most queue systems and schedulers will provide this information, but often
not in a convenient format.

`alog` is called at the start of a task, and at its end, and provides
centralized logging in a single file.  This requires a POSIX complient
shared file system when the job is running on multiple compute nodes.

Again, consider the fragment of the job script:
```bash
#!/bin/bash
...
alpha=0.5
beta=-1.3
Rscript bootstrap.R $alpha $beta
...
```
(Note that `aenv` was not used here, which was done to stress the point
that `alog` and `aenv` are independent of one another, but obviously can
be combined.)

To enable logging, a call to `alog` is added as the first and the last
executable line of the job script, i.e.,
```bash
#!/bin/bash
...
alog --state start
alpha=0.5
beta=-1.3
Rscript bootstrap.R $alpha $beta
alog  --state end  --exit $?
```
Here we asume that the exit status of the last actual job command
(`Rscript` in this example) is also the exit status of the task.  The
Linux convention is that exit code 0 signifies success, any value between
from 1 to 255 indicates a failure.  It is the value passed to the logger
via the `--exit <status>` option that will be recorded in the log file,
and that will determine whether a task is considered failed, or
successfully completed.

The resulting log file is automatically created, and its name will be
`<job-name>.log<job-id>` where the job name and job identifier follow
the conventions of the queue system or scheduler used.

The log file will look like, e.g.,
```

1 started by r1i1n3 at 2016-09-02 11:47:45
2 started by r1i1n3 at 2016-09-02 11:47:45
3 started by r1i1n3 at 2016-09-02 11:47:46
2 failed by r1i1n3 at 2016-09-02 11:47:46: 1
3 completed by r1i1n3 at 2016-09-02 11:47:47
```
The format is `<task-id> <status> by Mnode-name> at <time-stamp`, followed
by `: <exit-status>` for failed jobs.  For this particular example, task
1 didn't complete, 2 failed, and 3 completed succesfully.

`alog` takes a single option, `--conf <conf>` to specify your own
configuration file.

Help on the command is printed using the `--help` flag.
