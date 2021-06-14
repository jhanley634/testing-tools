
---
author: John Hanley
title: Things we'd rather not read
date: Monday, June 14th, 2021
---


# Things we'd rather not read

<!--- Copyright 2021, John Hanley
MIT licensed -- see end.
--->

An experienced programmer has read _lots_ of code.

There are some things we'd rather not read again and again.

Here are a few of them.
I will start small.

## goal

The Author's goal is always to present a compelling argument,
much as a sonnet, an essay, or a math proof would try to do.

An essay starts with a topic paragraph,
which starts with a topic sentence.
The Author "wins" if subsequent arguments
adequately buttress the topic sentence's claims;
the Reader will decide.

A program is trying to convince the Reader that

1. it accomplishes the Requirements, and that
2. it is correct.

You send me a PR.
Without attempting to execute it,
I will decide if I'm convinced of those two things.


# lint

Here's a trivial difficulty:

    def double(n):
        return 2* n

Yes, the Turing machine computes the Right Thing.

No, it does not conform to the Requirements,
not for a project with stated goals of adhering to
[PEP-8](https://www.python.org/dev/peps/pep-0008/#whitespace-in-expressions-and-statements).
On the one hand we have whitespace slightly off.
On the other, the Author is making it clear
that she did not care enough about the Reader
to run a `flake8` linter before submitting PR.
When that's true, then a large PR will typically
have many similar issues, and they become distracting.
Which leads to a lower quality review,
fewer substantive issues uncovered.

It's not hard to write standards-conforming code.
Let the linter teach you.
Soon you'll be writing that way without even thinking about it.

(And as far as `import` ordering goes,
don't give it a 2nd thought.
Just run `isort` and be done with it.)


# sometimes initialized

    def deal_with(items):
        for item in items:
            if complex_predicate():
                x = get_new_x()
            process(item, x)

Maybe this is Correct.
Maybe `x` _always_ exists by the time we process an item.
But you're making me nervous.
I'm concerned we're going to raise

    NameError: name 'x' is not defined

Please, just assign `x = None` up top,
and then there's one less thing to worry about.


# catalog of attributes

    class Foo:

        def __init__(self):
            self.a = 1
            self.b = 1

        def increment(self, n):
            self.c = n + self.a



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
