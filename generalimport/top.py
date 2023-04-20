from typing import List, Union, Tuple

import sys

from generalimport import GeneralImporter, ImportCatcher


def _assert_no_dots(names):
    for name in names:
        assert "." not in name, f"Dot found in '{name}', only provide package without dots."

def get_importer():
    """ Return existing or new GeneralImporter instance. """
    return GeneralImporter.singleton_instance or GeneralImporter()

def generalimport(*name_message_pairs: List[Union[str, Tuple[str, str]]]):
    """ Adds names to a new ImportCatcher instance.
        Creates GeneralImporter instance if it doesn't exist. """
    # print(get_previous_frame_filename())
    names = [n[0] if isinstance(n, Tuple) else n for n in name_message_pairs]
    messages = {m[0]: m[1] for m in name_message_pairs if isinstance(m, Tuple)}
    _assert_no_dots(names=names)
    catcher = ImportCatcher(*names)
    get_importer().messages.update(messages)
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



































