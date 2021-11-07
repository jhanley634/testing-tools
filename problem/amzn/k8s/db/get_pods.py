#! /usr/bin/env python

# Copyright 2021 John Hanley.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# The software is provided "AS IS", without warranty of any kind, express or
# implied, including but not limited to the warranties of merchantability,
# fitness for a particular purpose and noninfringement. In no event shall
# the authors or copyright holders be liable for any claim, damages or
# other liability, whether in an action of contract, tort or otherwise,
# arising from, out of or in connection with the software or the use or
# other dealings in the software.
from pathlib import Path
from subprocess import check_output
import re

from ruamel.yaml import YAML


class Pods:

    def __init__(self, cache=Path('/tmp/pods.yaml')):
        if not cache.exists():
            self.k8s_get_pods(cache)
        with open(cache) as fin:
            d = YAML().load(fin)
        assert d['apiVersion'] == 'v1'
        assert d['kind'] == 'List'
        self.items = d['items']

    def k8s_get_pods(self, out_file):
        cmd = 'kubectl get pods -o yaml'
        txt = check_output(cmd.split()).decode()
        with open(out_file, 'w') as fout:
            fout.write(txt)


class Pod:

    def __init__(self, p: dict):
        self.p = dict(p)  # ruamel's ordereddict --> dict

    @property
    def name(self):
        return self.p['metadata']['name']


def main(verbose=False):
    pods = Pods()


if __name__ == '__main__':
    main()
