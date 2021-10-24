
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
"""
Utility functions for retrieving kubernetes resources (nodes, pods).
"""
from subprocess import check_output
from typing import Iterable, List, Tuple


def _get_resources(resource_type) -> List[str]:
    """Pass in e.g. 'deployments'."""
    # We discard the heading line.
    cmd = f'kubectl get {resource_type} | egrep -v "^NAME "'
    return check_output(cmd, shell=True).decode().splitlines()


def _get_running_pods() -> Iterable[Tuple[str, str]]:
    """Generator for mapping each pod to its scheduled node.
    """
    for line in _get_resources('pods -o wide'):
        # name ready status restarts age ip node ...
        pod, _, status, _, _, _, node, *_ = line.split()
        if status != 'Running':  # Skip the 'Completed' cron jobs.
            continue
        yield pod, node
