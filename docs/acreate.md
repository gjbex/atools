# Adding atools features using templates

Although the modifications required to use `atools` are fairly simple,
they involve some steps that may be unfamiliar to the casual user.

`acreate` adds everything required to use `atools` effectively to an
existing job script.  By default, it will insert the `PATH` redefinition
to use the `atools` commands, and the logging of start and end events.
Suppose the original job script is called `jobscript.slurm`, then the command
to generate the file annotated for `atools` is:

```bash
$ acreate  jobscript.slurm  >  jobscript_atools.slurm
```

If `aenv` is to be used, in addition to logging, you simply add the
`--data` option:
```bash
$ acreate  --data data.csv --  jobscript.slurm  > jobscript_atools.slurm
```

The default shell is the one specified in the configuration file, but
this can be overridden on the command line using the `--shell` option,
e.g., if `jobscript.slurm` where a tcsh shell script, you would use

```bash
$ acreate  --shell tcsh  jobscript.slurm  >  jobscript_atools.slurm
```

It is also possible to supply your own template instead of the one provided
by `atools` in the `tmpls` directory using the `--tmpl` option, and you
can use your own configuration file with `--conf`.

Help on the command is printed using the `--help` flag.
