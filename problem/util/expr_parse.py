
from collections import deque
import re

WrapperDescriptor = type(object.__init__)


def _get_op_pairs():
    yield from {
        '(': (0, None),
        '+': (1, float.__add__),
        '*': (2, float.__mul__),
        '^': (3, float.__pow__),
    }.items()


class ExprParser:

    op_to_precedence = {
        op: pair[0] for op, pair in _get_op_pairs()}
    op_to_fn = {
        op: pair[1] for op, pair in _get_op_pairs()}

    sane_charset_re = re.compile(r'^[()+*^0-9 ]+$')

    def __init__(self, infix: str):
        assert self.sane_charset_re.search(infix), infix
        assert (infix.count('(')
                == infix.count(')')), infix
        self.infix = f'({infix})'

    def _get_tokens(self):
        for ch in self.infix:
            fn = self.op_to_fn.get(ch)
            if ch == ' ':
                pass
            elif fn:
                yield fn, self.op_to_precedence[ch]
            elif ch.isnumeric():
                yield int(ch), None
            elif ch in '()':
                yield ch, None
            else:
                raise

    def to_postfix(self) -> str:
        # based on https://algotree.org/algorithms/stack_based/infix_to_postfix
        expr = []  # a postfix expression
        stack = deque()  # stuff we've not gotten around to yet
        for token, prec in self._get_tokens():
            prec = self.op_to_precedence.get(self._to_str(token))
            # print(prec, token)
            if token == '(':
                stack.append(token)
            elif token == ')':
                while stack[-1] != '(':
                    expr.append(stack.pop())
                tok = stack.pop()
                assert tok == '('
            elif prec:
                while self.op_to_precedence[self._to_str(stack[-1])] > prec:
                    expr.append(stack.pop())
                stack.append(token)
            else:
                assert isinstance(token, int), token
                expr.append(token)

        assert 0 == len(stack), stack

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
