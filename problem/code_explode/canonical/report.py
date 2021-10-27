#! /usr/bin/env python
from pathlib import Path
import dis
import importlib


def canonical_report(infile='report.py', out_dir='out'):
    out_dir = Path(out_dir).expanduser().resolve()
    mod = importlib.import_module(str(infile))
    d = dis.dis(mod)
    print(d)


if __name__ == '__main__':
    canonical_report()
