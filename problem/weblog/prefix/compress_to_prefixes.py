#! /usr/bin/env python

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


from collections import deque

import click

from problem.weblog.prefix.ip_addr import IpAddr, Prefix, log_dist


MAX_ACL_ENTRIES = 60  # Some amazon security groups, e.g. impose this quota limit.


def compress(ips, max_acl_entries=MAX_ACL_ENTRIES):
    # This ordering brings together IPs that belong in a common prefix.
    acl = deque(sorted(Prefix(ip, 32)
                       for ip in ips))

    while len(acl) > max_acl_entries:
        _greedy_merge(acl)

    print("")
    print("\n".join(map(str, acl)))


def _greedy_merge(acl):
    assert len(acl) >= 2
    a = acl.popleft()
    b = acl[0]
    print("\n", a, b, end="\t")
    b.masklen = min(a.masklen, b.masklen)
    while a.ip not in b:
        b.masklen -= 1
    b = Prefix(b.ip, b.masklen)  # This clears the hostpart.
    print(log_dist(a.ip, b.ip), f"{b.mask():x}")



@click.command()
@click.option("--infile", required=True)
def main(infile):
    with open(infile) as fin:
        compress(map(IpAddr, fin.readlines()), 25)


if __name__ == "__main__":
    main()
