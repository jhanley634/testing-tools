
import unittest

from problem.util.expr_parse import ExprParser


def _munge_exp(s: str) -> str:
    """Adjusts the notation for exponentiation."""
    return s.replace('^', ' ** ')


class ExprParserTest(unittest.TestCase):

    def test_parse(self):
        expressions = [
            ('1+2', '1 2 +'),
            ('1+2+3', '1 2 3 + +'),
            ('(1+2)+3', '1 2 + 3 +'),
            ('1+(2+3)', '1 2 3 + +'),
            # ('2^3', '2 3 ^'),
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
        for infix, postfix in expressions:

            self.assertEqual(eval(_munge_exp(infix)), ExprParser('1').evaluate_postfix(postfix))

            self.assertEqual(postfix, ExprParser(infix).to_postfix())
