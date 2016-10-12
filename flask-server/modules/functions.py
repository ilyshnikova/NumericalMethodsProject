from dll_importer import BaseImport
from ctypes import c_double, c_bool

class F1(BaseImport):
    SO_NAME = '../cpp-sources/numerical_methods.so'
    RETURN_TYPES = {'GetValue' : c_double}
