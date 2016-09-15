#!/bin/bash

# determine true location of Bash script
exec=$(readlink -f ${0})

# determine directory of vsc-module-dependencies
DIR=$( cd -P "$( dirname "${exec}" )" && pwd )

echo $DIR

source ${DIR}/../conf/atools_python.sh
export PYTHONPATH="${DIR}/../lib:${PYTHONPATH}"

cd  "${DIR}"
${PYTHON} -m unittest discover -p '*_test.py'
