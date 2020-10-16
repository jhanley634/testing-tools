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
import csv
import subprocess

from tqdm import tqdm
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
        return Path(f'{self.directory}/{PREFIX}{self.bucket_name}.csv')

    @staticmethod
    def _tail1(file):
        return subprocess.check_output(['tail', '-1', file]).decode().rstrip()

    @staticmethod
    def _third_field(line: str):
        return line.split(',', 2)[-1]

    def _get_size_stamp_names(self, start_after):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(self.bucket_name)
        for obj in bucket.objects.all().filter(Marker=start_after):
            yield obj.size, obj.last_modified, obj.key

    def store_names(self):
        start_after = ''
        f = self._cache_file
        if f.exists() and f.stat().st_size > 0:
            start_after = self._third_field(self._tail1(f))
        else:
            f.write_text('size,updated,name\n')
        with open(f, 'a') as fout:
            sheet = csv.writer(fout)
            for row in tqdm(self._get_size_stamp_names(start_after)):
                sheet.writerow(row)


@click.command()
@click.option('--bucket', required=True,
              help='name of S3 bucket to read')
@click.option('--directory', default='/tmp',
              help='directory in which results are cached across runs')
def main(bucket, directory):
    s3n = S3Names(bucket, directory)
    s3n.store_names()


if __name__ == '__main__':
    main()
