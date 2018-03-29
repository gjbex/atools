# Change log

## Release 1.4.2
* Workaround for data files that have only a single column.
* Fixes in documentation and example.
* Fix in autotools file that impacted installation

## Release 1.4.1
* Bug fixes for installation of body reduce mode.
* Bug fix in `areduce` for actually using body mode
* According to principle of least surprise, changed installation default
    mode from csv to text.
* Regenerated `configure`.

## Release 1.4
* Added `acreate` command to automatically add `atools` features to a job
    script.
* `areduce` can now pass arguments to `empty` and `reduce` script for
    to make implementations of non-trivial cases more generic.
* Added `body` reduction mode to `arecude`.
* Improved installation procedure so that fiddling with the configuration
    file after installation is no longer required.

## Release 1.3
* Added unit testing for all modules.
* Improved installation procedure, now uses autotools.
* Added documentation.
* Bug fixes to aload.
* Implemented `--rm_orig` in `areduce`.

## Release 1.2
* Added `aload` to easily analyse load balance and task run time
    distributions.

## Release 1.1
* Added `areduce` to easily aggregate individual task output into a single
    file.
* Minor bug fixes.

## Release 1.0
* Initial release.
