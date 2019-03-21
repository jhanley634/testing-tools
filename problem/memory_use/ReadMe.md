
del
===

For list / dict / df we store a bunch of 100 KiB strings,
go until failure due to malloc fail,
then back off from that slightly to safely produce a “large” object.

Given that size target, we loop to create such an object a dozen times,
tidying up by letting go out of scope and/or `del` it.

