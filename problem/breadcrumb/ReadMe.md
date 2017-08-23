
breadcrumbs
===========

Given initial GPS breadcrumbs,
plus training data (and current time),
predict driver's final destination.

exploration
-----------

Use this to view common edge IDs:

    jq . /tmp/2002/0001.json | grep edgeId | sort | uniq -c | sort -n | tail
