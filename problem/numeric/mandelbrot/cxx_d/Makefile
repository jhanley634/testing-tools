
all: mset_cxx

mset_cxx: mset_cxx.o ppm.o
	$(CXX) -Wall $< -o $@

%.o: %.C
	$(CXX) -Wall -g -c $<
