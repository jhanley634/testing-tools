
all: mset_cxx

OBJS = mset_cxx.o ppm.o
mset_cxx: $(OBJS)
	ls -l $(OBJS)
	$(CXX) -Wall $(OBJS) -o $@

%.o: %.C
	$(CXX) -Wall -g -c $<
