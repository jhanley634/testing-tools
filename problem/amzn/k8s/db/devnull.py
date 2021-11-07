
from functools import wraps
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
import os
import sys


def devnull(func):
    """Decorator to silence a chatty function.

    Errors sent to stderr will still be displayed normally.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        tty = sys.stdout
        with open(os.devnull, 'w') as sys.stdout:

            func(*args, **kwargs)  # Shhhh! Be very very quiet.

        sys.stdout = tty  # Now we're back to normal.

    return wrapper
