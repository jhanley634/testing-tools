
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

import unittest
import uuid


def get_guid() -> str:
    """Generates a random GUID."""
    return str(uuid.uuid4())


class ZeroUuid4Test(unittest.TestCase):

    def test_zero_uuid4(self, num_trials=1e3):
        length = len(get_guid())  # 36
        min_nyb = ['~' for _ in range(length)]
        max_nyb = [' ' for _ in range(length)]

        for _ in range(int(num_trials)):
            for i in range(length):
                g = get_guid()
                min_nyb[i] = min(min_nyb[i], g[i])
                max_nyb[i] = max(max_nyb[i], g[i])

        self.assertEqual('00000000-0000-4000-8000-000000000000', ''.join(min_nyb))
        self.assertEqual('ffffffff-ffff-4fff-bfff-ffffffffffff', ''.join(max_nyb))

    def test_zero(self):
        g0 = uuid.UUID('00000000-0000-4000-8000-000000000000')
        g1 = uuid.UUID('00000000-0000-4000-bfff-ffffffffffff')

        self.assertEqual(0x10002, g0.int / 2 ** 62.)
        self.assertEqual(0x10003, g1.int // 2 ** 62.)

        # Version is binary 0100, that is, 4.
        self.assertEqual(0x4000, g0.time_hi_version)
        self.assertEqual(0x4000, g1.time_hi_version)

        # Set the variant to RFC 4122.
        # int &= ~(0xc000 << 48)
        # int |= 0x8000 << 48
        # that is, top two bits are 10.
        self.assertEqual(0x80, g0.clock_seq_hi_variant)
        self.assertEqual(0xbf, g1.clock_seq_hi_variant)
