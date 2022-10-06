
def _get_skip_base_classes():
    from unittest.case import SkipTest
    yield SkipTest

    try:
        from _pytest.outcomes import Skipped
        yield Skipped
    except ImportError:
        pass


class MissingOptionalDependency(*_get_skip_base_classes()):
    def __init__(self, msg=None):
        self.msg = msg

    def __repr__(self):
        if self.msg:
            return f"MissingOptionalDependency: {self.msg}"
        else:
            return f"MissingOptionalDependency"

    def __str__(self):
        return self.msg or "MissingOptionalDependency"
