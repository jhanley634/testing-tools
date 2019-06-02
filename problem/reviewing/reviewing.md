
---
author: John Hanley
title: On reviewing code
copyright: 2019, see below
---

#code review
Greetings!
I look forward to collaborating with you
in pursuit of high-quality code.
\blank

I tend to read code closely,
and write down whatever comes into my head as I'm reading.
I will write how I feel about a bit of code.
\blank

In particular, I do not limit myself
to just observations about code defects.

#ground rules
The original author always wins.
\blank

As a reviewer I approach the text with Beginner Eyes,
and can see things the author will gloss over.
\blank

My goal is to let the author see the code from
a new perspective, from my perspective.
\blank

If, having considered that, the author chooses to
reject a proposed change, that is *just fine!*

#ground rules
Just because I say a thing about the code,
doesn't mean that it is *true*.
\blank

Feel free argue a point, or ignore it.
Like everyone, I make mistakes, too.
Sometimes I am just Wrong.
\blank

#ground rules
OTOH, if I remark that I find code or docs

- confusing
- obscure
- misleading

then you have at *least one* data point
that you *might* want to clarify what you wrote.

It could be the case that a quick casual reading
leaves one confused,
and some tricky concept requires more careful reading.
But maybe adding a sentence about that tricky aspect
is warranted.
\blank

I might read the unchanged text the next day and find it clear.

But I'm a different person then, I'm no longer approaching it
with Beginner Eyes.

#signature
(We will be mostly dealing with **python** (3.7) from here on out.)
\blank

Feel free to annotate input types and return types, or not.
\blank

Do *not* return more than one kind of result,
e.g. sometimes an `int` and sometimes a `list` of `str`.
Doing so makes your public API hard to (correctly) consume.
\blank

Returning e.g. `int` or `None` is fine,
but *do* consider designing your API so an exception is raised
rather than `None` returned.
Depending on details, the exception may be more convenient for the caller.
\blank

*Do* consider returning empty (`[]` or `{}` or `""`)
rather than `None`.

#executable comments
Comments are good.

Executable comments are better.

Consider using `assert`, `verify()`, or conditional `raise`
to signal that input args were incorrect.

Simply assuming things about inputs is fine, also,
e.g. going ahead and de-referencing `x[y]`.
*Do* think about whether a failed operation
will produce a *diagnostic* error or an opaque one.
Consider adding checks you feel may help future debugging.
\blank

Keep **DbC**, Design by Contract, in mind.

It matters when writing code.

It matters more when designing the public API.

Should I muddle on? Return `None`? Raise an error?

#comments
Comments are Good. But...
\blank

Comments lie.
\blank

**Details** go in the code,

**generalities** go in the comments.

Better to write a vague comment which does not lie,

than to write something specific which isn't true.
\blank

Bit rot happens.

Comments are likely to rot, over time.

#docstring
A special kind of comment is a python *docstring*.

The audience is: engineers wanting to call your code.

Use `#` comments instead when you're writing *code* explanations,
rather than API *calling* explanations.
\blank

Each docstring should start with an English sentence.

A sentence begins with a Capital,
has a noun and a verb,
and ends with a `.` period.
\blank

Between the signature and the docstring,
an engineer should have a pretty good idea of how to
(correctly) use your public API.

Feel free to assume the engineer will *also* view your source code.
You don't have to answer every single question that might arise;
this isn't Sun's javadocs.
If you choose to wax poetic,
typically you should leave a blank line after the initial summary sentence
before beginning paragraph(s) describing your method.

#docstring --- numpydoc
You do *not* have to exhaustively detail every parameter of your method in a docstring.
A single sentence often will sufice.

However, if you feel details would be helpful,
please use numpydoc format. (https://numpydoc.readthedocs.io/en/latest/)

#docstring --- numpydoc
Here is a numpydoc example:

    def draw_random_sample(mu, sigma):
        """Draws random sample from a normal random variable.
        
        Parameters
        ----------
        mu : float
            Mean of the distribution.
        sigma : float
            Standard deviation of the distribution

        Returns
        -------
        float
            A normally distributed value from N(mu, sigma).
        """

#docstring --- numpydoc
If you *do* choose to go with a detailed Parameters section,
it is probably best to obey DRY (Don't Repeat Yourself),
and omit annotations from the signature.
After renames and whatnot,
we wouldn't want to see documentation out of sync.

#docstring --- doctest
The `doctest` module lets you execute specially formatted documentation.

It is related to the `unittest` module.
\blank

Here is an example:

    def sqrt(n):
        """Returns square root of a non-negative number.
        
        >>> sqrt(9)
        3.0
        """
               
If you use this format,
you *should* regularly execute such tests,
perhaps through a `Makefile` target.

For example: `$ python -m doctest *.py`


<!---
Copyright 2019 John Hanley.

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