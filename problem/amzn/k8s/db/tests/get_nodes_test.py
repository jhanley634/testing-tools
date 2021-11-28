
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
import unittest

from problem.amzn.k8s.db.devnull import devnull
from problem.amzn.k8s.db.get_nodes import Node, Nodes, display_image_size, main

# Usage:
#   cd ../testing-tools/ && python -m unittest problem/amzn/k8s/db/tests/*_test.py
#
#   rm -f /tmp/nodes.yaml &&
#   coverage erase && coverage run -m unittest problem/amzn/k8s/db/tests/*_test.py &&
#   coverage report && coverage html


class GetNodesTest(unittest.TestCase):

    nodes = Nodes()

    def test_nodes(self):
        self.assertGreaterEqual(len(self.nodes.items), 25)

    @devnull
    def test_exercise_main(self):
        main(verbose=True)

        node = Node(self.nodes.items[0])
        display_image_size(node)
        self.assertGreaterEqual(node.allocatable_kib_ram, 15_806_488)
