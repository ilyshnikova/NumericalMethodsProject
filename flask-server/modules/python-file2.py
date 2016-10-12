from dll_importer import BaseImport
from ctypes import c_double

class Foo(BaseImport):
    SO_NAME = './libfoo.so'
    RETURN_TYPES = {'double' : c_double}

for i in xrange(1):
    f = Foo(5)
    f.bar()
    f.func()
    print f.double()
