#! /usr/bin/env bash

set -e

DIR=`dirname $0`
export PATH=${PATH}:${DIR}/src

FILES=${1:-`find . -name '*.java'|sort`}
class_deps.jl ${FILES} | column -t

cd /tmp
set -x
dot -Tpng -o /tmp/deps.png deps.dot
dot -Tpdf -o /tmp/deps.pdf deps.dot
