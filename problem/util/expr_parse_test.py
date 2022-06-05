
# Copyright 2022 John Hanley. MIT licensed.
import unittest

from problem.util.expr_parse import ExprParser, _div


def _munge_exp(s: str) -> str:
    """Adjusts the notation for exponentiation."""
    return s.replace('^', ' ** ')


class ExprParserTest(unittest.TestCase):

    def test_get_token(self):
        p = ExprParser('3 + ((7 - 5) / 2)')
        self.assertEqual([('(', None),
                          (3, None),
                          (float.__add__, 1),
                          ('(', None),
                          ('(', None),
                          (7, None),
                          (float.__sub__, 1),
                          (5, None),
                          (')', None),
                          (_div, 2),
                          (2, None),
                          (')', None),
                          (')', None),
                          ], list(p._get_tokens()))

    expressions = [
        ('1+2', '1 2 +'),
        ('1+2+3', '1 2 3 + +'),
        ('(1+2)+3', '1 2 + 3 +'),
        ('1+(2+3)', '1 2 3 + +'),
        ('8-3', '8 3 -'),
        ('8/2', '8 2 /'),
        ('2^3', '2 3 ^'),
        ('1+2^3', '1 2 3 ^ +'),
        ('1+2^3+4+5*6+7', '1 2 3 ^ 4 5 6 * 7 + + + +'),
        ('1+2^(3+4)+5*6+7', '1 2 3 4 + ^ 5 6 * 7 + + +'),
        ('12*3', '12 3 *'),
        ('3^(20/5)-1081', '3 20 5 / ^ 1081 -'),
        ('2*3', '2 3 *'),
        ('2*3*4', '2 3 4 * *'),
        ('1+2*3*4', '1 2 3 4 * * +'),
        ('1+2*3*4+5', '1 2 3 4 * * 5 + +'),
        ('2*3*4+5', '2 3 4 * * 5 +'),
        ('1+2+3*4+5', '1 2 3 4 * 5 + + +'),
        ('1+(2+3)*4+5', '1 2 3 + 4 * 5 + +'),
        ('1+(2+3)*(4+5)', '1 2 3 + 4 5 + * +'),
        ('1+((2+3)*4+5)*6', '1 2 3 + 4 * 5 + 6 * +'),
        ('1+(2+(3*4+5))*6', '1 2 3 4 * 5 + + 6 * +'),
        ('2 * 3/7', '2 3 7 / *'),
        ('(1000 / 10) / 20', '1000 10 / 20 /'),  # conventional L->R order
        ('1000 / (10 / 20)', '1000 10 20 / /'),  # how paren-free expression parses
        ('3 + 0.14', '3 0.14 +'),
        ('3 + .14', '3 0.14 +'),
        ('4e5', '400000'),
        ('5.123e6', '5123000.0'),
        ('1e16', '1e+16'),
        ('(0 - 1) * .0', '0 1 - 0 *'),
        ('.123456789e-320', '1.235e-321'),  # subnorm
        ('1.6180339887498948482045868343656381177203091798057628621354486227', '1.618033988749895'),
        ('6.674e-11 * 1 * 5.97e24 / 6.371e6^2', '6.674e-11 1 5.97e+24 6371000.0 2 ^ / * *'),
    ]

    def test_parse(self):
        for infix, postfix in self.expressions:

            n = eval(_munge_exp(infix))
            self.assertAlmostEqual(n, ExprParser('1').evaluate_postfix(postfix), places=14)

            self.assertEqual(postfix, ExprParser(infix).to_postfix())
