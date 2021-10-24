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
from typing import Set

from problem.amzn.k8s.util_resource import _get_resources


class Parser:

    def __init__(self, deployments):
        self.deployments = set(deployments)

    def depl(self, pod):
        words = pod.split('-')
        while words and '-'.join(words) not in self.deployments:
            words.pop()
        return '-'.join(words)


def _get_deployments():
    """Generates k8s deployment names."""
    for line in _get_resources('deployments'):
        yield line.split()[0]


def find_fragile_deployments() -> Set[str]:
    """Shows pods from same deployment that are running on same node."""
    # We prefer that 2 pods be scheduled on 2 distinct nodes, in case one node bounces.
    p = Parser(_get_deployments())
    fragile_depl = set()
    seen = set()
    for line in _get_resources('pods -o wide'):
        # name ready status restarts age ip node ...
        pod, _, status, _, _, _, node, *_ = line.split()
        if status != 'Running':  # Skip the 'Completed' cron jobs.
            continue
        depl = p.depl(pod)
        depl_node = (depl, node)
        if depl_node in seen:
            print(depl_node)
            fragile_depl.add(depl)
        seen.add(depl_node)

    if not fragile_depl:
        return fragile_depl
    # Now suggest a command that reveals pod IDs, preparatory to one or more
    # $ kubernetes delete pod XYZ
    # commands. Then we should re-run the report to verify
    # that better (more diverse) nodes were chosen by k8s
    # when it respawned replacement pods.
    regex = '|'.join(sorted(fragile_depl))
    print(f'\nkubectl get pods -A -o wide | egrep "{regex}"')
    return fragile_depl


if __name__ == '__main__':
    find_fragile_deployments()
