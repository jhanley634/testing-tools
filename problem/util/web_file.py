
# Copyright 2021 John Hanley.
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
from hashlib import sha3_224
from pathlib import Path

import requests


class WebFile:
    """Offers cached access to files available from the web."""

    def __init__(self, url, fname=None, temp=Path('/tmp/webfile/')):
        self.url = url
        pfx = 'web' + sha3_224(url.encode()).hexdigest()[:4]
        fname = fname or Path(url).name  # e.g. 'foo.csv'
        self.fspec = temp / f'{pfx}_{fname}'

    def file(self) -> str:
        if not self.fspec.exists():
            resp = requests.get(self.url)
            resp.raise_for_status()
            self.fspec.parent.mkdir(exist_ok=True)
            with open(self.fspec, 'wb') as fout:
                fout.write(resp.content)

        return f'{self.fspec}'
