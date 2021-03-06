
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

There are some big advantages of automated tests
over ad hoc interactive debugging:

1. a test is forever, it keeps running, keeps verifying
2. a test is cheap to run, the setup is part of it, so is the good / bad check
3. a test is cheap for your teammate to run, and vice versa -- we benefit from _everyone's_ tests
4. a test is a good teaching opportunity, on par with the documentation

### must execute anyway

I accept this as axiomatic:

> A line of code I wrote
> that hasn't run yet
> is likely buggy.

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
Same number of lines as used by the `def main():` approach, in fact.

Now execute with:

    $ python -m unittest

or perhaps define a makefile target so you can say: `$ make test`

It is sometimes convenient to tack on a `--verbose` flag:

    $ python -m unittest -v

Now test as you always would.
Assemble the objects, create the dicts, call your function.
You can even do "print() debugging".
You can even insert `breakpoint()`.

Some folks prefer `pytest`.
I find the stacktrace formatting it does by default is verbose and unhelpful,
but to each his own.
Choose your favorite, they'll both work the same way.
I tend to start with unittest and move to pytest if needed,
since a TestCase will run under anything,
unlike a suite intended for pytest.

One advantage pytest offers is "marks".
They help us with choosing to run one type of test or another,
for example "slow" tests, or DB tests.
That can be pretty handy.

### logging

Consider using `logger.info('hi')` instead of `print('hi')`.
It's not a big thing, I won't be pedantic about it.
But when your code winds up in production,
you're going to need to use a logger anyway.
May as well cut to the chase and start using it now.

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
It must know if a result is Green or Red,
and let the test framework know about that.
Typically assertions do that.

## checking what matters

You wrote a docstring for the target function `foo()`, right?
No? Go back and write one now.
(Unless we're dealing with `get_foo()` or a similarly obvious contract.)
A single sentence might suffice.
In Design-by-Contract terms,
it should spell out the necessary pre-condition(s),
and also describe the value-add, the promised post-condition.

Use that to write a test which verifies it delivered on the promise.

Sometimes pre-conditions are implicit from parameter names or types.
Consider taking advantage of python's optional type annotations.

### example

    def sqrt(n: float) -> float:
        """Given a non-negative number, returns its approximate square root."""

That's not _very_ precise,
it doesn't tell us how much relative error fits within "approximate",
but it's still helpful.
And we can infer a test from the math definition of a root.
Let's use a helper:

    def is_small_relative_error(a: float, b: float, epsilon=1e-9) -> bool:
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

We pay much less attention to
[DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)
in tests, versus in target code,
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

The star-args syntax often proves useful here,
for sending several arguments into the target function:

    for args, expected in [
            ((3, 4, 5), True),
            ((5, 12, 13), True),
            ((1, 1, 2), False),
    ]:
        assert expected == is_pythagorean_triple(*args)

### weak test

The post-condition might make a strong assertion, or many of them.
Don't feel too bad about doing weaker sanity checks.
Does that mean you did not fully test the target function? Yes.
But hey, that's better than nothing!

With square root you might restrict your attention to a range,
like `n > 4`, and then verify the root is "small",
with `root < n / 2`.

Simply checking a length might suffice for your purposes:

    self.assertEqual(2, len(states_starting_with('North ')))

Here we could `.assertEqual(['NC', 'ND'], states_...())`
but with an argument of `'N'`, simply checking we get `8` results
starts to look more convenient.
It is a cheap way of saying, "yep, I eyeballed the results and
they looked good, now I am baking it in so I will notice any changes."

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
But as new residents move in, the test will need a succession of updates.
Hence the `.assertGreater()` used above,
which is weaker than verifying correct pop (how would it even do that?)
but stronger than accepting answers like
there is "one" or "one thousand" residents.
Keep business logic out of tests,
don't re-write functionality that's in the target function.

Avoid writing brittle tests.
Pay attention to the function's spec,
and test the relevant aspect of the spec,
test what we care about.

If you see spurious failures from a brittle test, consider fixing it.
But also consider removing it, since it is wasting rather than saving time.

## verify exception

Tell your test suite to check that an exception is thrown in this way:

    with self.assertRaises(ValueError):
        math.sqrt(-9)

If you like you can
tack this on: `.assertRaises(ValueError, msg='math domain error')`.

## unit vs. integration

Consider this setup, greatly simplified from a more complex program:

    def foo():
        w = world()
        return f'hello {w}'

    def world():
        return 'world'

    def test_foo():
        assert foo() == 'hello world'

Do we have a unit test here?
No, it is an integration test,
which lacks a tightly focused `test_world()`.
Do I care? No. This small test suite is Just Fine.
It was easy to write, it tests what matters,
and it exercises all the code.
If `world` never causes you trouble, then leave things as they are.
If it _does_ start exhibiting Heisenbugs that you want to
focus on, track down, and prevent from recurring,
then you will be motivated to create a small unit test just for it.

In a similar vein, suppose we marked `_world()` a private helper.
A test suite might choose to focus on testing public functions,
ignoring anything _private.
If trouble later develops,
again that would motivate writing small unit tests
that focus on the trouble.

Suppose we inject a code defect:

    def world():
        x = 1 / 0
        return 'world'

Will `test_foo` notice the fatal ZeroDivisionError?
Yes! So the test suite is Good Enough,
it suits our needs.
All the target code runs, and we verify what matters.

## doctests

Docstrings are nice.
But sometimes we don't believe them,
as they have fallen out of sync with the code,
not being maintained to track the changes.

How could we notice such bit rot?
And make a compelling case to the Reader
that "this docstring speaks truth!" ?
[Doctests](https://docs.python.org/3/library/doctest.html)
to the rescue!
Here is an example:

    def sqrt(n):
        """Given a non-negative input, returns its square root.

        >>> sqrt(16)
        4.0
        """

And here is how to run it:

    $ python -m doctest -v

(The `--verbose` flag is optional.)

Go ahead, try claiming `5.0` shall be returned, and see what happens.

If you _do_ start writing doctests in your code,
be sure to update your `make` target so they run routinely.

## refactoring

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

If you're faced with refactoring test-less code,
consider breaking the refactor into these steps:

1. Write just enough tests to cover the affected target code.
2. Refactor that target code.

## design

Do we hack, hack, hack, and declare whatever behavior
happened to fall out of the implemenation to be
the Public API? No! We intentionally design the API.
Sure, it may evolve as we iterate.
But the design is always guided by the caller's needs,
not by details of the callee implementation.

A design should be "easy to consume",
including the requirement that it be "easy to consume _correctly_."
What do I mean by that?
Let's consider a counter-example.

### libc

The venerable [write(2)](https://linux.die.net/man/2/write)
system call has been in unix / linux for more than half a century,
and it won't be going away soon.
Alas, callers seldom use its API correctly,
due in part to C language details.
Callers often invoke for side effects and ignore the returned `n`,
neglecting to check that it matches what they expect it will be.
Worse, they almost always neglect to check `errno`.
So `write()` does the Right Thing,
but app is buggy because caller failed to
correctly consume the Public API.

In C++ or other languages that support exceptions,
we could design a much better API by throwing an exception in cases where

1. we wrote a different number of bytes than was requested, or
2. an error occurred that was stored in `errno`.

### python gotchas

Avoid writing a function that returns two disparate types,
e.g. sometimes a `str` and sometimes a `float`.
Yes, python is dynamic.
But the caller will appreciate your type-safety guarantees.
If your function could return one or more `int`'s,
be sure the single answer case looks like

    return [n]

rather than a scalar

    return n

What if it could sometimes return zero `int`'s?
For example, in the case of "no matches found".
Look to the caller for guidance!

Will caller typically iterate over the result?
Then iterating through an empty container with zero results
is probably most convenient.

Does caller have to check for the "not found" case anyway?
Then returning `None` rather than `[]` is probably the best way
to ensure that caller will correctly consume your API.
It essentially is handing back a landmine that might explode
if not treated carefully, e.g. by trying to de-reference
the zero-th element of the `None` result.

But there is Another Way.
If the check is so essential that every caller
will _have_ to perform the check anyway,
might as well put the check in the called library.
The library can helpfully `raise NotFoundError()` -- that is _part_
of the Public API it exports, much as the return type is.

### custom exceptions

When should library raise an app-specific exception
instead of the standard RuntimeError?
It depends on caller needs.

Let's take a step back for a moment.
Why does caller drive the API design?
Because there's one instance of the called library code, but N callers.
So effort devoted to making each call site
smaller, more convenient, less bug-prone
will be effort well spent.
An **excellent** reason for writing tests
around the same time as writing an implementation
is the test will be the 2nd caller.
If it is inconvenient to write the test,
you will notice that, and perhaps polish the API a bit.

Back to the caller.
You have N of them.
Perhaps there is the occasional `try` mixed in there.
Do any of the call sites pay attention to _type_ of error raised?
Or do they all just treat error as "fatal error"?

If at least one caller needs to distinguish
among error types, then definitely go ahead
and define a new one that inherits from `Exception`.
If no one cares, then stick with `RuntimeError`.
What's that, you think someone will care next week?
[YAGNI](https://en.wikipedia.org/wiki/You_aren%27t_gonna_need_it).
Wait till next week when an _actual_ need arises,
and _then_ tack on the new error class.

Also, if there are multiple app-specific errors they should be
organized as inheriting from a single error class you define.
This again is for the convenience of callers,
so they can catch a fine-grained list or
just catch your umbrella error category.

### consolidating input args

When you look at callers of the several functions you recently wrote,
do you notice any commonalities?

If you see same argument being passed on many calls,
e.g. a DB connection, consider grouping your functions
under a class that stores the common arg as an instance attribute.

If you see groups of 2 or 4 args being passed to a few functions,
consider turning them into a
[single object](https://docs.python.org/3/library/collections.html#collections.namedtuple)
like this:

    from collections import namedtuple

    Name = namedtuple('Name', 'first last')
    Addr = namedtuple('Addr', 'address_line city state zipcode')

## happy path

Often I will write tests that just exercise the happy path,
be satisfied, and stop there.

If you notice errors that aren't picked up by your tests,
that may motivate testing more corner cases
or exercising more error handlers.

To go a bit farther down that path,
I heartily recommend this
[module](https://pypi.org/project/hypothesis/):

    import hypothesis

It will automatically generate more example inputs
than you would have created by hand.
You may find it will manage to break your code,
presenting you with an example input that triggers a bug.
Or it might declare your code "correct".

There is a nice "minimization" applied to broken examples,
where it will search for smaller numbers or shorter strings
that still exhibit same bug.
This leads to conveniently compact unit test inputs.
Incorporate the example into your test suite,
to ensure the code never regresses to the point
of exhibiting that bug again.

## mocking

Much has been written on the topics of
Dependency Injection and mocks.
I have poor habits in this department,
so I have little to teach here.

Mocking lets you decouple deps so you have a true unit test.
For example, your function might make DB queries.
A mock DB lets you avoid a large, potentially buggy RDBMS codebase,
avoid the danger of having rows change beneath you,
and avoid the expense of wiping and initializing DB tables.
Or your function might hit RESTful endpoints,
and again you want tests to succeed / fail independent of
whatever changes might happen to that external endpoint.

Mocks also permit Gantt chart decoupling.
We can develop client code for next year's server
by hitting a mock of that server.

I'm focused on only devoting effort where it saves effort,
and I have not yet found the mocking argument super convincing.
I feel it's a technique I need to explore further.

One approach I have found,
that gives something like a mock DB "for free",
is testing of target code that accesses mysql or postgres
via the sqlalchemy portability layer.
If code does not need vendor-specific syntax features,
then swapping in a sqlite backend can be a good way to
decouple test results from a potentially changing persistent datastore.

## measurement

You have some target code,
and tests that exercise it.
Pat yourself on the back!
Are you through?
Well, maybe. Best to check, right?

A coverage measurement will tell you what fraction of your code
is exercised by the test suite,
and will highlight lines not run.

Sometimes there are methods or even whole classes that
are never invoked by an automated test, and that might be Fine,
depending on your testing goals.
But it's good to know for sure what is covered.
In particular, there might be details in a report
that surprise you, showing that an `if` / `else` clause never ran,
or that two recently added functions never ran.
If you're surprised and you _do_ want that code to execute, well,
change the inputs,
Extract Helper or otherwise revise the design,
or write new tests, whatever it takes.
Then re-run, and verify the coverage changed as intended.

If you find that it is "impossible" (or merely "difficult")
to exercise a line of code, consider deleting it.
Maybe you don't need it.
Or maybe you should change the design
so that code is now exposed where a unit test _can_ call it.

For example, `if date > '2030-01-01':` might benefit from
turning the hardcoded date into a passed parameter.
Similarly, `if is_pingable('my_server'):` could benefit
from letting a test specify `'dead_server'` as an input hostname,
but better it could accept an `is_healthy` predicate
so a unit test can swap out `is_pingable` with
an `always_false` function, to deliberately trigger that condition.
Checks for "no free disk space" and "out of memory" also fall
into that same category of "hard to provoke" during a unit test.

### testability

While writing tests, if you find yourself
bumping into  such "hard to trigger" issues,
well, you've kind of lost the battle already.

> Testability is a requirement.

When authoring the original target code,
you should have been paying closer attention.
It's never too late,
there's still time to refactor,
to break things apart so the innards are exposed for testing.

One reason we avoid nested `def` is the inner function
is completely inaccessible for testing.
Another reason is that coupling of shared namespace
is a bit like using global variables,
making it harder to reason about the code.

We avoid having one module call another's _private() functions.
But you should never feel bad about having a test
access _private symbols -- that is perfectly OK, and encouraged!

### making a measurement

To run it, rather than `python -m unittest` we will use:

    $ coverage run -m unittest test_*.py

Actually, it's a bit more involved than that.
You see, the `coverage`
[module](https://coverage.readthedocs.io/en/coverage-5.4/)
essentially puts a counter on every source line of code,
during interpreter bytecode generation.
And those counters are persisted to disk,
so they can be accumulated across several runs.
Non-zero counters correspond to exercised code.
Runs usually are automated but can also include interactive sessions.
And finally we will want to do some reporting.

This will clear (erase) the sqlite `.coverage` counter file,
accumulate counts, then produce both HTML and text summary reports:

    $ coverage erase
    $ coverage run -m unittest test_*.py
    $ coverage html
    $ coverage report

Use `conda` (or `pip`) to install the `coverage` package,
add the above commands to a convenient `make` target,
and you're good to go.

Use `$ open htmlcov/index.html`
to view the generated report in your browser.
Green lines of source ran,
red lines were not covered by the test suite.

## recap

We write tests to save time.
Only do the work if your team finds it valuable.

We intentionally design our Public APIs,
they don't fall out of some accidental implementation detail.
Consider the caller's needs.

Reviewing test results helps us catch mistakes.
If you notice you've made a mistake, ask yourself,
"how could my test suite help me avoid repeating it in future?"

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
