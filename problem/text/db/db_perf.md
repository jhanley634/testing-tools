
---
author: John Hanley
title: Database Performance
date: 9\textsuperscript{th} October 2020 [N slides]
copyright: 2020, see below
---

# Overview: superpowers

- locality of reference
- sequential over random reads
- know the future

# Optimizing queries

Optimizing is all about doing less work.

The compiler / backend asks the question,
"Can we use a cheaper access path and still get identical results?"

You should be asking,
"Do we really need _all_ that,
or could we get by with smaller / weaker results?"
For example, would an _estimate_ suffice?

# Loops

Push loops down,
out of your python code,
into the backend.
Ask **big** queries.

# Why is my query slow?



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
