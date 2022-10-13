from generalimport import GeneralImporter, FakeModule, ImportCatcher
import sys


def _assert_no_dots(names):
    for name in names:
        assert "." not in name, f"Dot found in '{name}', only provide package without dots."

def get_importer():
    """ Return existing or new GeneralImporter instance. """
    return GeneralImporter.singleton_instance or GeneralImporter()

def generalimport(*names):
    """ Adds names to a new ImportCatcher instance.
        Creates GeneralImporter instance if it doesn't exist. """
    # print(get_previous_frame_filename())
    _assert_no_dots(names=names)
    catcher = ImportCatcher(*names)
    get_importer().catchers.append(catcher)
    return catcher

def fake_module_check(obj, error=True):
    """ Simple assertion to trigger error_func earlier if module isn't installed. """
    if isinstance(obj, FakeModule):
        if error:
            obj.error_func()
        else:
            return True
    else:
        return False


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



































