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

from collections import defaultdict
from functools import partial
from hashlib import sha3_256

"""Demonstrates why one should fold in XORed bits when truncating."""


def _truncating_hash(output_bits, prefix, msg):
    return sha3_256(f'{prefix}{msg}'.encode()).hexdigest()[:output_bits // 4]


def _half_length_hash(output_bits, prefix, msg):
    out_nybbles = output_bits // 4
    digest = sha3_256(f'{prefix}{msg}'.encode()).hexdigest()
    while len(digest) > out_nybbles:
        n = len(digest) // 2
        first, second = digest[:n], digest[n:]  # cut digest into halves
        combined = int(first, 16) ^ int(second, 16)  # XOR combine them
        digest = f'{combined:0{out_nybbles}x}'  # lpad with zeros
    return digest


def hash_fn_factory(hash_fn, output_bits=128, prefix='42', verbose=True):
    if verbose:
        print(output_bits)
    assert output_bits % 4 == 0, f'Request int number of nybbles: {output_bits}'
    return partial(hash_fn, output_bits, prefix)


def digest_generator(hash_fn, bits=8):
    for i in range(2 ** bits):
        yield hash_fn(str(i))


def count_collisions(digest_gen):
    seen = defaultdict(int)
    for digest in digest_gen:
        seen[digest] += 1

    for digest, count in seen.items():
        if count > 1:
            print(count, digest)

    return sum(cnt - 1
               for cnt in seen.values())


def simple_shrinking():
    for out_bits in range(24, 0, -4):
        total = count_collisions(digest_generator(
            hash_fn_factory(_truncating_hash, out_bits, '43'),
            8))
        print(f'{total} collisions')


def binary_shrinking():
    for out_bits in [128, 64, 32, 16, 8, 4]:
        total = count_collisions(digest_generator(
            hash_fn_factory(_half_length_hash, out_bits, '43'),
            8))
        print(f'{total} collisions')


def run_experiment():
    print('simple:')
    simple_shrinking()
    print('\nbinary:')
    binary_shrinking()


if __name__ == '__main__':
    run_experiment()
