#! /usr/bin/env python

# Copyright 2019 John Hanley.
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
import socket
import struct
import sys


def parse_proc_net_tcp(in_file):
    try:
        in_file = Path(in_file)
        fin = open(in_file)
    except TypeError:
        fin = in_file  # Caller must have opened a file handle already.
    yield from _parse(fin)


def _parse(fin):
    for i, line in enumerate(fin):
        words = line.split()
        if i == 0:
            heading = ('sl local_address rem_address st tx_queue rx_queue'
                       ' tr tm->when retrnsmt uid timeout inode')
            assert 'sl' == words[0], words
            assert heading == ' '.join(words), words
            continue  # Skip heading.
        sl, local, remote, *_ = words
        assert f'{i - 1}:' == sl, sl
        yield _ip_port(local) + _ip_port(remote)


def _ip_port(ip_port):
    hex_ip, port = ip_port.split(':')
    return [_dotted_quad(hex_ip), int(port, 16)]


def _dotted_quad(hex_ip):
    addr = int(hex_ip, 16)
    addr = struct.pack('<I', addr)
    return socket.inet_ntoa(addr)


def netstat_an(in_file):
    for row in parse_proc_net_tcp(in_file):
        yield ' '.join(map(str, row))


if __name__ == '__main__':
    print('\n'.join(netstat_an(sys.stdin)))
