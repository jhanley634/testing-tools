
# database memory use

Copyright 2021 John Hanley.

Suppose you are informed that a database is running low on memory.
How would you diagnose it?
First figure out which case you are in:

1. You are the SysAd, or
2. Amazon Aurora is.

## local admin

You have `sudo` root access,
and installed the DB with `apt install postgres`.
Use `ps axuww | grep postgres` to see half a dozen background daemons.
Pick a PID, like 123, and use `ps wwup 123` to see
the same thing with column headings.
This is the identical procedure you would use
for noticing whether any _other_ daemon was leaking memory.
Output at the top of `top` can also be useful.

Note that all daemons are sitting on roughly the same amount of memory,
and that it has been fairly stable since boot time.
Postgres is mature code -- most leaks have been removed.
Uptime of many months is routine,
so even slow leaks would be noticed.

Use `$ cat /proc/swaps` to see if any backing store has been configured,
and how much is currently used.
Kubernetes famously avoids configuring swap space,
so on a k8s pod this will be empty.
Use `$ head /proc/meminfo` to see how much RAM you have,
and how much is in use.

It is worth noting that tmpfs can malloc.
Running `$ mount` will reveal such filesystems.
Use `$ df -h /tmp` to see total size.
Use `du` and `ls` for finer grained assessment.
An `rm` of large file corresponds to `free()`'ing
some malloc'd space.

## remote admin

If the database is an Amazon Aurora instance,
then you lack shell access to the DB server.
We will have to probe it from afar.
A good starting place is the "Monitor"
tab on amazon's RDS web console.

A DB client can be in a few states:

1. idle -- outside a transaction, holding almost no resources
2. query -- in a short transaction, will finish within ten seconds
3. report -- a long-running job

Use a query like this to see what clients are up to:

    SELECT    datname, pid, usename, application_name AS app,
              EXTRACT(EPOCH FROM NOW() - query_start)::INTEGER AS age_sec,
              state, SUBSTRING(query, 1, 60) AS query
    FROM      pg_stat_activity
    ORDER BY  state, age_sec, LENGTH(query);

A report _can_ tie up an interesting amount of memory
to support hash-join or the like.
But e.g. hour long reports should be seen to use less RAM
as free memory slowly dwindles, switching plans
to prefer less memory or even disk-based mergesort.
A multi-day report won't be responsive in that way,
but such reports raise their own class of issues
and should probably be segregated onto a separate server.

What's more likely is that a simple metric of

    SELECT  COUNT(*)  FROM pg_stat_activity;

will explain most of the client-induced memory consumption.
Even an idle session uses a little memory,
for the worker process on the server.

For a tighter focus on the source of those connections, use

    SELECT    COUNT(*), client_addr
    FROM      pg_stat_activity
    GROUP BY  client_addr
    ORDER BY  1 DESC, 2;

## remediation

Consider killing wasteful / non-essential clients,
to recover server resources.
If you're on the client host,
a simple `kill` (or `kill -9`) will suffice.
If the client is a k8s pod,
consider using `$ kubectl delete pod foo-xxxxxxxx-yyyyy`
to bounce it (k8s will re-spawn),
or `$ kubectl scale deployment foo --replicas=2`
to reduce the number of replicas
to some small number like 2.

If there's a particular backend process `123` you find troublesome,
you might use `SELECT pg_cancel_backend(123);` to ask it to die.
As it executes its query plan, it will periodically poll
for a "cancel" message, and exit gracefully.
If you notice that does not succeed within a second or two,
you can resort to the slightly more violent
`SELECT pg_terminate_backend(123);`.
That shall deliver a signal to the process, and it won't be ignored.

### extreme measures

A DB client will commonly re-connect upon having a session terminated.
If you need to ensure that will no longer happen,
consider changing the DB credentials to some new password.

Once the incident is better understood and mitigated,
you will likely want to change the password back.
Alternately you may wish to whisper the new password
into the ear of several k8s deployments,
verifying that they get back in and do not harm the DB.
Any miscreant pods would still be locked out
if they don't receive the updated creds.


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
