# Installation

## Requirements
`atools` requires at least Python 2.7.x, but only uses the standard
library.

Supported queue systems and schedulers:

* PBS torque,
* Moab (Adaptive Computing),
* SUN Grid Engine.


## Installation
After downloading a release from
[GitHub](https://github.com/gjbex/atools/releases) and unpacking, simply
run
```bash
$ ./configure --prefix=<install-path>
$ make install
```
Note: atools will be configured to use the Python that is in your PATH
when installing.  If you change your mind afterwards, edit
`conf/atools_python.sh` to your liking.

Depending on the batch system you use, the `--with-batchsystem` configure
option should be set appropriately, i.e.,

* `torque` for PBS torque,
* `moab` for Adaptive Computing Moab,
* `sge` for SUN Grid Engine.

The default is `torque`

One can also specify the default shell `atools` will assume for job scripts
at installation time by using the `--with-shell` configure option.  It
defaults to `bash`, but `sh`, `csh`, and `tcsh` are also accepted.  Note
that all relevant `atools` commands have a `--shell` option which overrides
the installation default.

In addition, one can set the default reduce mode as either `text` or `csv`
using the `--with-reducemode` configure option.  Again, `areduce` has a
`--mode` option to override this at any time.

Note that a reinstall is not required to change these installation default,
you can simply edit the `conf/atools.conf` file to modify `atools`
behavior after installation.


## Usage
Ensure that the `bin` directory is in your path when executing `atools`
commands, i.e., by adding it to the `PATH` environment variable.

Note that the Python run time dependency is "hidden" within `atools`
configuration, and is only required from within the bash wrapper scripts,
so using `atools` will not pollute any environment variables except `PATH`.
