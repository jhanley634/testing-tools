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

from pathlib import Path
import subprocess

import boto3
import click


class S3Names:

    def __init__(self, bucket, directory):
        self.bucket_name = bucket
        self.directory = Path(directory)
        assert self.directory.exists(), directory

    @property
    def _cache_file(self):
        PREFIX = 'bucket_'  # Arbitrary. This simply sorts them together.
        return Path(f'{self.directory}/{PREFIX}{self.bucket_name}.txt')

    def _tail1(self, file):
        return subprocess.check_output(['tail', '-1', file])

    def _get_names(self, start_after):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(self.bucket_name)
        for obj in bucket.objects.all(start_after=start_after):
            print(type(obj), dir(obj))
            yield obj.key

    def store_names(self):
        start_after = ''
        f = self._cache_file
        if f.exists() and f.stat().st_size > 0:
            start_after = self._tail1(f)
        with open(f, 'a') as fout:
            for name in self._get_names(start_after):
                fout.write(f'{name}\n')


@click.command()
@click.option('--bucket', required=True,
              help='name of S3 bucket to read')
@click.option('--directory', default='/tmp',
              help='directory in which results are cached across runs')
def main(bucket, directory):
    s3n = S3Names(bucket, directory)


if __name__ == '__main__':
    main()
