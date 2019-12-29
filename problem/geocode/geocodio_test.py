
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

import unittest

from problem.geocode.geocodio import GeocodeCache, GeocodioGeocoder


class GeocodioTest(unittest.TestCase):

    def test_geocode(self):
        with GeocodioGeocoder() as geo:
            self.assertEqual(
                dict(lat=38.884999,
                     lng=-77.094806,
                     formatted_addr='1020 N Highland St, Arlington, VA 22201'),
                geo.code('1020 North Highland Street unit 1109'
                         ' Arlington, Virginia  22201'))

    def test_cache(self):
        c = GeocodeCache()
        with GeocodioGeocoder() as geo:
            c.insert_text_files(geo.log_dir)
