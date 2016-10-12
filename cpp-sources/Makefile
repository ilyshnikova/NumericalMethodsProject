all:
	g++ -g -c -fPIC tabular_function.cpp -o tabular_function.o
	g++ -g -c -fPIC functions.cpp -o functions.o
	g++ -g -c -fPIC interpolated_function.cpp -o interpolated_function.o
	g++ -g -c -fPIC cauchy_problem.cpp -o cauchy_problem.o
	g++ -g -shared -Wl,-soname,numerical_methods.so -o numerical_methods.so cauchy_problem.o interpolated_function.o tabular_function.o functions.o
	rm -rf tabular_function.o interpolated_function.o functions.o cauchy_problem.o

clean:
	rm -rf *.so


