# FAQ
### `aenv` is neat, but I don't care about job arrays, can it still be used?
Yes, it can.  Simply use the `--id` option to specify a row in a CSV
file.

### It seems that `arange` isn't useful unless you work with a CSV file for variable initialization, but I simply use `PBS_ARRAYID` for bookkeeping, how can I use `arange`?
`arange` also has the `-t` option that you can use as you would when
submitting a job.

### When using `arange` to compute which array IDs to redo it seems to return tasks that were done before, why?
Remember to pass *all* relevant log files to `arange`, not only the
last one.

### `aenv` and `arange` seem to break when my data file has a single column
The sniffer gets confused, you can use the `--no_sniffer` option to
deactivate it.  Since the data format is very simple in that case, the
defaults should do the right thing.
