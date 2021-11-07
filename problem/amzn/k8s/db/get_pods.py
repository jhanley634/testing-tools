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
from functools import lru_cache
from io import StringIO
from pathlib import Path
from subprocess import check_output
import json

from glom import glom
from ruamel.yaml import YAML


@lru_cache
def _get_node_attrs(in_file=Path('/tmp/node_az_and_memory.json')) -> dict:
    with open(in_file) as fin:
        return json.load(fin)


def _get_az_and_memory(node_name: str):
    az_kib = _get_node_attrs().get(node_name, 'unknown_AZ 0')
    az, kib = az_kib.split()
    return az, int(kib)


def node_availability_zone(node_name: str):
    return _get_az_and_memory(node_name)[0]


def node_installed_kib(node_name: str):
    return _get_az_and_memory(node_name)[1]


class Pods:

    def __init__(self, cache=Path('/tmp/pods.json')):
        if not cache.exists():
            self.k8s_get_pods(cache)
        with open(cache) as fin:
            d = json.load(fin)  # typical parse time: 80 msec

        assert d['apiVersion'] == 'v1'
        assert d['kind'] == 'List'
        self.items = d['items']

    def k8s_get_pods(self, out_file):
        cmd = 'kubectl get pods -o yaml'
        txt = check_output(cmd.split()).decode()
        d = YAML().load(StringIO(txt))  # load() parsing is on the slow side.
        with open(out_file, 'w') as fout:
            json.dump(d, fout)


class Pod:

    def __init__(self, p: dict):
        self.p = p
        assert p['apiVersion'] == 'v1'
        assert p['kind'] == 'Pod'
        assert ' '.join(p.keys()) == 'apiVersion kind metadata spec status'

    @property
    def app_name(self):
        try:
            return self.p['metadata']['labels']['app']
        except KeyError:
            return self.p['metadata']['labels']['job-name']  # for a cron job

    @property
    def pod_id(self):
        return self.p['metadata']['name']

    @property
    def namespace(self):
        return self.p['metadata']['namespace']

    @property
    def node_name(self):
        """What node is this pod currently scheduled on?
        """
        return self.p['spec']['nodeName']

    @property
    def requests(self):
        try:
            container = self.p['spec']['initContainers'][0]
        except KeyError:
            return dict(cpu=None,
                        memory=None)
        r = container['resources']['requests']
        assert ' '.join(r.keys()) == 'cpu memory'
        return r  # e.g. {'cpu': '100m', 'memory': '128Mi'}

    @property
    def phase(self):
        return self.p['status']['phase']

    @property
    def start_time(self):
        return self.p['status']['startTime']


def main(node_name_width=42, verbose=False):
    pods = Pods()
    for item in pods.items:
        pod = Pod(item)
        print(pod.start_time, ' ',
              pod.node_name.ljust(node_name_width),
              node_availability_zone(pod.node_name), ' ',
              pod.pod_id)


if __name__ == '__main__':
    main()
