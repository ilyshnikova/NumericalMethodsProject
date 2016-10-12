from ctypes import cdll, c_double
U = PolynomialFunction()
S = PolynomialFunction()
z = PolynomialFunction()
F = F1()

lib = cdll.LoadLibrary('../cpp-sources/numerical_methods.so')
obj = lib.CauchySolution_New(c_double(0), c_double(0), c_double(0), c_double(0),)
lib.CauchySolution_Delete(obj)


