
# design by contract

Copyright 2021 by John Hanley

---
monofont: DejaVuSansMono.ttf
---

## correctness

There are two kinds of programs:

- correct, or
- incorrect

We strive to write programs that are correct.

Decades ago Brooks wrote of the
[mythical man-month](https://en.wikipedia.org/wiki/The_Mythical_Man-Month),
and described a "20-year bug",
one that only triggered after twenty years of running in production,
a bug hardly worth diagnosing or fixing.
Even if a function stacktraces only rarely,
such a function is still "incorrect" and awaiting a fix.

We have several tools in our toolbox to aid in writing correct code.

### testing

Automated unit tests, and e2e integration tests, are essential.
But they are not enough.

> Testing shows the presence, not the absence of bugs.
>
> ---edsger w. dijkstra

### simplicity

Abstractions are a huge help for writing correct code.
Every application strives to write in a higher level language,
closer to the business domain, so in the end we say `doit()`
and the Right Thing happens. OOP "hiding" techniques can play a
role in this.

Shooting for Tony's first case is the way to go:

> There are two ways of constructing a software design:
> One way is to make it so simple that there are obviously no deficiencies,
> and the other way is to make it so complicated that there are no obvious deficiencies.
> The first method is far more difficult.
>
> ---C. A. R. Hoare

### single responsibility

A method, or class, should do One Thing well.
Write it down, in a sentence.
If it takes two sentences, that's a hint you need two methods,
that you should Extract Helper.

Sometimes we refer to this as Separation of Concerns.

### local analysis

We must be able to reason about the correctness of a function
by reading it in a screenful of code.
Without scrolling.
Without referring to functions it calls, nor to its callers.

So the signature should make interface details clear.

We should be able to examine the handful of public methods
in a module to learn its purpose,
glossing over lots of _private helpers.

Similarly we should be able to understand the handful of attributes
assigned by an `__init__()` constructor and maintained by a class,
and keep them in mind when reading each public method of the class.

If any of these stray from Single Responsibility, or grow too long,
then it is time to Extract Helper,
to whittle the implementation down to something that _can_
be held in the mind all at once upon the first reading.

### induction

If you can demonstrate a working base case, such as in a unit test,
and you have an induction step that always works,
well, then you can correctly solve an infinite class of problems.

### composition

Let `o` denote composition.
Consider functions `f(x)` and `g(x)`.

Then `f o g`, or `f` composed with `g`, is `f(g(x))`.

Layered software needs to exploit composition routinely.
Making it work correctly is at the heart of DbC.

## contracts

Every software component has a specification, a "contract" it
must conform to.

### mowing example

Alice's lawn needs mowing.
She offers Bob $20 to cut the grass.
This is a contract.

There are some pre-conditions that must be satisfied, or the contract is void:

- Bob needs access to the lawn,
- and to a mower.

There are some post-conditions:

- At day's end the grass shall be cut, and
- Alice shall hand the cash to Bob.

### sqrt() example

Let's examine the contract of this root-finding function.

Pre-condition:

- Offer a non-negative real input.

Post-condition:

- Squaring the output shall (approximately) give the input number.

So the square root function is making a **promise** about its output.
And we can test it, we can verify it.

### impossible to compute

What if a pre-condition is violated, as with input of `-1` ?
Should `sqrt` return a sentinel like `0` ? No.
It is literally impossible to compute a sensible result,
to return something that satisfies the post-condition.

In that case, we compute "nothing"!
We un-ask the original question,
we raise fatal error rather than returning a result.

    def sqrt(n: float) -> float:
        if n < 0:
            raise ValueError('need a non-negative real input')
        ...
        assert is_small_relative_error(root * root, n)
        return root

This is the magic of Design By Contract!
If we can't satisfy the contract, we compute "nothing",
it's like it never happened.
There's no reason to try making "false promises",
such as returning a sentinel value.

### contracts compose

    def twice_radical(x: float) -> float:
        return 2 * sqrt(x)

Notice how we get the relevant guarantees "for free" here.
If `x` is a bad input, the Right Thing will happen.
No need for other layers to know about the negative constraint.
Checking happens where it ought to, and
an error will bubble up  the call stack.

    def rad_x_on_x(x: float) -> float:
        """Given a positive input, computes √X̅ / X."""
        return sqrt(x) / x

There is one more value to avoid here: zero.
But again the check comes for free, since `operator.__truediv__()`
will helpfully raise ZeroDivisionError when necessary.

### environment is a global variable

Consider a report that queries a remote database,
writes a few temp files, and returns summary statistics.
There are some implicit pre-conditions for the caller:

- We shall have network connectivity.
- DB server shall be available.
- /tmp shall have adequate free space available.

The caller needn't check them beforehand.
It's not even desirable, as it's not his concern.
Disk and net conditions could change at any time
during a lengthy report run, and they will be checked
at the appropriate instant by the appropriate layer.
You get your report, or you don't.

## exception handling

Some people view exceptions, or stack traces, as a Bad thing.
Not so!
They are wonderfully freeing.
They give you latitude to give up when a problem turns out to be impossible,
and then the rest of the time you return correct results.
Either satisfy the spec, the contract,
or else declare it null and void.

Knowing when to catch an exception,
and when to let it bubble on up the stack
can be a bit subtle.
(In python we use `try` ... `except` to catch.)

### catch at the bottom

A low-level utility function like `sqrt` is usually
at or near the bottom of the call stack, it is a leaf node.
Such functions typically may raise errors but they do not catch.
They have few dependencies, few additional calls.
Either the pre-conditions were satisfied upon entry, or they weren't.

### catch near the bottom

Functions that implement the lower layers of an application
may similarly raise, on their own or due to a dep.
But should they catch?

Almost always the answer is "no!" Here is a pair of (rare) "yes" situations:

#### extra logging

The author might find it surprising that a dep raised,
and he wants to know about it. So he logs it.

    try:
        x = shake(input)
        y = bake(x)
    except Exception:
        logger.exception('chicken unavailable')
        raise
    z = ...

Note that we `raise` same exception at the end.
This is essential!
A thing we depend on failed, so we must fail,
and report that up the call stack.

We do not ask for `e` using `except Exception -> e:`,
and we do not use `logger.error(f'trouble with {e}'`,
since the `.exception()` method has it implicitly
and will do a fine job of reporting the details.

#### retry

Perhaps you have two implementations to try.
If `bake()` fails, perhaps you could call `fry()`.
Or maybe you have two XML parsers, each with their own rough edges, so
error from one might not imply you'll get same error from the other.
In such a case you legitimately can "handle" the error,
by catching an trying it the other way,
in an effort to make good on the contract, on the promise.
If retry fails, be sure to let that error go up the stack.

A special case of this approach is to retry
calling the _same_ function more than once,
in the hopes that a future call will offer a different result.
There are pitfalls here.
