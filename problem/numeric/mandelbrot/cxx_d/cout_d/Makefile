
all: cout_bench

OBJS = cout_bench.o

%.o: %.C
	$(CXX) $(CFLAGS) -Wall -O0 -g -c $<

cout_bench: $(OBJS)
	$(CXX) $(OBJS) -o $@
