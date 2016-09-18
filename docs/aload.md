# Detailed job statistics
Gathering statistics about the execution time of tasks is straightforward
using `aload`.  Given the log file(s) of a job, it will

* the number of tasks completed (both succesful and failed), the average,
    minimum, maximum, and total execution time;
* the number of slaves, the average, minimum, maximum, and total execution
    time from the perspective of the slaves.

The first statistics is of course useful to guide future experiments,
or to report on.  The second statistics may be helpful to estimate load
imbalance, and improve resource requests for future jobs.

Using `aload` is simple:
```bash
$ aload  --log bootstrap.pbs.log10493
```
It is not always useful to include failed items in the statistics since
their execution time may seriously skew the results.  They can be excluded
by adding the `--no_failed` flag to the call to `aload`.

Sometimes it can be useful to compute more detailed statistics or plot
distributions of, e.g., the task execution time.  It is beyond the scope
of `aload` to do this, but the data can be exported for further analysys
by adding the `--list_tasks` flag, i.e.,
```bash
$ aload  --log bootstrap.pbs.log10493  --list_tasks
```
Similarly, for raw data on the slaves, add the `--list_slaves` flag.
If the output is to be imported in a software package, or parsed by a
script, it can be more convenient to obtain it in CSV format by adding the
`--csv` flag.

Internally, `aload` uses an in-memory SQLite3 database for storing and
analyzing the information.  This database can be made persistent by adding
the `--db <db-name>` option.  You can easily analyze the data using SQL
queries on the tables directly.

Lastly, you can provide your own configuration file using the
`--conf <config-file>` option.

Help on the command is printed using the `--help` flag.
