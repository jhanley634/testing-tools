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
from subprocess import check_output


class Parser:

    def __init__(self, deployments):
        self.deployments = set(deployments)

    def dep(self, pod):
        words = pod.split('-')
        while words and not '-'.join(words) in self.deployments:
            words.pop()
        return '-'.join(words)


def _get_thing(thing):
    """Pass in e.g. 'deployments'."""
    # We discard the heading line.
    # The sort ensures that a "more specific" like foo-bar-123 will precede foo-123.
    cmd = f'kubectl get {thing} | egrep -v "^NAME " | sort -r'
    return check_output(cmd, shell=True).decode().splitlines()


def _get_deployments():
    """Returns k8s deployment names."""
    for line in _get_thing('deployments'):
        yield line.split()[0]


def report():
    p = Parser(_get_deployments())
    node_to_dep = {}
    for line in _get_thing('pods -o wide'):
        # name ready status restarts age ip node ...
        name, _, _, _, _, _, node = line.split()
        dep = p.dep(name)
        print(dep, name)

group_by_month.py
if __name__ == '__main__':
    report()
