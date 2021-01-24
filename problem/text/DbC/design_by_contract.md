
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

### exceptions

An important tool!
More on this later.

### composition

Another important tool.
Let us study this outside of Turing Machines for a moment,
and then return to it.
