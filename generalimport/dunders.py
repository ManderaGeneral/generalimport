from generalimport.generalimport_bottom import _inside_typing
from generalimport.import_catcher import ErrorPars


class DynamicDunder:
    """ Inherit to define a dynamic dunder.
        All subclasses' triggers are tested for truthy before a MissingOptionalDependency is raised.
        Returns result() of first triggered dynamic dunder. """
    subclasses: list[type["DynamicDunder"]] = []

    def __init_subclass__(cls, **kwargs):
        cls.subclasses.append(cls)

    def __init__(self, error_pars: ErrorPars):
        self.error_pars = error_pars

    def trigger(self): return True
    def result(self): ...


NON_CALLABLE_DUNDERS = (
    # Callable
    "__annotations__", "__closure__", "__code__", "__defaults__", "__globals__", "__kwdefaults__",
    # Info
    "__bases__", "__class__", "__dict__", "__doc__", "__module__", "__name__", "__qualname__", "__all__", "__slots__",
    # Pydantic
    "_nparams",
)
CALLABLE_CLASS_DUNDERS = [
    # Lookup
    "__class_getitem__",
]
CALLABLE_DUNDERS = [
    # Binary
    "__ilshift__", "__invert__", "__irshift__", "__ixor__", "__lshift__", "__rlshift__", "__rrshift__", "__rshift__",
    # Callable
    "__call__",
    # Cast
    "__bool__", "__bytes__", "__complex__", "__float__", "__int__", "__iter__", "__hash__",
    # Compare
    "__eq__", "__ge__", "__gt__", "__instancecheck__", "__le__", "__lt__", "__ne__", "__subclasscheck__",
    # Context
    "__enter__", "__exit__",
    # Delete
    "__delattr__", "__delitem__", "__delslice__",
    # Info
    "__sizeof__", "__subclasses__",
    # Iterable
    "__len__", "__next__", "__reversed__", "__contains__", "__getitem__", "__setitem__",
    # Logic
    "__and__", "__iand__", "__ior__", "__or__", "__rand__", "__ror__", "__rxor__", "__xor__",
    # Lookup
    "__dir__",
    # Math
    "__abs__", "__add__", "__ceil__", "__divmod__", "__floor__", "__floordiv__", "__iadd__", "__ifloordiv__",
    "__imod__", "__imul__", "__ipow__", "__isub__", "__itruediv__", "__mod__", "__mul__", "__neg__", "__pos__",
    "__pow__", "__radd__", "__rdiv__", "__rdivmod__", "__rfloordiv__", "__rmod__", "__rmul__", "__round__",
    "__rpow__", "__rsub__", "__rtruediv__", "__sub__", "__truediv__", "__trunc__",
    # Matrix
    "__imatmul__", "__matmul__", "__rmatmul__",
    # Object
    "__init_subclass__", "__prepare__", "__set_name__",
    # Pickle
    "__getnewargs__", "__getnewargs_ex__", "__getstate__", "__reduce__", "__reduce_ex__",
    # String
    "__format__", "__fspath__", "__repr__", "__str__",
    # Thread
    "__aenter__", "__aexit__", "__aiter__", "__anext__", "__await__",
    # Typing
    "__origin__",
]


class DynamicEQ(DynamicDunder):
    def trigger(self):
        return _inside_typing() and self.error_pars.caller == "__eq__" and bool(self.error_pars.args)

    def result(self):
        other = self.error_pars.args[0]
        return id(self) == id(other)


class DynamicHash(DynamicDunder):
    def trigger(self):
        return _inside_typing() and self.error_pars.caller == "__hash__"

    def result(self):
        return id(self)
