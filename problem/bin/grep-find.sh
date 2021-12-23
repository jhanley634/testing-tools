#! /usr/bin/env bash

# Copyright 2016 John Hanley. MIT licensed.

find.sh |
  xargs gegrep --color -B4 -A4 -n -i "$@"
