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

from contextlib import contextmanager
import os
import subprocess


@contextmanager
def open_sorted_file(infile):
    temp_sorted_file = f'/tmp/find_longest_prefixes_{os.getpid()}.txt'
    cmd = f'sort < {infile}  > {temp_sorted_file}'
    subprocess.check_call(cmd, shell=True)
    try:
        with open(temp_sorted_file) as fin:
            yield fin
    finally:
        os.unlink(temp_sorted_file)


def verify_ordered(fin):
    """Pass-through generator, verifies the input file is sorted."""
    # For example, `$ env LC_COLLATE=C sort` might differ from python ordering.
    prev = ''
    for line in fin:
        assert prev <= line, line
        yield line


def longest_prefix_match(a, b):
    i = len(a)
    if (len(b) >= i
            and a == b[:i]):  # Fast path, new line B doesn't change the prefix A.
        return i

    i = 0  # Just in case A & B are the empty string.
    for i in range(min(map(len, (a, b)))):
        if a[i] != b[i]:
            assert a[:i] == b[:i]
            return i
    assert a[:i] == b[:i]
    return i


def longest_prefixes(infile):
    """Given a set of redis keys, or syslog messages, find the generating prefixes.

    For example:
        redis.set(f'bar-{guid}')
        redis.set(f'bazz-{guid}')
    would elicit two prefixes: ['bar-', 'bazz-'].
    Other services, such as syslog, would work similarly.
        syslog(f'bar-{guid} at {timestamp}')
        syslog(f'bazz-{guid} at {timestamp}')
    """

    assert ' ' not in infile, infile  # Why would we want quoting craziness?
    assert os.path.isfile(infile), infile
    pfx, prev_i = None, 0
    with open_sorted_file(infile) as fin:
        for line in verify_ordered(fin):
            line = line.rstrip()
            if len(line) == 0:
                continue  # Else an empty-string prefix could explain ALL lines.
            if pfx is None:
                pfx = line
                prev_i = len(line)
            i = longest_prefix_match(pfx, line)
            if i < prev_i:
                yield pfx
                pfx = line
            else:
                pfx = line[:i]
            prev_i = i
        yield pfx
