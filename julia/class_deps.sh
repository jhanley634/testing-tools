#! /usr/bin/env bash

DIR=`dirname $0`
export PATH=${PATH}:${DIR}

FILES=${1:-`find . -name '*.java'|sort`}
exec time class_deps.jl ${FILES}
