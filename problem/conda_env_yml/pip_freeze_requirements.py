#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.


from pathlib import Path
from typing import Generator, Iterable
import re
import subprocess

_dep_ver_re = re.compile(r"^([\w-]+)[~>=]=([\d.]+)$")


def _parse_requirements(in_file: Path) -> Generator[tuple[str, str], None, None]:
    with open(in_file) as fin:
        yield from _dep_ver_tuples(fin, _dep_ver_re)


def _parse_environment(in_file: Path) -> Generator[tuple[str, str], None, None]:
    dep_ver_re = re.compile(r"^ *- *([\w-]+) *>?= *([\d.]+)")
    with open(in_file) as fin:
        yield from _dep_ver_tuples(fin, dep_ver_re)


def _run_freeze() -> Generator[tuple[str, str], None, None]:
    cmd = "pip freeze"
    frozen = subprocess.check_output(cmd.split()).decode().split("\n")
    yield from _dep_ver_tuples(frozen, _dep_ver_re)


def _dep_ver_tuples(
    fin: Iterable[str], dep_ver_re: re.Pattern
) -> Generator[tuple[str, str], None, None]:
    for line in fin:
        m = dep_ver_re.search(line)
        if m:
            dep, ver = m.groups()  # e.g. 'absl-py': '2.0.0'
            yield dep.lower(), ver


def main() -> None:
    req = dict(_parse_requirements(Path("requirements.txt")))
    assert 28 == len(req)
    freeze = dict(_run_freeze())

    for dep, rev in _parse_environment(Path("environment.yml")):
        fr_rev = freeze.get(dep, "0.0.0")
        if fr_rev > rev:
            print(f"UPDATE environment.yml to use: {dep} >= {fr_rev}")

        if dep not in req:
            print(f"{dep}=={rev}")
        else:
            if req[dep] < rev:
                dep = dep.upper()
                print(f"{dep}=={rev}")


if __name__ == "__main__":
    main()
