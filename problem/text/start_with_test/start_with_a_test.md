
---
author: John Hanley
title: Start with a test!
date: Tuesday, May 11th, 2021
---


# Start with a test!

(also: DbC)

<!--- Copyright 2021, John Hanley
MIT licensed -- see end.
--->


# puzzler

    #include <stdio.h>
    main() {
      long long P = 1,
                E = 2,
                T = 5,
                A = 61,
                L = 251,
                N = 3659,
                R = 271173410,
                G = 1479296389,
                x[] = { G * R * E * E * T ,
                        P * L * A * N * E * T };
      puts((char*)x);
    }

\hfill {\tiny --- https://codegolf.stackexchange.com/questions/22533}

# answer

    x[] = { G * R * E * E * T ,
            P * L * A * N * E * T };
    puts((char*)x);

    (lldb) p/x x
    (long long [2]) $1 = ([0] = 0x6f57206f6c6c6548,
                          [1] = 0x0000000021646c72)
    (lldb) x/16c &x
    0x7ffeefbff7a0: Hello World!\0\0\0\0
    (lldb) x &x[1]
    0x7ffeefbff7a8: 72 6c 64 21 00 00 00 00  rld!....


# hello C
\blank

You have been writing code for some little while at this point.

Does it tend to start like this?
\blank

    #include <stdio.h>

    int main(int argc, char **argv) {

        puts("Hello world!")

    }

\blank
(Implicit declaration of function 'puts' is invalid in C99.)


# hello python

Or start like this?

    print("Hello world!")

More verbosely:

    def main():
        print("Hello world!")

    if __name__ == '__main__':
        main()

Run with: `python hello.py`

You have to run the code _anyway_,
you _will_ be going through an edit-debug cycle.

(Why the "goop"? For clean imports.)


# buy low, sell high

Given a history of daily closing prices for an NYSE ticker symbol,
find the maximum possible profit.

E.g. `[12, 10, 15]` suggests a profit of 5.
\blank

    def find_profit(prices):
        ...
        return profit

    if __name__ == '__main__':
        print(find_profit([12, 10, 15]))


# hello test

    import unittest

    class ProfitTest(unittest.TestCase):

        def test_profit(self):
            self.assertEqual(5, find_profit([12, 10, 15]))

\blank
Run with: `python -m unittest profit_test.py`

Notice that an automated test is _self evaluating_ --
it knows the right answer.
If the target code regresses, it gets flagged right away.


# implementation -- brute force

We want:  $$\max\limits_{j \ge i} \; price_j - price_i$$

The code comes straight from the math notation.
\vfill

    def find_profit_quadratic(prices):
        profit = 0
        for i, buy in enumerate(prices):
            for j in range(i, len(prices)):
                assert j >= i
                sell = prices[j]
                profit = max(profit, sell - buy)
        return profit

\vfill
This has $O(n^2)$ time complexity :-(

# implementation -- linear

    def find_profit(prices):
        buy = min(prices)
        del prices[:prices.index(buy)]
        sell = max(prices)
        return sell - buy


# run it!

    import unittest

    class ProfitTest(unittest.TestCase):

        def test_profit(self):
            prices = [12, 10, 15]
            self.assertEqual(5, find_profit_quadratic(prices))
            self.assertEqual(5, find_profit(prices))

# run it some more

    import unittest

    class ProfitTest(unittest.TestCase):

        def test_profit(self):
            for expected, prices in [
                (5, [12, 10, 15]),
                (5, [12, 10, 11, 15, 14]),
                (5, [40, 12, 10, 15]),
                (0, [15, 14, 12, 12, 12]),
                (0, [12]),
            ]:
                for fn in [find_profit,
                           find_profit_quadratic]:

                    self.assertEqual(expected, fn(prices))


# DbC

Design by Contract is a way of thinking about functions,
so they are correct, and composable.

$f(g(x))$, or $f \circ g$, is $f$ composed with $g$.

This turns out to be quite important.
Consider e.g.

- def update_listing_status(id)
- def update_zipcode(zipcode)
- def update_state(state)

tl;dr: exceptions are your friend!


# contract

A contract is a promise, a condition, a specification.

Functions have pre-conditions,
e.g. pass in one or more numeric prices,
or pass in a valid 5-char zipcode.

    assert len(zipcode) == 5
    assert int(zipcode) > 0

They also have post-conditions, e.g.
return value shall be max feasible profit,
or after completion all listings within zipcode
shall have updated status.


# sqrt

Another example:

    def sqrt(n: float) -> float:
        if n < 0:
            raise ValueError(f'{n} is negative')
        ...
        # Newton-Raphson goes here
        ...
        assert root >= 0
        assert is_approx_equal(root * root, n)
        return root

(We _never_ `try:` / `catch` an `AssertionError`.)


# exceptions

Sometimes it is _impossible_ for a function to
complete its task, and to correctly satisfy the post-condition.

E.g. DB lock, or network connection went away.

What should we do then?
Return a sentinel profit of -1 ? No!

Prefer to `raise` a `ValueError` or similar exception.

This tells the caller that there is literally No Answer.


# composition

- def update_listing_status(id)
- def update_zipcode(zipcode)
- def update_state(state)

At the state level we loop across zipcodes.

At the zip level we loop across listing IDs.

A TCP timeout while updating a listing status
could be transient or permanent.
If an error corresponds to missing data for a region,
it's possible we could update _other_ regions successfully.

Naïve processing would simply let the exception
bubble up the call stack.
If it happens often enough to be troublesome,
the loop at state level might recover
by considering current zipcode un-updateable,
and simply move on to next zipcode.

# three kinds of assertion

- pre-condition (input), `assert 0 <= learning_rate <= 1`

    ----

- invariant, `assert j >= i`
- post-condition, `assert root >= 0`

\vfill
These three are all about correctness of the code.
\blank

Additionally, we might want to signal certain errors:

    if len(rows) == 0:
        raise LookupError('sorry, zero rows found')


# summary
\blank

Start your edit-debug cycle by writing a test.
\blank

Functions have pre- and post- conditions.
Raise an exception if you can't deliver on the promise.


<!---
Copyright 2021 John Hanley.

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
The software is provided "AS IS", without warranty of any kind, express or
implied, including but not limited to the warranties of merchantability,
fitness for a particular purpose and noninfringement. In no event shall
the authors or copyright holders be liable for any claim, damages or
other liability, whether in an action of contract, tort or otherwise,
arising from, out of or in connection with the software or the use or
other dealings in the software.
--->
