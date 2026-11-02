# Running many short tasks: `arun`

Each array job is scheduled separately by the queue system or scheduler.
When tasks take only seconds or minutes, submitting one array job per task
puts a lot of stress on the scheduler, and the overhead of starting a job
may well exceed the run time of the task itself.  It is much better to
run several tasks in each array job.

`arun` makes this easy.  It runs a command for each task that belongs to
the current array job, one after the other, and takes care of what you
would otherwise do with [`aenv`](aenv.md) and [`alog`](alog.md):

* it defines environment variables with the values of the task's row in
  the CSV file, and
* by default, it logs the start and end of each task, so that
  [`arange`](arange.md) and [`aload`](aload.md) work as usual.

Grouping tasks is only supported for Slurm.  For other batch systems,
`arun` runs a single task per array job.

## Example

Consider the CSV file `data.csv` with the parameters for the tasks:

```
alpha,beta
0.5,-1.3
0.5,-1.5
0.5,-1.9
0.6,-1.3
...
```

The job script `bootstrap.slurm` is:

```bash
#!/usr/bin/env -S bash -l
#SBATCH --time=01:00:00
module load R

arun --data data.csv -- 'Rscript bootstrap.R $alpha $beta'
```

To run 5 tasks (rows) per array job, use `arange` to compute the array ID
range to submit:

```bash
$ sbatch --array=$(arange --data data.csv --group_size 5)  bootstrap.slurm
```

For a data file with 103 rows, `arange` prints `1-101:5`, so Slurm starts 21
array jobs.  The array job with array ID 1 runs the tasks for rows 1 to 5,
the one with array ID 6 runs rows 6 to 10, and so on.  The last one, with
array ID 101, runs only rows 101 to 103.

The group size is set only when you submit the job: Slurm passes the step
of the array ID range to the array jobs, and `arun` uses that.  The job
script doesn't change when you change the group size.  To run a single
task per array job, simply leave out `--group_size`.

Since the array IDs are task identifiers, they go up to the number of tasks,
whatever the group size.  Slurm limits array IDs to values below its
`MaxArraySize` setting, so that also limits the number of tasks you can run
this way.  You can check the value for your cluster with
`scontrol show config | grep MaxArraySize`.  If you have more tasks, split
the data file and submit a job for each part.

### The command

Everything after `--` is the command that is executed for each task.  It is
run by `bash`, so it can be any shell command.  Always put the whole
command between single quotes, e.g.,
`'Rscript bootstrap.R $alpha $beta'`.  The variables are then expanded when
each task runs.  Without the quotes, the shell running the job script
expands them before `arun` is even started, and they are empty.

Quoting the whole command also makes redirections, pipes, `;` and `&&` part
of the command for each task, rather than of the `arun` command itself.
For example, the following writes a separate output file for each task:

```bash
arun --data data.csv -- 'Rscript bootstrap.R $alpha $beta > out-$ATOOLS_TASK_ID.txt'
```

If a value may contain spaces, put the variable between double quotes
inside the single quotes, e.g., `'Rscript bootstrap.R "$alpha" "$beta"'`,
otherwise it is split into several arguments.

The command itself can't contain single quotes.  If it needs them, or if it
gets long, put it in a separate script, as shown below.

Always put `--` before the command, otherwise `arun` may take the command
for a data file.

If the command is more complicated, it is easier to put it in a separate
script, e.g., `bootstrap.sh`:

```bash
#!/usr/bin/env bash
Rscript bootstrap.R "$alpha" "$beta" > "out-${ATOOLS_TASK_ID}.txt"
```

and run that:

```bash
arun --data data.csv -- ./bootstrap.sh
```

Besides the variables from the CSV file, the task's identifier, i.e., the
row number in the CSV file, is available as `ATOOLS_TASK_ID`.  Use it
rather than the array ID to name output files, since an array job may run
several tasks.

The command runs in a new process, so shell variables set in the job script
are only visible to the command if they are exported.  Modules loaded in
the job script are available.

## Failed tasks

When a task fails, i.e., its command has a non-zero exit status, `arun`
logs that and continues with the next task.  If any task failed, `arun`
exits with status 1.

## Resuming

The log file contains task identifiers, so you can check progress or find
the tasks still to do with `arange`, see
[monitoring jobs and resuming tasks](arange.md).  To resume a job, compute
the array ID range of the groups that still have work with `arange`:

```bash
$ sbatch --array=$(arange --data data.csv --group_size 5 \
                          --log bootstrap.slurm.log10493)  bootstrap.slurm
```

and add the same `--log` option to `arun` in the job script, so that
tasks that already completed are not run again:

```bash
arun --data data.csv --log bootstrap.slurm.log10493 \
    -- 'Rscript bootstrap.R $alpha $beta'
```

To also redo the tasks that failed, add `--redo` to both commands.

Use the array ID range computed by `arange` as is.  Slurm takes the group
size from the step in the range, so a range without a step, e.g.,
`1,6,56`, runs only a single task per array job.

## Options

1. `--data <files>`: CSV files with the task parameters.  When more than
    one file is given, the variables of all files are defined.
1. `-t <range>`: task identifier range, used instead of, or together
    with, `--data`.
1. `--log <files>`: log files of previous runs, tasks that completed are
    skipped.
1. `--redo`: also run the tasks that failed according to the log files.
1. `--no_logging`: do not log the start and end of tasks, which `arun` does
    by default.
1. `--sniff <nr_bytes>`, `--no_sniffer`: see [`aenv`](aenv.md).
1. `--conf <config-file>`: use the specified configuration file, rather
    than the default one.

Help on the command is printed using the `--help` flag.
