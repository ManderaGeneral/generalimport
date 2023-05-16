from typing import Optional
import sys
import logging
from functools import partialmethod
from generalimport.exception import MissingOptionalDependency, MissingDependencyException


EXCEPTION_NAMING_PATTERNS = ["Exception", "Error"]

logger = logging.getLogger("generalimport")


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



class FakeModule:
    """ Behaves like a module but any attrs asked for always returns self.
        Raises a ModuleNotFoundError when used in any way.
        Unhandled use-cases: https://github.com/ManderaGeneral/generalimport/issues?q=is%3Aissue+is%3Aopen+label%3Aunhandled """
    __path__ = []

    def __init__(self, spec, trigger: Optional[str] = None):
        self.name = spec.name
        self.trigger = trigger

        self.__name__ = spec.name
        self.__loader__ = spec.loader
        self.__spec__ = spec
        self.__fake_module__ = True  # Should not be needed, but let's keep it for safety?

    @staticmethod
    def _error_func(name, trigger, caller):
        required_by = f" (required by '{trigger}')" if trigger else ""
        name_part = f"{name}{required_by} " if name else ""
        msg = f"Optional dependency {name_part}was used but it isn't installed."
        msg = f"{msg} Triggered by '{caller}'."
        logger.debug(msg=msg)
        raise MissingDependencyException(msg=msg)

    def error_func(self, _caller: str, *args, **kwargs):
        self._error_func(name=self.name, trigger=self.trigger, caller=_caller)

    @classmethod
    def error_func_class(cls, _caller: str, *args, **kwargs):
        cls._error_func(name=None, trigger=None, caller=_caller)

    @staticmethod
    def _item_is_exception(item):
        return any(str(item).endswith(pattern) for pattern in EXCEPTION_NAMING_PATTERNS)

    @staticmethod
    def _item_is_dunder(item):
        return item in NON_CALLABLE_DUNDERS

    def __getattr__(self, item):
        fakemodule = FakeModule(spec=self.__spec__, trigger=item)
        if self._item_is_exception(item=item) or self._item_is_dunder(item=item):
            fakemodule.error_func(item)
        return FakeModule(spec=self.__spec__, trigger=item)

    @classmethod
    def assign_dunder_methods(cls, dunders, error_func):
        """ Sets all the callable dunders of FakeModule to 'error_func()' by preserving the name of the dunder that triggered it.
            Mainly useful for debug purposes. """
        for dunder in dunders:
            setattr(cls, dunder, partialmethod(error_func, dunder))


FakeModule.assign_dunder_methods(dunders=CALLABLE_DUNDERS, error_func=FakeModule.error_func)
FakeModule.assign_dunder_methods(dunders=CALLABLE_DUNDERS_CLASS, error_func=FakeModule.error_func_class)


def is_imported(module_name: str) -> bool:
    """
    Returns True if the module was actually imported, False, if generalimport mocked it.
    """
    module = sys.modules.get(module_name)
    try:
        return bool(module and not isinstance(module, FakeModule))
    except MissingDependencyException as exc:
        # isinstance() raises MissingDependencyException: fake module
        pass
    return False
