
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
    ]

    def test_parse(self):
        for infix, postfix in self.expressions:

            self.assertEqual(eval(_munge_exp(infix)), ExprParser('1').evaluate_postfix(postfix))

            self.assertEqual(postfix, ExprParser(infix).to_postfix())
