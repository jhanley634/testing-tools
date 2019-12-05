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

import boto3


def _get_bucket_names():
    client = boto3.client('s3', region_name='us-west-2')
    buckets = client.list_buckets()['Buckets']
    return sorted(map(itemgetter('Name'), buckets))


class BucketWalker:

    def __init__(self, region_name='us-west-2'):
        self.client = boto3.client('s3', region_name=region_name)

    def _report_on(self, bucket_name, out_dir=Path('/tmp/bucket')):
        os.makedirs(out_dir, exist_ok=True)

        paginator = self.client.get_paginator('list_objects')
        prev = ''
        for page in paginator.paginate(Bucket=bucket_name):
            for item in page['Contents']:
                key, mtime, size = map(item.get, ('Key', 'LastModified', 'Size'))
                print(mtime, f'{size:8d}   {bucket_name}/{key}')
                assert key > prev, key
                prev = key


def report():
    # print('\n'.join(_get_bucket_names()))
    bw = BucketWalker()
    print(list(map(bw._report_on, _get_bucket_names())))


if __name__ == '__main__':
    report()
