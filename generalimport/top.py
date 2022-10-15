import sys

from generalimport import GeneralImporter, ImportCatcher


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



































