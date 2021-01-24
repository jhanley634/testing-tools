
# design by contract

Copyright 2021 by John Hanley

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

### exceptions

An important tool!
More on this later.

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
