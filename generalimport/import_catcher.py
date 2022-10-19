from logging import getLogger

from generalimport import _get_previous_frame_filename, _get_top_name, _get_scope_from_filename


class ImportCatcher:
    WILDCARD = "*"

    def __init__(self, *names):
        self.names = set(names)
        self.added_names = set()
        self.added_fullnames = set()
        self.enabled = True
        self._scope = self._get_scope()

        getLogger(__name__).info(f"Created Catcher with names {self.names} and scope {self._scope}")

        self.latest_scope_filename = None

    def handle(self, fullname):
        if not self._handle_name(fullname=fullname):
            return False
        if not self._handle_scope():
            return False

        self._store_handled_name(fullname=fullname)
        return True



    @staticmethod
    def _get_scope():
        filename = _get_previous_frame_filename(depth=4)
        return _get_scope_from_filename(filename=filename)

    def _store_handled_name(self, fullname):
        name = _get_top_name(fullname=fullname)
        self.added_names.add(name)
        self.added_fullnames.add(fullname)

    def _handle_name(self, fullname):
        name = _get_top_name(fullname=fullname)
        if self.WILDCARD in self.names:
            return True
        if name in self.names:
            return True
        return False

    def _handle_scope(self):
        if self._scope is None:
            return True
        filename = _get_previous_frame_filename(depth=6)
        self.latest_scope_filename = filename
        return filename.startswith(self._scope)
