
from enum import Enum, auto
import re


def _get_op_pairs():
    yield from {
        '+': (3, float.__add__),
        '*': (2, float.__mul__),
        '^': (1, float.__pow__),
    }.items()


class ExprParser:

    op_to_precedence = {
        op: pair[0] for op, pair in _get_op_pairs()}
    op_to_fn = {
        op: pair[1] for op, pair in _get_op_pairs()}

    sane_charset_re = re.compile(r'^[()+*^0-9 ]+$')

    def __init__(self, infix: str):
        assert self.sane_charset_re.search(infix), infix
        self.infix = infix
        # self.infix = infix.replace(' ', '')

    def _get_tokens(self):
        for ch in self.infix:
            fn = self.op_to_fn.get(ch)
            if ch == ' ':
                pass
            elif fn:
                yield fn, self.op_to_precedence[ch]
            elif ch.isnumeric():
                yield int(ch), 0
            elif ch in '()':
                yield ch, 0
            else:
                raise

    def to_postfix(self) -> str:
        return ''
