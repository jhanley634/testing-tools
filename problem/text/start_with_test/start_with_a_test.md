
<!--- Copyright 2021, John Hanley
MIT licensed -- see end.
--->

---
author: John Hanley
title: Start with a test!
date: Tuesday, May 11th, 2021
---

# Start with a test!

## hello

You have been writing code for some little while at this point.

Does it tend to start like this?

    #include <stdio.h>

    int main(int argc, char **argv) {

        puts("Hello world!")

    }

(Implicit declaration of function 'puts' is invalid in C99.)


# hello

Or like this?

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

    def find_profit(prices):
        ...
        return max_profit

    if __name__ == '__main__':
        print(find_profit([12, 10, 15]))


# hello test

    import unittest

    class ProfitTest(unittest.Testcase):

        def test_profit(self):
            self.assertEqual(5, find_profit([12, 10, 15]))

Run with: `python -m unittest profit_test.py`

Notice that an automated test is _self evaluating_ --
it knows the right answer.
If the target code regresses, we will know right away.

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
