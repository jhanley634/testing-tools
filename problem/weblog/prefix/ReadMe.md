
# compress to prefixes

## problem
Given K slots in a firewall ACL and
N IP address (IPv4 /32's),
emit a set of at most K CIDR prefixes
that admits all N client addresses
plus some minimal number of extra addresses.
The loss function is the number
of extra addresses that the ACL admits.
That will be zero when N <= K,
so the problem is only interesting
if N /32's won't fit within the K slots. 

## example
given K=1 and three IPs:

- 10.0.0.4
- 10.0.0.6
- 10.0.0.7

the appropriate output would be 10.0.0.4/30,
and the loss function would be "1 extra IP".
