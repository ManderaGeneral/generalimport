
import warnings


def _get_skip_base_classes():
    from unittest.case import SkipTest
    yield SkipTest

    try:
        from _pytest.outcomes import Skipped
        yield Skipped
    except ImportError:
        pass


class SkipTestException(*_get_skip_base_classes()):
    def __init__(self, msg=None):
        if msg is None:
            msg = ""
        self.msg = msg

    def __repr__(self):
        message = f"'{self.msg}'" if self.msg else ""
        return f"{type(self).__name__}({message})"

    def __str__(self):
        return self.msg


class MissingDependencyException(SkipTestException):
    pass


class MissingOptionalDependency(SkipTestException):
    """ MissingOptionalDependency is deprecated, use MissingDependencyException """
    pass

# def MissingOptionalDependency(*args, **kwargs):
#     warnings.warn("MissingOptionalDependency has been changed to MissingDependencyException", DeprecationWarning, stacklevel=2)
#     return MissingDependencyException(*args, **kwargs)


















