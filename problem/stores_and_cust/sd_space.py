
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

import geopy.distance


class SdSpace:
    """San Diego space is a metric space that maps lat, longs of
    the continental 48, originally located in quadrant II, to
    a portion of quadrant I, with San Diego somewhat near the origin.
    Degrees are converted to a number that approximately corresponds to meters.
    """

    X_SCALE = 4_149_754 / 44.791  # meters per degree of longitude (SD->Miami)

    Y_SCALE = 1_710_540 / 23.610  # meters per degree of latitude (SD->Seattle)

    ORIGIN_LAT = 24
    """24 degrees N latitude,
    which accommodates the Florida Keys.
    We choose to ignore much of Mexico and points farther south."""

    ORIGIN_LNG = -125
    """125 degrees W longitude,
    which accommodates Ozette Island in Washington state.
    We choose to ignore Juneau and other points to the west."""

    CANADIAN_BORDER = 49
    """49th parallel, which accommodates nearly all of Minnesota."""

    MAINE = -65
    """65 degrees W longitude, which accomodates all of Maine."""

    def __init__(self, lat, lng):
        if (lat < self.ORIGIN_LAT
                or lat > self.CANADIAN_BORDER
                or lng < self.ORIGIN_LNG
                or lng > self.MAINE):
            raise ValueError(f'coord ({lat}, {lng}) out of bounds')
        self.x = int((lng - self.ORIGIN_LNG) * self.X_SCALE)
        self.y = int((lat - self.ORIGIN_LAT) * self.Y_SCALE)

    def lng(self):
        return self.x / self.X_SCALE + self.ORIGIN_LNG

    def lat(self):
        return self.y / self.Y_SCALE + self.ORIGIN_LAT

    def distance(self, other):
        """Great circle distance in meters between two geographic points."""
        p1 = (self.lat(), self.lng())
        p2 = (other.lat(), other.lng())
        return geopy.distance.distance(p1, p2).meters
