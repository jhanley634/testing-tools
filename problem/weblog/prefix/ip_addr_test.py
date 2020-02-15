
# Copyright 2020 John Hanley.
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

from problem.weblog.prefix.ip_addr import IpAddr, Prefix, log_dist


class IpAddrTest(unittest.TestCase):

    def test_fmt(self):
        self.assertEqual("00000000", str(IpAddr("0.0.0.0")))
        self.assertEqual("01020304", str(IpAddr("1.2.3.4")))
        self.assertEqual("0a000001", str(IpAddr("10.0.0.1")))
        self.assertEqual("80818283", str(IpAddr("128.129.130.131")))
        self.assertEqual("ffffffff", str(IpAddr("255.255.255.255")))
        self.assertEqual("ffffffff", IpAddr("255.255.255.255").hex())

        self.assertEqual("10.0.1.200", IpAddr("10.0.1.200").decimal())
        self.assertEqual("010.000.001.200", IpAddr("10.0.1.200").decimal03())

    def test_bad_input(self):
        with self.assertRaises(AssertionError):
            IpAddr("2.3.4")

        with self.assertRaises(AssertionError):
            IpAddr("1.2.300.4")

    def test_comparison(self):
        a = IpAddr("1.99.3.4")
        b = IpAddr("1.100.3.4")
        self.assertLessEqual(a.addr, b.addr)
        self.assertLessEqual(a, b)
        self.assertLess(a, b)
        self.assertGreater(b, a)
        self.assertGreaterEqual(b, a)
        self.assertNotEqual(b, a)
        self.assertNotEqual(a, b)
        self.assertEqual(a, a)
        self.assertEqual(b, b)
        self.assertEqual(b, IpAddr("1.100.3.4"))

        self.assertNotEqual(a, 1)
        self.assertNotEqual(a, "1.99.3.4")
        self.assertNotEqual(1, a)
        self.assertNotEqual("1.99.3.4", a)


class CidrPrefixTest(unittest.TestCase):

    def test_prefix(self):
        rtr = IpAddr("10.3.2.1")
        rtr_prefix = Prefix(rtr, 32)
        self.assertEqual("10.3.2.1/32", str(rtr_prefix))

        host = IpAddr("10.3.2.9")
        subnet = Prefix("10.3.2.9/28")
        self.assertEqual("fffffff0", f"{subnet.mask():x}")

        self.assertTrue(rtr in subnet)
        self.assertTrue(host in subnet)

        self.assertTrue(rtr in rtr_prefix)
        self.assertTrue(host not in rtr_prefix)


class LogDistTest(unittest.TestCase):

    def test_log_dist(self):
        rtr = IpAddr("10.3.2.1")
        self.assertEqual(0, log_dist(rtr, rtr))  # It's a metric, so dist to self is zero.
        self.assertEqual(0, log_dist(rtr, IpAddr("10.3.2.1")))

        self.assertEqual(1, log_dist(rtr, IpAddr("10.3.2.0")))
        self.assertEqual(0, log_dist(rtr, IpAddr("10.3.2.1")))
        self.assertEqual(2, log_dist(rtr, IpAddr("10.3.2.2")))
        self.assertEqual(2, log_dist(rtr, IpAddr("10.3.2.3")))
        self.assertEqual(3, log_dist(rtr, IpAddr("10.3.2.4")))
        self.assertEqual(3, log_dist(rtr, IpAddr("10.3.2.5")))
        self.assertEqual(3, log_dist(rtr, IpAddr("10.3.2.6")))
        self.assertEqual(3, log_dist(rtr, IpAddr("10.3.2.7")))
        self.assertEqual(4, log_dist(rtr, IpAddr("10.3.2.8")))
        self.assertEqual(4, log_dist(rtr, IpAddr("10.3.2.9")))
        self.assertEqual(4, log_dist(rtr, IpAddr("10.3.2.15")))
        self.assertEqual(5, log_dist(rtr, IpAddr("10.3.2.16")))
