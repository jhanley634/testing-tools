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


class Cluster:

    def __init__(self, cache=Path('/tmp/nodes.yaml')):
        if not cache.exists():
            self.k8s_get_nodes(cache)
        with open(cache) as fin:
            d = YAML().load(fin)
        assert d['apiVersion'] == 'v1'
        assert d['kind'] == 'List'
        self.items = d['items']

    def k8s_get_nodes(self, out_file):
        cmd = 'kubectl get nodes -o yaml'
        txt = check_output(cmd.split()).decode()
        with open(out_file, 'w') as fout:
            fout.write(txt)


class Node:

    def __init__(self, n: dict):
        self.n = dict(n)  # ruamel's ordereddict --> dict

    @property
    def name(self):
        return self.n['metadata']['name']

    @property
    def _labels(self):
        return self.n['metadata']['labels']

    @property
    def instance_type(self):
        assert self._labels['kubernetes.io/os'] == 'linux'
        return self._labels['node.kubernetes.io/instance-type']

    @property
    def availability_zone(self):
        return self._labels['topology.kubernetes.io/zone']

    @property
    def _status(self):
        return self.n['status']

    @property
    def os_image(self):
        """Typical return value: 'Ubuntu 20.04 LTS'
        """
        assert self._status['nodeInfo']['architecture'] == 'amd64'
        assert self._status['nodeInfo']['operatingSystem'] == 'linux'
        return self._status['nodeInfo']['osImage']

    @property
    def cores(self):
        return int(self._status['capacity']['cpu'])

    _kib_re = re.compile(r'^([0-9]+)Ki$')

    @property
    def installed_kib_ram(self):
        m = self._kib_re.search(self._status['capacity']['memory'])
        return int(m.group(1))

    @property
    def free_kib_ram(self):
        m = self._kib_re.search(self._status['allocatable']['memory'])
        return int(m.group(1))


if __name__ == '__main__':
    c = Cluster()
    n = Node(c.items[0])
    print(n.name, n.os_image, n.instance_type, n.availability_zone)
    print(n.free_kib_ram)
    print(n.installed_kib_ram, n.cores)

    # status = n.n['status']
    # from pprint import pp
    # breakpoint()
