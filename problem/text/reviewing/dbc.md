
---
author: John Hanley
title: Design by Contract
date: 9\textsuperscript{th} July 2020
copyright: 2020, see below
---

# Design by Contract
A Turing Machine can compute anything.

\pause
Including "wrong" things.

\pause
Among our tools for controlling complexity are

- break code into small functions
- composition of functions
- attach data + methods to OO class objects
- DbC --- design by contract

# Promises

My neighbor promises to cut my lawn.

I promise to give him twenty bucks.

That's a contract.

# Promises

Caller will give the `sqrt` function a non-negative number.

It will give me a result whose square matches the input.

That's a contract.

# Promises

What about broken promises?

\pause
    n = sqrt(-9)

Omg, omg, what to do?

\blank
\pause
Return *nothing*, no computed result, nada. Blow up!

`raise ValueError()`

# Contracts in the design

- Caller satisfies a **pre-condition**. If not, all bets are off.
- Callee satisfies a **post-condition**. Or explodes.

# Contracts in the design

## composition

\blank

    a = f()
    b = g(a)
    c = h(b)
 
\blank
or
\blank

    c = h(g(f()))

# "handling" an exception

Is an exception fatal?

Should I catch / ignore / log / swallow it?

\pause
No!

\pause
\blank
Should I let it propagate up the call chain?

Yes. Of course. **That** is what composition in DbC is all about.

# "handling" an exception

Should I deal with it or let it percolate up the stack?

The **one** question you need to ask is:

> Can I satisfy the post-condition?

\blank
If you cannot keep your promise, then `raise` and make
it someone else's problem.

\blank
If you *can* recover and re-compute,
so you deliver on the promise, then do so.
That is what "handling" means.

# questions

Questions?

\blank
Experiences?


<!---
Copyright 2020 John Hanley.

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
