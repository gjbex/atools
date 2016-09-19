AC_INIT([atools], [1.4], [geertjan.bex@uhasselt.be])
AM_INIT_AUTOMAKE([-Wall -Werror foreign tar-pax])
echo "export PYTHON=\"$(which python)\"" > conf/atools_python.sh
AC_CONFIG_FILES([
    Makefile
    bin/Makefile
    conf/Makefile
    lib/Makefile
    lib/vsc/Makefile
    lib/vsc/atools/Makefile
    reduce/Makefile
])
AC_ARG_WITH(
    [batchsystem],
    AS_HELP_STRING(
         [--with-batchsystem=SYSTEM],
         [Scheduler to use: torque, moab, sge; default=torque]
     )
)
AC_ARG_WITH(
    [reducemode],
    AS_HELP_STRING(
        [--with-reducemode=MODE],
        [reduce mode to use as default: text, csv; default=csv]
    )
)
AS_IF([test "x$with_batchsystem" == "x"], [with_batchsystem=torque])
AS_CASE([$with_batchsystem],
    [torque], [],
    [moab], [],
    [sge], [],
    [AC_MSG_ERROR([batch system should be one of torque, moab, or sge])]
)
AS_IF([test "x$with_reducemode" == "x"], [with_reducemode=csv])
AS_CASE([$with_reducemode],
    [text], [],
    [csv], [],
    [AC_MSG_ERROR([reduce mode should be one of text, csv])]
)
echo "mode: $with_reducemode"
echo "batch system: $with_batchsystem"
AC_OUTPUT
