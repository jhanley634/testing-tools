#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.

from pprint import pp
import glob
import os
import re
import subprocess

from ruamel.yaml import YAML


def _run_freeze():
    dep_ver_re = re.compile(r"^([\w-]+)==([\d.]+)$")
    cmd = "pip freeze"
    for line in subprocess.check_output(cmd.split()).decode().split("\n"):
        m = dep_ver_re.search(line.rstrip())
        if m:
            yield m.groups()  # e.g. 'absl-py': '2.0.0'


def _get_frozen_dep_ver():
    return dict(_run_freeze())


def main():
    pp(_get_frozen_dep_ver())


if __name__ == "__main__":
    main()
