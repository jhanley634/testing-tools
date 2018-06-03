#! /usr/bin/env python3

# Copyright 2018 John Hanley.
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

"""Rasterizes input text via HTML rendering to produce an output PNG."""

from pathlib import Path
import os

import click
import imgkit


def _get_html(text):
    ttf = _get_static() / 'tangerine.ttf'
    font_src = f"src: url('{ttf}');"
    return ("""<!DOCTYPE html>
<html>
<head>
  <style type="text/css">
  @font-face {
    font-family: 'Tangerine';
    """ + font_src + """
    font-weight: normal;
    font-style: normal;
  }
  body {
    margin: 0;
    padding: 0;
    font-size: 24px;
    font-family: 'sans serif';
  }
  p {
    font-family: 'Tangerine';
    margin: 0;
    padding: 0;
  }
  </style>
</head>

<body>
  <p>
    """ + text + """
  </p>
</body>
</html>
""")


def _get_static():
    d = Path(os.path.dirname(os.path.abspath(__file__)))
    return d / 'static'


@click.command()
@click.argument('message_text', default="How vexingly quick daft zebras jump!")
@click.option('--directory', default=os.path.expanduser('~/Desktop'))
@click.option('--file', default='text.png')
@click.option('--width', default=400)  # imgkit would default to 1024
def render(message_text, directory, file, width):
    """Rasterizes input text via HTML rendering to an output PNG."""
    fspec = Path(directory) / file
    options = {'width': width}
    imgkit.from_string(_get_html(message_text),
                       fspec, css=None, options=options)


if __name__ == '__main__':
    render()
