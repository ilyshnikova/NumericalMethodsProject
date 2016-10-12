from dll_importer import BaseImport
from ctypes import c_double, c_bool

class TabularFunction(BaseImport):
    SO_NAME = '../cpp-sources/numerical_methods.so'
    RETURN_TYPES = {}

class TabularFunctionIterator(BaseImport):
    SO_NAME = '../cpp-sources/numerical_methods.so'
    RETURN_TYPES = {'GetX': c_double, 'GetY': c_double, 'IsDefine': c_bool}

class Tabulator(object):

    def __init__(self):
        pass

    def tabulting(self, expression, from_arg, to_arg, step):
        tabular_function = TabularFunction()
        x = from_arg
        while x <= to_arg:
            y = eval(expression)
            tabular_function.AddValue(c_double(x), c_double(y))
            x += step

        return tabular_function

    def get_points(self, tabular_function):
        points = []
        it = TabularFunctionIterator(tabular_function.obj)
        while it.IsDefine():
            points += [[it.GetX(), it.GetY()]]
            it.Next()

        return points
