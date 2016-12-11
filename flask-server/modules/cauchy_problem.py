from dll_importer import BaseImport
from ctypes import c_double, c_bool

class CauchyProblem(BaseImport):
    SO_NAME = '../cpp-sources/numerical_methods.so'
    RETURN_TYPES = {}

class CauchySolution(BaseImport):
    SO_NAME = '../cpp-sources/numerical_methods.so'
    RETURN_TYPES = {}

class CircleCauchyFunction(BaseImport):
    SO_NAME = '../cpp-sources/numerical_methods.so'
    RETURN_TYPES = {}

class SpiralCauchyFunction(BaseImport):
    SO_NAME = '../cpp-sources/numerical_methods.so'
    RETURN_TYPES = {}



