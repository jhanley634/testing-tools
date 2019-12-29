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

from operator import itemgetter
from pathlib import Path
import os

import click

import boto3


def _get_bucket_names():
    client = boto3.client('s3', region_name='us-west-2')
    buckets = client.list_buckets()['Buckets']
    return sorted(map(itemgetter('Name'), buckets))


class BucketWalker:

    def __init__(self, region_name='us-west-2', out_dir=Path('/tmp/bucket')):
        self.client = boto3.client('s3', region_name=region_name)
        self.out_dir = out_dir
        os.makedirs(out_dir, exist_ok=True)
        with open(out_dir / 'list.txt', 'w') as fout:
            fout.write('\n'.join(_get_bucket_names()))

    def walk(self, bucket_name, start_after=''):
        # Vaguely similar to os.walk().

        paginator = self.client.get_paginator('list_objects_v2')
        prev = ''
        for page in paginator.paginate(Bucket=bucket_name, StartAfter=start_after):
            for item in page.get('Contents', []):
                key, mtime, size = map(item.get, ('Key', 'LastModified', 'Size'))
                yield mtime, size, key
                assert key > prev, key  # Verify that the API always offers ordered keys.
                prev = key

    def _report_on(self, bucket_name):
        for mtime, size, key in self.walk(bucket_name):
            print(mtime, f'{size:8d}  {bucket_name}/{key}')

    def report_content_of_all_buckets(self):
        list(map(self._report_on, _get_bucket_names()))

    def _walk_dirs(self, bucket_name):
        for mtime, size, key in self.walk(bucket_name):
            dirs = key.split('/')
            assert len(dirs) > 0
            yield size, '/'.join(dirs[:-1]), dirs[-1]

    def du(self, bucket_name):
        cur, dir_total, grand_total = None, Counter(), Counter()
        for size, dir, file in self._walk_dirs(bucket_name):
            cur = cur or dir
            if cur != dir:
                print(f'{dir_total.n:6d} {dir_total.size:9d}   {cur}')
                grand_total.add(dir_total)
                dir_total = Counter()
                cur = dir
            dir_total.add(size)
        print(f'{dir_total.n:6d} {dir_total.size:9d}   {cur}')
        grand_total.add(dir_total)
        return grand_total


class Counter:
    def __init__(self):
        self.n = 0
        self.size = 0

    def add(self, size):
        if isinstance(size, Counter):
            self.n += size.n
            self.size += size.size
        else:
            self.n += 1
            self.size += size

    def __str__(self):
        return f'{self.n:6d} {self.size:9d}'


@click.command()
@click.option('--bucket')
def main(bucket):
    if bucket == 'all':
        for bucket in _get_bucket_names():
            print(BucketWalker().du(bucket))
        else:
            print(BucketWalker().du(bucket))
    else:
        BucketWalker().report_content_of_all_buckets()


if __name__ == '__main__':
    main()
