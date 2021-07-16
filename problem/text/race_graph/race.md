
---
author: John Hanley
title: Race Logic
date: Friday, July 16th, 2021
---


# Race Logic

<!--- Copyright 2021, John Hanley
MIT licensed -- see end.
--->

overview of https://dl.acm.org/doi/pdf/10.1145/3460223
In-Sensor Classification
With Boosted Race Trees

by Tzimpragos et al.

# Moore's law

Things are no longer getting faster,
just denser.

![Moore's law](http://xlabs.ai/wp-content/uploads/2014/11/moore2.png)


# Thermal management -- heat

More bit flips means more $I^2 R$ heating

![toaster](toaster.jpg){height=2.3cm}

![short circuit](short-circuit.jpg){height=2.3cm}


# Thermal management -- register

![one-bit register, D flip-flop](
https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/D-Type_Transparent_Latch.svg/2560px-D-Type_Transparent_Latch.svg.png){
height=2cm}

![NAND gate](https://upload.wikimedia.org/wikipedia/commons/9/9b/PMOS-NAND-gate.svg){height=3.7cm}


# Thermal management -- gate

![NAND gate](https://content.instructables.com/ORIG/FVP/M39M/I8FR2WRE/FVPM39MI8FR2WRE.jpg)


# Delay encoding

There's more than one way to store small integers.

"The key idea behind race logic is to encode values as a _delay_ from some reference."


# Computing with delay encoding

"basic temporal operators MAX, MIN, and ADD-CONSTANT ...
efficiently solve a class of dynamic programming algorithms"

![logic building blocks](max-min.png)


# Reverse race trees

A decision tree, e.g. an XGBoost model,
can be implemented as a tree of signals racing from leaves to root.

At each node the first arriving signal wins, with others suppressed.


# Reverse race trees

![decision tree](decision-tree.png){height=8cm}


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
