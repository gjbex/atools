AC_INIT([atools], [1.5.2], [geertjan.bex@uhasselt.be])
AM_INIT_AUTOMAKE([-Wall -Werror foreign tar-pax])

AC_CONFIG_FILES([
    Makefile
    bin/Makefile
    conf/Makefile
    lib/Makefile
    lib/vsc/Makefile
    lib/vsc/atools/Makefile
    reduce/Makefile
    tmpls/Makefile
])

# set batch system option
AC_ARG_WITH(
    [batchsystem],
    AS_HELP_STRING(
         [--with-batchsystem=SYSTEM],
         [Scheduler to use: torque, moab, sge, slurm; default=slurm]
     )
)

# set reduce mode option
AC_ARG_WITH(
    [reducemode],
    AS_HELP_STRING(
        [--with-reducemode=MODE],
        [reduce mode to use as default: text, body, csv; default=text]
    )
)

# set shell options
AC_ARG_WITH(
    [shell],
    AS_HELP_STRING(
        [--with-shell=SHELL],
        [shell that is considered default: bash, sh, tcsh, csh; default=bash]
    )
)

# if unset, set batch system to default, check validity
AS_IF([test "x$with_batchsystem" == "x"], [with_batchsystem=slurm])
AS_CASE([$with_batchsystem],
    [torque], [],
    [moab], [],
    [sge], [],
    [slurm], [],
    [AC_MSG_ERROR([batch system should be one of torque, moab, sge, slurm])]
)

# if unset, set reduce mode to default, check validity
AS_IF([test "x$with_reducemode" == "x"], [with_reducemode=text])
AS_CASE([$with_reducemode],
    [text], [],
    [body], [],
    [csv], [],
    [AC_MSG_ERROR([reduce mode should be one of text, body, csv])]
)

# if unset, set shell to default, check validity
AS_IF([test "x$with_shell" == "x"], [with_shell=bash])
AS_CASE([$with_shell],
    [bash], [],
    [sh], [],
    [tcsh], [],
    [csh], [],
    [AC_MSG_ERROR([default shell should be one of bash, sh, tcsh, csh])]
)

# create atools_python.sh file
python_path=$(which python)
AC_MSG_NOTICE([Setting Python to $python_path...])
echo "export PYTHON=\"${python_path}\"" > conf/atools_python.sh

# create atools.conf
AC_MSG_NOTICE([Creatign atools.conf...])
m4 \
    -DBATCH_SYSTEM=$with_batchsystem \
    -DMODE=$with_reducemode \
    -DSHELL=$with_shell \
    conf/atools.conf.m4 > conf/atools.conf

AC_OUTPUT
