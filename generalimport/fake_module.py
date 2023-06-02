from typing import Optional
import sys
import logging
from functools import partialmethod

from generalimport.exception import MissingDependencyException
from generalimport.dunders import DynamicDunder, NON_CALLABLE_DUNDERS, CALLABLE_CLASS_DUNDERS, CALLABLE_DUNDERS
from generalimport.import_catcher import ErrorPars

EXCEPTION_NAMING_PATTERNS = ["Exception", "Error"]

logger = logging.getLogger("generalimport")


class FakeModule:
    """ Behaves like a module but any attrs asked for always returns self.
        Raises a ModuleNotFoundError when used in any way.
        Unhandled use-cases: https://github.com/ManderaGeneral/generalimport/issues?q=is%3Aissue+is%3Aopen+label%3Aunhandled """
    __path__ = []
    # __args__ = []  # Doesn't seem necessary
    SENTINEL = object()

    def __init__(self, spec, trigger: Optional[str] = None, catcher=None):
        self.name = spec.name
        self.trigger = trigger
        self.catcher = catcher

        self.__name__ = spec.name
        self.__loader__ = spec.loader
        self.__spec__ = spec
        self.__fake_module__ = True  # Should not be needed, but let's keep it for safety?


    @classmethod
    def _dynamic_dunder_check(cls, error_pars: ErrorPars):
        for dynamic_dunder_cls in DynamicDunder.subclasses:
            dynamic_dunder = dynamic_dunder_cls(error_pars=error_pars)
            if dynamic_dunder.trigger():
                return dynamic_dunder.result()

        return cls.SENTINEL

    @classmethod
    def _get_error_message(cls, error_pars: ErrorPars):
        required_by = f" (required by '{error_pars.trigger}')" if error_pars.trigger else ""
        name_part = f"{error_pars.name}{required_by} " if error_pars.name else ""

        msg_list = [
            f"Optional dependency {name_part}was used but it isn't installed.",
            f"Triggered by '{error_pars.caller}'.",
        ]
        if error_pars.catcher is not None and error_pars.catcher.message:
            msg_list.append(error_pars.catcher.message)

        return " ".join(msg_list)

    @classmethod
    def _error_func(cls, error_pars):
        result = cls._dynamic_dunder_check(error_pars=error_pars)
        if result is not cls.SENTINEL:
            return result

        msg = cls._get_error_message(error_pars=error_pars)

        logger.debug(msg=msg)
        raise MissingDependencyException(msg=msg)

    def error_func(self, _caller: str, *args, **kwargs):
        error_pars = ErrorPars(name=self.name, trigger=self.trigger, caller=_caller, catcher=self.catcher, args=args, kwargs=kwargs)
        return self._error_func(error_pars=error_pars)

    @classmethod
    def error_func_class(cls, _caller: str, *args, **kwargs):
        error_pars = ErrorPars(name=None, trigger=None, caller=_caller, catcher=None, args=args, kwargs=kwargs)
        return cls._error_func(error_pars=error_pars)

    @staticmethod
    def _item_is_exception(item):
        return any(str(item).endswith(pattern) for pattern in EXCEPTION_NAMING_PATTERNS)

    @staticmethod
    def _item_is_dunder(item):
        return item in NON_CALLABLE_DUNDERS

    def __getattr__(self, item):
        fakemodule = FakeModule(spec=self.__spec__, trigger=item, catcher=self.catcher)
        if self._item_is_exception(item=item) or self._item_is_dunder(item=item):
            return fakemodule.error_func(item)
        return fakemodule


# Sets all the callable dunders of FakeModule to 'error_func()' by preserving the name of the dunder that triggered it.
# Mainly useful for debug purposes.
for dunder in CALLABLE_DUNDERS:
    setattr(FakeModule, dunder, partialmethod(FakeModule.error_func, dunder))

for dunder in CALLABLE_CLASS_DUNDERS:
    setattr(FakeModule, dunder, partialmethod(FakeModule.error_func_class, FakeModule, dunder))




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
