import sys

from generalimport import FakeModule, MissingDependencyException
from generalimport.general_importer import GeneralImporter
from generalimport.import_catcher import ImportCatcher


def _assert_no_dots(names):
    for name in names:
        assert "." not in name, f"Dot found in '{name}', only provide package without dots."

def get_importer():
    """ Return existing or new GeneralImporter instance. """
    return GeneralImporter.singleton_instance or GeneralImporter()

def generalimport(*names, message=None):
    """ Adds names to a new ImportCatcher instance.
        Creates GeneralImporter instance if it doesn't exist. """
    # print(get_previous_frame_filename())
    _assert_no_dots(names=names)
    catcher = ImportCatcher(*names, message=message)
    get_importer().catchers.append(catcher)
    return catcher



def _pop_imported_modules():
    for catcher in get_importer().catchers:
        for fullname in catcher.added_fullnames:
            sys.modules.pop(fullname, None)

def _clear_importer():
    importer = get_importer()
    sys.meta_path.remove(importer)
    importer.catchers.clear()
    GeneralImporter.singleton_instance = None

def reset_generalimport():
    _pop_imported_modules()
    _clear_importer()


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
