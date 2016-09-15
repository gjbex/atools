AC_INIT([atools], [1.3], [geertjan.bex@uhasselt.be])
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
AC_OUTPUT
