# Installation
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

Depending on the batch system you use, the `batch_system` option in
`conf/atools.conf` should be changed to:
* `torque` for PBS torque,
* `moab` for Adaptive Computing Moab,
* `sge` for SUN Grid Engine.
