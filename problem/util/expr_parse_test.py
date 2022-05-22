
import unittest

from problem.util.expr_parse import ExprParser


class ExprParserTest(unittest.TestCase):

    def test_parse(self):
        expressions = [
            ('1+2', '1 2 +'),
            ('1+2+3', '1 2 + 3 +'),
            ('(1+2)+3', '1 2 + 3 +'),
            ('1+(2+3)', '1 2 3 + +'),
            ('1+2+3*4+5', '1 2 + 3 4 * + 5 +'),
            ('1+(2+3)*4+5', '1 2 3 + 4 * + 5 +'),
        ]
        for infix, postfix in expressions:

            self.assertEqual(eval(infix), ExprParser('1').evaluate_postfix(postfix))

            self.assertEqual(postfix, ExprParser(infix).to_postfix())
