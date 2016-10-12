from dll_importer import BaseImport
from ctypes import c_double, c_bool

class CauchyProblem(BaseImport):
    SO_NAME = '../cpp-sources/numerical_methods.so'
    RETURN_TYPES = {}

class CauchySolution(BaseImport):
    SO_NAME = '../cpp-sources/cauchy_problem.so'
    RETURN_TYPES = {'GetX': c_double, 'GetY': c_double, 'IsDefine': c_bool}



