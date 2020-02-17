
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

from functools import lru_cache, total_ordering
import re


@total_ordering
class IpAddr:
    """Models an IPv4 32-bit address."""

    dotted_quad_re = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

    def __init__(self, dotted_quad):
        if isinstance(dotted_quad, IpAddr):
            dotted_quad = dotted_quad.decimal()
        m = self.dotted_quad_re.search(dotted_quad)
        assert m, dotted_quad  # Input must be a valid decimal IPv4 address.
        four_bytes = map(int, dotted_quad.split("."))
        self.addr = self._combine(four_bytes)

    @staticmethod
    def _combine(nums):
        acc = 0
        for num in nums:
            assert 0 <= num < 0x100, num
            acc *= 0x100
            acc += num
        return acc

    def _get_addr_bytes(self):
        a = self.addr
        bytes = []
        for _ in range(4):
            bytes.append(a & 0xFF)
            a //= 0x100
        return reversed(bytes)

    def __str__(self):
        return f"{self.addr:08x}"

    def hex(self):
        return self.__str__()

    def decimal(self):
        return ".".join(map(str, self._get_addr_bytes()))

    def decimal03(self):
        """Returns e.g. 001.002.003.004. Lexical and numeric collations match."""
        return ".".join([f"{b:03d}"
                         for b in self._get_addr_bytes()])

    # from https://docs.python.org/3/library/functools.html#functools.total_ordering
    @staticmethod
    def _is_valid_operand(other):
        return (hasattr(other, "addr")
                and isinstance(other.addr, int)
                and other.addr >= 0)

    @classmethod
    def _invalid(cls, other):
        if cls._is_valid_operand(other):
            return None  # We can keep going.
        else:
            return NotImplemented  # Prohibit further processing.

    def __eq__(self, other):
        return self._invalid(other) or self.addr == other.addr

    def __lt__(self, other):
        return self._invalid(other) or self.addr < other.addr


@total_ordering
class Prefix:
    """Models an IPv4 CIDR prefix: 32-bit address + mask."""

    def __init__(self, ip: IpAddr, masklen=None):
        if isinstance(ip, str) and "/" in ip:
            ip, masklen = ip.split("/")
        self.masklen = int(masklen)
        assert 0 <= self.masklen <= 32, masklen
        self.ip = IpAddr(ip)
        self.ip.addr &= self.mask()  # Canonicalize. Host part must be all zero.

    def __str__(self):
        return self.ip.decimal() + f"/{self.masklen}"

    @staticmethod
    @lru_cache()
    def _mask(masklen: int):
        # net_bits = masklen  # network part, e.g. 24 in a class C
        # host_bits = 32 - net_bits  # host part, e.g. 8 in a class C
        net_mask = 0
        bit_val = 2 ** 32  # Start with MSB.
        for _ in range(masklen):
            bit_val //= 2  # Right shift one position.
            net_mask |= bit_val
        return net_mask

    def mask(self):
        return self._mask(self.masklen)

    def __contains__(self, item: IpAddr):
        a1 = self.ip.addr & self.mask()
        a2 = item.addr & self.mask()
        return a1 == a2

    @staticmethod
    def _is_valid_operand(other):  # Other is a prefix that has an IP, and a mask.
        return (hasattr(other, 'ip')
                and IpAddr._is_valid_operand(other.ip)
                and hasattr(other, 'masklen')
                and 0 <= other.masklen <= 32)

    @classmethod
    def _invalid(cls, other):
        if cls._is_valid_operand(other):
            return None  # We can keep going.
        else:
            return NotImplemented  # Prohibit further processing.

    def __eq__(self, other):
        return self._invalid(other) or (self.ip.addr, self.masklen) == (other.ip.addr, other.masklen)

    def __lt__(self, other):
        return self._invalid(other) or (self.ip.addr, self.masklen) < (other.ip.addr, other.masklen)


def log_dist(a: IpAddr, b: IpAddr):
    """Finds the distance beween IPs, according to a logarithmic distance metric."""

    prefix = Prefix(b, 32)
    while (prefix.masklen > 0
           and a not in prefix):
        assert b in prefix, (b, prefix)
        prefix.masklen -= 1

    assert b in prefix, (b, prefix)
    assert a in prefix, (a, prefix)
    assert 0 <= prefix.masklen <= 32

    log_distance = 32 - prefix.masklen
    return log_distance
