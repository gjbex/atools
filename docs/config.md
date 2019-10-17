# Configuration file

If `atools` was installed for you by your friendly local system
administrator, you do not have to worry about the log file, it is installed
with `atools` and configured to do the right thing on your system.

The log file is in Python's `ConfigParser` format, and contains the
defaults for the system `atools` is installed on.  The first `global`
section is where these defaults are set.
```
[global]
# batch system to use
batch_system = torque
# default reduce mode
mode = text
# default Linux shell
shell = bash
````

The supported batch systems are:

* `torque`: PBS torque,
* `moab`: Adaptive Computing Moab,
* `sge`: SUN Grid Engine.

The supported standard reduction modes are:

* `text`: concatenate text files, assuming no header information,
* `csv`: concatenate CSV files, assuming the first line contains the
    column definitions.

The supported shells are:

* `bash`: Bourn again shell
* `sh`: Bourn shell
* `tcsh`: Tennex C shell
* `csh`: C shell

The remaining sections of the configuration file should normally not be
touched, unless to add additional reduce modes, support for shells or
batch systems.
