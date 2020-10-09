
---
author: John Hanley
title: Database Performance
date: 9\textsuperscript{th} October 2020 [20 slides]
copyright: 2020, see below
---

# Overview

- indexes
- selectivity
- lookup speed
- slow queries
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

# Random I/O

Random reads are _slower_ than sequential reads.

\blank
example timing:

- 16 µs per sequential read ( ~ 60 K read/sec), vs
- 90 µs per random read ( ~ 10 K read/sec)

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

    SELECT COUNT(*) FROM mls.property WHERE zipcode = '91320';
    3614

    SELECT COUNT(*) FROM mls.property;
    19001000

That is .02 % of the base relation's rows, so an index would win.

# Latency numbers every programmer should know
    L1 cache reference ....................... 0.5 ns
    Branch mispredict .......................... 5 ns
    L2 cache reference ......................... 7 ns
    Mutex lock/unlock ......................... 25 ns
    Main memory reference .................... 100 ns
    Compress 1K bytes with Zippy ........... 3,000 ns  =   3 µs
    Send 2K bytes over 1 Gbps network ..... 20,000 ns  =  20 µs
    SSD random read ...................... 150,000 ns  = 150 µs
    Read 1 MB sequentially from memory ... 250,000 ns  = 250 µs
    Round trip within same datacenter .... 500,000 ns  = 0.5 ms
    Read 1 MB sequentially from SSD* ... 1,000,000 ns  =   1 ms
    Disk seek ......................... 10,000,000 ns  =  10 ms
    Read 1 MB sequentially from disk .. 20,000,000 ns  =  20 ms
    Send packet CA->Netherlands->CA .. 150,000,000 ns  = 150 ms

\blank
\footnotesize ref.: https://gist.github.com/hellerbarde/2843375 \newline
orig. ref.: https://norvig.com/21-days.html#answers

# Querying in O(log n) time (1 / 3)

binary tree

![](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Complete_binary2.svg/900px-Complete_binary2.svg.png)

# Querying in logarithmic time (2 / 3)

B tree

![](https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/B-tree.svg/600px-B-tree.svg.png)

# Querying in logarithmic time (3 / 3)

B+ tree

![](https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Bplustree.png/600px-Bplustree.png)

# Why is my query slow? (1 / 4)

Maybe it has to be slow.
If you're asking for a million result rows,
that's going to take some time.

You might be requesting a dozen result rows,
but require _filtering_ a million base rows.
Can you index, so we're not filtering?

\blank
Measure the $\dfrac{\textrm{rows}}{\textrm{sec}}$
app level throughput.

Use COUNT(*) to estimate the filtering throughput.

# Why is my query slow? (2 / 4)
## Cartesian cross product

Let $a$ and $b$ be number of rows in those tables.
Then

        SELECT *  FROM A  JOIN B;

produces $a \times b$ result rows. An ON clause,

        SELECT *  FROM A  JOIN B ON a.id = b.a_id;

can cut that down substantially.

\blank
For an equi-join, say it in the ON, rather than WHERE.

\blank
Pay attention to PKs of both tables,
so you don't accidentally omit a column from a compound key.

# Why is my query slow? (3 / 4)
## Driving table

Do you have a plan in mind?
When you read your query,
can you envision what the backend will do?
In what order?

If you can't, maybe your query is too hard to read.
Consider breaking it into separately testable chunks,
using WITH cte, or CREATE VIEW, or temp table.

What are the table sizes?
Are they wide?
What's the selectivity, how much filtering is happening?
What's likely to be cached?

In a JOIN, prefer to access big tables first.

Read the EXPLAIN plan -- does it match what you expect?  Try:

    EXPLAIN ANALYZE SELECT ...

# Why is my query slow? (4 / 4)
## Disabled index

Understand that the backend cannot "see through" a function, e.g.

        WHERE x > y

lets us exploit an index on either column. This is no different:

        WHERE sqrt(x) > sqrt(y)

except the backend doesn't understand the monotonicity,
and won't be able to exploit an index on either column.

\blank
Avoid CAST and similar functions in ON clauses, also:

    FROM a  JOIN b  ON a.unsigned_zipcode::TEXT = b.zip5

# know the future

Sometimes we _know_ there will be a chrono query tomorrow,
for rows we've already committed.
Or perhaps many such queries.

Why wait? Do the work now, and store it on disk.
We call this an index.
Or perhaps a derived table, a reporting table.
Consider using CREATE MATERIALIZED INDEX.

\blank
Store counts, if that's all the query result will need.

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
