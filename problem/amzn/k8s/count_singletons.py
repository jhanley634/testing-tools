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


def count_singletons_per_node():
    """Reports on assignment of singletons to k8s nodes.

    A singleton deployment is inherently fragile. We count how many
    singletons each node has, as an aid to balancing the workload.

    Imagine a given node N has twice as many singletons as neighboring nodes,
    and N fails. Then twice as many user-visible failures occurred as necessary.
    Ideally the max-per-node would be no more than 1 greater than min-per-node.
    """


if __name__ == '__main__':
    count_singletons_per_node()
