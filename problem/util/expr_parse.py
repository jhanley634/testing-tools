
from collections import deque
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

        expr = []  # a postfix expression
        stack = deque()  # stuff we've not gotten around to yet
        for token, prec in self._get_tokens():
            prec = self.op_to_precedence.get(self._to_str(token))
            # print(prec, token)
            if isinstance(token, int):
                expr.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                assert stack[-1] != ')', stack  # Prohibit '()', and also ')'.
                while stack and stack[-1] != ')':
                    tok = stack.pop()
                    if tok != '(':
                        expr.append(tok)
            elif prec:
                if len(stack) == 0 or stack[-1] == '(':
                    stack.append(token)
                else:
                    print(8, expr)
                    print(9, stack)
                    while stack and self.op_to_precedence.get(self._to_str(stack[-1]), 99) < prec:
                        expr.append(stack.pop())
            else:
                stack.append(token)

        while stack:
            expr.append(stack.pop())

        return ' '.join(map(self._to_str, expr))

    def _to_str(self, token):
        if isinstance(token, WrapperDescriptor):
            txt = ' UNKNOWN '
            for k, v in self.op_to_fn.items():
                if v == token:
                    txt = k  # e.g. '+' or '*'
            return txt
        else:
            return f'{token}'

    def evaluate_postfix(self, expr: str):
        assert '(' not in expr, expr
        assert ')' not in expr, expr

        stack = []
        for tok in expr.split():
            if tok.isnumeric():
                stack.append(float(int(tok)))
            else:
                op = self.op_to_fn[self._to_str(tok)]
                stack.append(op(stack.pop(),
                                stack.pop()))

        assert 1 == len(stack), (len(stack), stack)
        return stack.pop()
