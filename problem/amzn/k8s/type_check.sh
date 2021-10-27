#! /usr/bin/env bash

set -e -x

# Checking type annotations since anno 2012!
mypy .
echo


pytype --strict-import --unresolved .
pytype --tree .
#  Ninja trouble?
# pytype .


python -c 'import pyre_check' || pip install pyre-check fb-sapp
ls .pyre/ > /dev/null || pyre init

#  This says much more about our conda env than about the *.py source files:
# pyre analyze
