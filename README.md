# atools

[![Documentation Status](https://readthedocs.org/projects/atools/badge/?version=latest)](http://atools.readthedocs.io/en/latest/?badge=latest)

`atools` is intended to facilitate working with job arrays, a feature
supported by a resource manager such as PBS torque, or a scheduler such
as Moab (Adaptive Computing), SUN Grid Engine and Slurm workload manager.

Although the job array concept is quite versatile, typically some
tinkering is required for bookkeeping purposes.  `atools` aims to
eliminate much of the boilerplate coding by supporting the following
common tasks with minimal modification of job scripts.

* Adding `atools` features using templates,
    (using [`acreate`](docs/acreate.md)),
* instantiating parameter values per task
    (using [`aenv`](docs/aenv.md)),
* logging task start and completion information
    (using [`alog`](docs/alog.md)),
* monitoring the progress of a running job in terms of the number of tasks
    completed, and the number of failed tasks
    (using [`arange`](docs/arange.md)),
* resuming computations if not all tasks were completed
    (using [`arange`](docs/arange.md)),
* aggregating output generated by the tasks
    (using [`areduce`](docs/areduce.md), and
* analysing task run times and load balance
    (using [`aload`](docs/aload.md)).


## Documentation
Full documentation is available on
[Read the Docs](http://atools.readthedocs.io/en/latest/).


## Important note
If you use job arrays on a HPC system that accounts for compute time,
remember that each job in the array is account as an individual job.
Depending on the number of cores used by a job, this may increase the
cost by a large factor compared to using the
[worker framework](https://github.com/gjbex/worker).


## Requirements
`atools` requires at least Python 3.2, but only uses the standard
library.

Currently, PBS torque, Adaptive Computing Moab, SUN Grid Engine and
Slurm workload manager are supported.  Slurm is the default, but
that can be change during installation.


## Installing
After downloading and unpacking, simply run `configure` and `make`.  For
details, see the [documentation](http://atools.readthedocs.io/en/latest/).


## Planned features
In no particular order...
* Template based job script creation
* Indexed data files for scaling to very large numbers of tasks.


## Contributors
* [Geert Jan Bex](mailto:geertjan.bex@uhasselt.be), Hasselt University/University
    of Leuven
* Stefan Becuwe, Antwerp University
  * Fixes to the documentation
  * Fix to the install process
  * Bug report
* Ward Poelmans, Vrije Universiteit Brussel
  * Fixes to the install process
* Kurt Lust, Antwerp University
  * Several bug reports and fixes
  * Added Slurm compatibility
* Robin Verschoren, Antwerp University
  * Bug report and fix suggestion
* Damien Francois, Unversite Catholique de Louvain-la-Neuve
  * Fix typos
