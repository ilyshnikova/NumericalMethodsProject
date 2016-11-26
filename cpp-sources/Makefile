all:
	g++ -g -c -fPIC tabular_function.cpp -o tabular_function.o
	g++ -g -c -fPIC tabulate_integration.cpp -o tabulate_integration.o
	g++ -g -c -fPIC functions.cpp -o functions.o
	g++ -g -c -fPIC interpolated_function.cpp -o interpolated_function.o
	g++ -g -c -fPIC cauchy_problem.cpp -o cauchy_problem.o
	g++ -g -c -fPIC interpolation.cpp -o interpolation.o
	g++ -g -shared -Wl,-soname,numerical_methods.so -o numerical_methods.so cauchy_problem.o interpolated_function.o tabular_function.o tabulate_integration.o functions.o interpolation.o
	rm -rf tabular_function.o interpolated_function.o functions.o cauchy_problem.o tabulate_integration.o

clean:
	rm -rf *.so


