from ctypes import cdll
from commands import getstatusoutput

class DLLLoader(object):
    LOADED = {}

    @classmethod
    def get_lib(cls, name):
        if name not in cls.LOADED:
            print "Loading {name}".format(name = name)
            cls.LOADED[name] = cdll.LoadLibrary(name)

        return cls.LOADED[name]

def method_wrapper(self_object, self_func):
    def method(*args):
        return self_func(self_object, *args)

    return method

class BaseImport(object):
    def __init__(self, *args):
        cls = type(self)
        type_name = cls.__name__
        self.lib = DLLLoader.get_lib(cls.SO_NAME)

        self.obj = getattr(self.lib, "{type_name}_New".format(type_name = type_name))(*args)


        for class_with_method in getstatusoutput("nm -D " + cls.SO_NAME + "  | awk '{print $3}'  | grep -E '^" + type_name + "'")[1].split('\n'):
            if class_with_method[len(type_name)] == '_':
                method = class_with_method[len(type_name) + 1:]
                if method in cls.RETURN_TYPES:
                    return_type = cls.RETURN_TYPES[method]
                    getattr(self.lib,"{type_name}_{method}".format(type_name = type_name, method = method)).restype = return_type

                if method == "Delete":
                    self_method = "__del__"
                else:
                    self_method = method

                setattr(
                    self,
                    self_method,
                    method_wrapper(
                        self.obj,
                        getattr(self.lib,"{type_name}_{method}".format(type_name = type_name, method = method))
                    )
                )
    def __del__(self):
        getattr(self.lib, "{type_name}_Delete".format(type_name = type(self).__name__))(self.obj)

