
import geopy.distance


class SdSpace:
    """San Diego space is a metric space that maps lat, longs of
    the continental 48, originally located in quadrant II, to
    a portion of quadrant I, with San Diego somewhat near the origin."""

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
        self.x = lng - self.ORIGIN_LNG
        self.y = lat - self.ORIGIN_LAT

    def lng(self):
        return self.x + self.ORIGIN_LNG

    def lat(self):
        return self.y + self.ORIGIN_LAT

    def distance(self, other):
        """Great circle distance in meters between two geographic points."""
        p1 = (self.y, self.x)
        p2 = (other.y, other.x)
        return geopy.distance.distance(p1, p2).meters
