
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
"Can we use a cheaper access path
and still get identical results?"
It wants to avoid
busy work,
 computing X only to discard it.

You should be asking,
"Do we really need _all_ that,
or could we get by with smaller / weaker results?"
For example, would an _estimate_ suffice?

# Primary key

Every relation should have a PK.

Enough said.

![](http://tempest.fluidartist.com/wp-content/uploads/2014/10/Receipts.jpeg)

# Mappings

A relation is a function mapping from PK to attribute(s).

\blank
Example:

    SELECT price  FROM listing  WHERE guid = '123def';

\blank
This is $f(guid) \rightarrow price$.

# Covering index (1 / 2)

An index "covers" a query if it supplies all values needed,
so we don't have to seek into the row blocks on disk.

\blank
Examples:

    CREATE INDEX ON prop(fips_county, apn);

    SELECT    fips_county, COUNT(*)
    FROM      prop
    GROUP BY  fips_county;

    SELECT    fips_county, COUNT(*), MAX(apn)
    FROM      prop
    GROUP BY  fips_county;

# Covering index (2 / 2)


An index "covers" a query if it supplies all values needed,
so we don't have to seek into the row blocks on disk.

\blank
**Not** a covering index (for this query):

    CREATE INDEX ON prop(fips_county, apn);

    SELECT    fips_county, MAX(price)
    FROM      prop
    GROUP BY  fips_county;

Fix it with:

    CREATE INDEX ON prop(fips_county, apn, price);

# Loops

Push loops down,
out of your python code,
into the backend.
Ask **big** queries.

Why?

The backend query planner is called a "planner" for a reason.
Tell it about **all** the rows you'll be asking for,
and it can avoid dumb busy work, it can make a better plan.

Sending a thousand queries for a thousand zipcodes
blinds the planner to the fact you're going to send 999 similar queries.
If it knows all blocks shall be retrieved,
then it will choose sequential tablescan instead of index.

# Selectivity (1 / 2)

The selectivity of a query is the fraction
of base rows that appear in the result set.

\blank
Example:

    SELECT COUNT(*)  FROM mls.property  WHERE zipcode = '91320';
    3614

    SELECT COUNT(*)  FROM mls.property;
    19001000

That is .02 % of the base relation's rows, so an index would win.

# Querying in O(log n) time (1 / 3)

binary tree

![](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Complete_binary2.svg/900px-Complete_binary2.svg.png)

# Querying in logarithmic time (2 / 3)

B tree

![](https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/B-tree.svg/600px-B-tree.svg.png)

# Querying in logarithmic time (3 / 3)

B+ tree

![](https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Bplustree.png/600px-Bplustree.png)

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
