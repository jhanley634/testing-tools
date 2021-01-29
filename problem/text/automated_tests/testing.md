
# automated testing

Copyright 2021, John Hanley

There are many ways to test.
I won't say this is the Right Way.
This is where _I_ am at in the testing journey right now.
Next year I'm sure my tests will be better.

## motivation

Code has bugs.
More code, more bugs.
Bugs have costs.
There are some known techniques for reducing bugs.

Always remember:

> We spend time writing tests
> to save time.

If a technique isn't saving time for you, or your team,
then don't do it.

There is certainly a difference between unit- and integration-tests,
but I choose not to quibble about it.
I lump many test types together under the heading "automated tests".
I feel the most important thing is that they are cheap to run.
They should be so easy that you run them All The Time, and so will jenkins.
Ideally they should interactively complete within ten seconds.
Long-running tests have value, as well,
but segregate them into their own test suite.
Jenkins is happy to patiently run that suite for you in the background.

### must execute anyway

I accept this as axiomatic:

A line of code I wrote
that hasn't run yet
is likely buggy.

Especially if it is a line in an error handler.

With java / C the compiler can maybe help point out
type safety issues, potential null deref and the like.
With python, at best you'll be told about parse fail.
You _have_ to run the code.

### get the test for free

Now, you could use `if __name__ == '__main__': main()`,
and exercise recently authored code in that way.
But it's the same amount of effort to paste in a bit of boilerplate.
Here, I'll get you started:

    import unittest

    class TestFoo(unittest.TestCase):

        def test_foo(self):
            assert True

Several lines.
I know, slightly tedious.
But honestly, it wasn't that bad.
Same number of lines the `def main():` approach needs, in fact.

Now execute with:

    $ python -m unittest

or perhaps define a makefile target so you can say: `$ make test`

It is sometimes convenient to tack on a `--verbose` flag:

    $ python -m unittest -v

Now test as you always would.
Assemble the objects, create the dicts, call your function.
You can even do "print() debugging", you can even insert `breakpoint()`.

Some folks prefer `pytest`.
I find the stacktrace formatting it does by default is verbose and unhelpful,
but to each his own.
Choose your favorite, they'll both work the same way.

One advantage pytest offers is "marks".
They help us with choosing to run one type of test or another,
for example "slow" tests, or DB tests.
That can be pretty handy.

### logging

Consider using `logger.info('hi')` instead of `print('hi')`.
It's not a big thing, I won't be pedantic about it.
But when your code winds up in production,
you're going to need to use a logger anyway,
may as well cut to the chase and start using it now.

### finish the test

Eventually you will have convinced yourself the new function works,
for some definition of "works".
At a minimum it doesn't crash.

Now, how to share that hard work?
How to leverage what you've already done
so teammates can benefit from it,
and so we can notice future regressions?

Well, look!
You've already done the hard part!
You have the setup, it's calling your function with suitable args.
Now we just need to **evaluate** the result.

You have perhaps been printing the output
of your `foo()` function to stdout.
Which is nice enough.
But it makes _you_ the weak link,
as we need you to eyeball the output
and evaluate if it is Good or Bad.
It's time to make the test self-evaluating.
It must _know_ if a result is Green or Red.

## checking what matters

You wrote a docstring for the target function `foo()`, right?
No? Go back and write one now.
(Unless we're dealing with `get_foo()` or a similarly obvious contract.)
A single sentence might suffice.
In Design-by-Contract terms,
it should spell out  the necessary pre-condition(s),
and describe the value-add, the promised post-condition.

Use that to write a test which verifies it delivered on the promise.

### example

    def sqrt(n: float) -> float:
        """Given a non-negative number, returns its approximate square root."""

That's not _very_ precise,
it doesn't tell us how much relative error fits within "approximate",
but it's still helpful.
And we can infer a test from the math definition of a root.
Let's use a helper:

    def is_small_relative_error(a: float, b: float, epsilon: 1e-9) -> bool:
        if a == 0:
            return abs(b) < epsilon
        assert a > 0
        rel_err = abs(b - a) / a
        return rel_err < epsilon

Now the test is easy:

    def test_square_root(self):
        for n in get_nonnegative_examples():
            root = sqrt(n)
            assert is_small_relative_error(root * root, n)

A simple set of examples would be:

    def get_nonnegative_examples(k=100):
        yield from range(k)

though I would feel better about the test
if we threw in some non-integer values, as well.

### simpler example

    def test_square_root(self):
        self.assertEqual(0, sqrt(0))
        self.assertEqual(1, sqrt(1))
        self.assertEqual(3, sqrt(9))
        self.assertEqual(1e3, sqrt(1e6))
        self.assertAlmostEqual(.5, sqrt(.25), 3)
        self.assertAlmostEqual(1.772, sqrt(math.pi), 3)

This is a perfectly sensible approach to testing.
It enjoys the virtue of being very simple, very easily understood.

We pay much less attention to DRY in tests, versus in target code,
but it can still be helpful.
Consider re-phrasing as:

    def test_square_root(self):
        for val, expected in [
                (0, 0),
                (1, 1),
                (9, 3),
                (1e6, 1e3),
                (.25, .5),
                (math.pi, 1.772),
        ]:
            self.assertAlmostEqual(expected, sqrt(val), 3)

This is especially winning if there's two or three lines
of setup before calling the target function,
or if there's a few tests to perform on the several returned attributes.

### weak test

The post-condition might make a strong assertion, or many of them.
Don't feel too bad about doing weaker sanity checks.
Does that mean you did not fully test the target function? Yes.
But hey, that's better than nothing!

With square root you might restrict your attention to a range,
like `n > 4`, and then verify the root is "small": `root < n / 2`

Simply checking a length might suffice for your purposes:

    self.assertEqual(2, len(count_states_starting_with('North ')))

Here we could `.assertEqual(['NC', 'ND'], count_...())`
but with an argument of `'N'`, checking we get `8` results
starts to look more convenient.

Sometimes we anticipate growth, so an inequality is more suitable:

    self.assertGreater(get_population('Austin TX'), 790_000)

For both target functions,
we are confident that if its data source is truncated or unavailable,
we will certainly notice the error.

## brittleness

We spend time writing tests to save us time.

A brittle test is one that doesn't age gracefully,
doesn't accommodate change and bit-rot.

For example:

    self.assertEqual(get_population('Austin TX'), 790_390)

This might have been a fine test in 2010.
It might even be fine now, if the getter is specified
to consume a dataset that is forever frozen in time, a 2010 snapshot.
But as folks move in, the test will need a succession of updates.
Hence the `.assertGreater()` used above,
which is weaker than verifing correct pop (how would it even do that?)
but stronger than accepting answers like
there is "one" or "one thousand" residents.

Avoid writing brittle tests.
Pay attention to the function's spec,
and test the relevant aspect of the spec,
test what we care about.

If you see spurious failures from a brittle test, consider fixing it.
But also consider removing it, since it is wasting rather than saving time.

## refactoring

### courage

One of the enormous wins from having a good test suite
is it gives us the _courage_ to refactor the target code.

Lacking proper test coverage,
we might go in there to make some changes.
The code _should_ behave the same before and after a change.
But who can tell?

Answer: see a Green run of tests, make your change, run tests again.
If it's Green, maybe things are OK, and you can make further changes.
If it's Red, you _definitely_ know you broke something,
go figure it out before you wreak further havoc.

## measurement

