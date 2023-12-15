#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.


from pathlib import Path
from pprint import pp
from typing import Generator, Iterable
import re
import subprocess

from ruamel.yaml import YAML


def _parse_requirements(in_file: Path) -> Generator[tuple[str, str], None, None]:
    with open(in_file) as fin:
        yield from _dep_ver_tuples(fin)


def _run_freeze() -> Generator[tuple[str, str], None, None]:
    cmd = "pip freeze"
    frozen = subprocess.check_output(cmd.split()).decode().split("\n")
    yield from _dep_ver_tuples(frozen)


_dep_ver_re = re.compile(r"^([\w-]+)[~>=]=([\d.]+)$")


def _dep_ver_tuples(fin: Iterable[str]) -> Generator[tuple[str, str], None, None]:
    for line in fin:
        m = _dep_ver_re.search(line)
        if m:
            dep, ver = m.groups()  # e.g. 'absl-py': '2.0.0'
            yield dep, ver


def main() -> None:
    req = dict(_parse_requirements(Path("requirements.txt")))
    assert 28 == len(req)
    freeze = dict(_run_freeze())
    pp(freeze)


if __name__ == "__main__":
    main()
