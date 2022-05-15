
import re

WrapperDescriptor = type(object.__init__)


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

        def to_str(token):
            if isinstance(token, WrapperDescriptor):
                txt = ' UNKNOWN '
                for k, v in self.op_to_fn.items():
                    if v == token:
                        txt = k  # e.g. '+' or '*'
                return txt
            else:
                return f'{token}'

        tokens = [to_str(token)
                  for token, _ in self._get_tokens()]
        return ' '.join(tokens)
