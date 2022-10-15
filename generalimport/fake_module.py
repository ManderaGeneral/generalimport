from generalimport import MissingOptionalDependency


class FakeModule:
    """ Behaves like a module but any attrs asked for always returns self.
        Raises a ModuleNotFoundError when used in any way.
        Unhandled use-cases: https://github.com/ManderaGeneral/generalimport/issues?q=is%3Aissue+is%3Aopen+label%3Aunhandled """
    __path__ = []

    def __init__(self, spec):
        self.name = spec.name

        self.__name__ = spec.name
        self.__loader__ = spec.loader
        self.__spec__ = spec

    def error_func(self, *args, **kwargs):
        name = f"'{self.name}'" if hasattr(self, "name") else ""  # For __class_getitem__
        raise MissingOptionalDependency(f"Optional dependency {name} was used but it isn't installed.")

    def __getattr__(self, item):
        if item in self.non_called_dunders:
            self.error_func()
        return self

    # Binary
    __ilshift__ = __invert__ = __irshift__ = __ixor__ = __lshift__ = __rlshift__ = __rrshift__ = __rshift__ = error_func

    # Callable
    __call__ = error_func

    # Cast
    __bool__ = __bytes__ = __complex__ = __float__ = __int__ = __iter__ = __hash__ = error_func

    # Compare
    __eq__ = __ge__ = __gt__ = __instancecheck__ = __le__ = __lt__ = __ne__ = __subclasscheck__ = error_func

    # Context
    __enter__ = __exit__ = error_func

    # Delete
    __delattr__ = __delitem__ = __delslice__ = error_func

    # Info
    __sizeof__ = __subclasses__ = error_func

    # Iterable
    __len__ = __next__ = __reversed__ = __contains__ = __getitem__ = __setitem__ = error_func

    # Logic
    __and__ = __iand__ = __ior__ = __or__ = __rand__ = __ror__ = __rxor__ = __xor__ = error_func

    # Lookup
    __class_getitem__ = __dir__ = error_func

    # Math
    __abs__ = __add__ = __ceil__ = __divmod__ = __floor__ = __floordiv__ = __iadd__ = __ifloordiv__ = __imod__ = __imul__ = __ipow__ = __isub__ = __itruediv__ = __mod__ = __mul__ = __neg__ = __pos__ = __pow__ = __radd__ = __rdiv__ = __rdivmod__ = __rfloordiv__ = __rmod__ = __rmul__ = __round__ = __rpow__ = __rsub__ = __rtruediv__ = __sub__ = __truediv__ = __trunc__ = error_func

    # Matrix
    __imatmul__ = __matmul__ = __rmatmul__ = error_func

    # Object
    __init_subclass__ = __prepare__ = __set_name__ = error_func

    # Pickle
    __getnewargs__ = __getnewargs_ex__ = __getstate__ = __reduce__ = __reduce_ex__ = error_func

    # String
    __format__ = __fspath__ = __repr__ = __str__ = error_func

    # Thread
    __aenter__ = __aexit__ = __aiter__ = __anext__ = __await__ = error_func


    non_called_dunders = (
        # Callable
        "__annotations__", "__closure__", "__code__", "__defaults__", "__globals__", "__kwdefaults__",

        # Info
        "__bases__", "__class__", "__dict__", "__doc__", "__module__", "__name__", "__qualname__", "__all__", "__slots__",
    )