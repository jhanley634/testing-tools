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


import click

from problem.weblog.prefix.ip_addr import IpAddr, Prefix, log_dist


MAX_ACL_ENTRIES = 60  # Some amazon security groups, e.g. impose this quota limit.


def _get_distances(acl):
    prev = acl[-1]  # We anticipate high distance between first and last
    for pfx in acl:
        yield log_dist(prev.ip, pfx.ip)
        prev = pfx


def compress(ips, max_acl_entries=MAX_ACL_ENTRIES):
    # Sorting by IP brings together addresses that belong in a common prefix.
    acl = [Prefix(ip, 32)
           for ip in sorted(ips)]

    # Need to merge together this many neighboring IPs.
    n = max(0, len(acl) - max_acl_entries)

    while n > 0:
        distances = list(_get_distances(acl))
        print(distances)
        acl = _get_smaller_acl(acl, n, min(distances))
        n = max(0, len(acl) - max_acl_entries)

    print("\n".join(map(str, acl)))


def _get_smaller_acl(acl, n, min_dist):
    ret = []
    prev = None
    for pfx in acl:
        if (n > 0
                and prev
                and log_dist(prev.ip, pfx.ip) <= min_dist):
            n -= 1
            pfx = _merge(ret.pop(), pfx.ip)
        ret.append(pfx)
        prev = pfx
    return ret


def _merge(pfx, ip):
    while ip not in pfx:
        pfx.masklen -= 1
    return Prefix(pfx.ip, pfx.masklen)  # This clears the hostpart.


@click.command()
@click.option("--infile", required=True)
def main(infile):
    with open(infile) as fin:
        compress(map(IpAddr, fin.readlines()), 23)


if __name__ == "__main__":
    main()
