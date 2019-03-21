
memory_use
=========

Utility to verify details of when a given python interpreter or
python extension will call malloc & free.

Three kinds of containers are supported: list, dict, dataframe.

A memory hog deliberately fills a container with many unique 100 KiB strings,
running until malloc fail.
Then binary search identifies the largest feasible allocation,
and we back off 10% from that, as the target size.

Then we repeatedly demonstrate that we can allocate and deallocate a
container of the target size.
Deallocation can be an explicit `del`,
or due to a variable going out of scope of a helper function.
