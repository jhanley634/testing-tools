#! /usr/bin/env bash

# Copyright 2016 John Hanley. MIT licensed.

find . \
    -name '*.py' \
 -o -name '*.sh' \
 -o -name Makefile |
  sort
