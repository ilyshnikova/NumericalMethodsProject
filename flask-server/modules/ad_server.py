from dll_importer import BaseImport
from ctypes import c_double, c_bool

class AdServer(BaseImport):
    SO_NAME = '../cpp-sources/numerical_methods.so'
    RETURN_TYPES = {'C1' : c_double, 'C2' : c_double, 'Phi' : c_double, 'GetBeta': c_double}

class AdServerAutoSetup(BaseImport):
    SO_NAME = '../cpp-sources/numerical_methods.so'
    RETURN_TYPES = {}



