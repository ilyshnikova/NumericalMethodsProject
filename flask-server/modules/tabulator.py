from dll_importer import BaseImport
from ctypes import c_double, c_bool
import math

class TabularFunction(BaseImport):
    SO_NAME = '../cpp-sources/numerical_methods.so'
    RETURN_TYPES = {}

class TabularFunctionIterator(BaseImport):
    SO_NAME = '../cpp-sources/numerical_methods.so'
    RETURN_TYPES = {'GetX': c_double, 'GetY': c_double, 'IsDefine': c_bool}

class TabularCauchyFunction(BaseImport):
    SO_NAME = '../cpp-sources/numerical_methods.so'
    RETURN_TYPES = {}

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

class CauchyFunctionTabulator(object):
    def __init__(self, t_min, t_max, t_step, x_min, x_max, y_min, y_max):
        self.args = (t_min, t_max, t_step, x_min, x_max, y_min, y_max)

    def tabulate(self, expression_x, expression_y):
        (t_min, t_max, t_step, x_min, x_max, y_min, y_max) = self.args
        tabular_cauchy_function = TabularCauchyFunction()
        t = t_min
        while t < t_max:
            x = x_min
            while x < x_max:
                y = y_min
                while y < y_max:
                    tabular_cauchy_function.AddValueX(c_double(x), c_double(y), c_double(t), c_double(eval(expression_x)))
                    tabular_cauchy_function.AddValueY(c_double(x), c_double(y), c_double(t), c_double(eval(expression_y)))
                    y += t_step
                    y = math.floor(y * 100) / 100
                x += t_step
                x = math.floor(x * 100) / 100
            t += t_step
            t = math.floor(t * 100) / 100
        return tabular_cauchy_function

