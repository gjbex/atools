# Gathering output

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
`out-{PBS_ARRAYID}.txt` or `out-{SLURM_ARRAY_TASK_ID}.txt` where `PBS_ARRAYID`
or `SLURM_ARRAY_TASK_ID` represents the array ID of the respective task for PBS
Torque or Slurm respectively, and the final output should be a file `out.txt`
that is the concatenation of all the individual files.

```bash
$ areduce  -t 1-250  --pattern 'out-{PBS_ARRAYID}.txt'  --out out.txt
```

Similar for Slurm:
```bash
$ areduce  -t 1-250  --pattern 'out-{SLURM_ARRAY_TASK_ID}.txt'  --out out.txt
```

Although this could be easily achieved with `cat`, there are nevertheless
advantages to using `areduce` even in this very simple case.  `areduce`
handles missing files (failed tasks) gracefully, whereas the corresponding
shell script would get somewhat tedious.  `areduce` also takes care of the
proper order of the files, while this would be cumbersome to do by hand.

If each of the output files were CSV files, the first line of each file
would contain the field names, that in the aggregated file should occur
only once as the first line.

```bash
$ areduce  -t 1-250  --pattern 'out-{t}.csv'  --out out.csv  --mode csv
```

The command above will produce the desired CSV file without any hassle.
Note that the shorthand `t` for `PBS_ARRAYID` or `SLURM_ARRAY_TASK_ID`
has been used in the file name pattern specification.

When one or more tasks failed, you may not want to aggregate the output of
those tasks since it may be incomplete and/or incorrect.  In that case,
simply use [`arange`](arange.md) to determine the task identifiers of the
completed task using the `--list_completed` flag.

Out of the box, atools supports three types of reductions that can be
specified via  the `--mode` option.

  * `text`: output files are text files, and will simply be concatenated;
  * `csv`: output files are comma-separated value (CSV) files, the first
    line of each files contains the column names, and that will not be
    repeated in the aggregated output, i.e., there will be a single line
    containing the column names at the top of the file;
  * `body`: output files are  text files, but you can specify how many
    lines to skip at the top and the bottom of each file while aggregating.

For example, the following command would aggregate data skipping three lines
at the top, and five lines at the bottom of each individual output file:

```bash
$ areduce  -t 1-250  --pattern 'out-{t}.txt'  --out out.txt  \
           --mode body  --reduce_args '--h 3  -f 5'
```

To handle more interesting cases, you can supply two scripts that
each take two arguments: the name of the resulting file, and the name of
a single data file.  The first script creates an empty result file (in
case of CSV data, that would be a file containing a single line with the
field names).  The second appends the data file to the output file,
respecting the semantics of the data.  The scripts to use can be passed
to `areduce` using the `--empty` and `--reduce` options.
Examples can be found in the `reduce` directory.

Arguments can be passed to the `empty` and `reduce` script as in the example
below:

```bash
$ areduce  -t 1-250  --pattern 'out-{t}.csv'  --out out.csv  \
           --empty my_empty  --reduce my_reduce  --reduce_args '--h 3'
```
Note that the arguments to be passed must be quoted, i.e., passed as a
single string to `areduce`.

An example of a non-trivial `reduce` is `reduce/reduce_body`.  The `body`
mode takes two additional arguments for its `reduce`, i.e., `--h <n>` will
skip the first n lines of the text files, `--f <n>` will skip the last n
lines of the text file.

`areduce` will print a warning message for missing output files, which may
happen if one or more tasks failed, or some tasks were not completed. 
These messages can be repressed using the `--quiet` flag.

In addition, `areduce` can remove the original output files if you add the
`--rm_orig` flag, use this at your own peril!

You can use your own configuration file rather than `atools` by supplying
it using the `--conf <conf-file>` option.

Help on the command is printed using the `--help` flag.
