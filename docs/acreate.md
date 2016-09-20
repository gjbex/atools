# Adding atools features using templates,

Although the modifications required to use `atools` are fairly simple,
they involve some steps that my be unfamiliar to the casual user.

`acreate` adds everything required to use `atools` effectively to an
existing job script.  By default, it will insert the `PATH` redefinition
to use the `atools` commands, and the logging of start and end events.
Suppose the original log file is called `bootstrap.pbs`, then the command
to generate the file annotated for `atools` is:
```bash
$ acreate  bootstrap.pbs  >  bootstrap_atools.pbs
```

If `aenv` is to be used, in addition to logging, you simply add the
`--data` option:
```bash
$ acreate  --data data.csv  bootstrap.pbs  > bootstrap_atools.pbs
```

The default shell is the one specified in the configuration file, but
this can ben overridden on the command line using the `--shell` option,
e.g., if `bootstrap.pbs` where a tcsh shell script, you would use
```bash
$ acreate  --shell tcsh  bootstrap.pbs  >  bootstrap_atools.pbs
```

It is also possible to supply your own template instead of the one provided
by `atools` in the `tmpls` directory using the `--tmpl` option, and you
can use your own configuration file with `--conf`.

Help on the command is printed using the `--help` flag.
