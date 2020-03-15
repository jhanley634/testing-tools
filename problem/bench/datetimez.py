
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

import datetime as dt


class Datetimez(dt.datetime):
    """Supports _always_ using UTC."""

    utc = dt.timezone.utc

    @classmethod
    def from_(cls, datetime: dt.datetime):
        return datetime.replace(tzinfo=cls.utc)

    @classmethod
    def fromisoformat(cls, date_string: str):
        assert date_string.endswith("+0000"), date_string
        return (super().fromisoformat(date_string.replace("+0000", ""))
                .replace(tzinfo=cls.utc))

    @classmethod
    def fromtimestamp(cls, sec):
        return super().fromtimestamp(sec).replace(tzinfo=cls.utc)

    @classmethod
    def now(cls):
        return super().now().replace(tzinfo=cls.utc)

    @classmethod
    def strptime(cls, date_string, format):
        return super().strptime(date_string, format).replace(tzinfo=cls.utc)
