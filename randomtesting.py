from generalimport import generalimport

generalimport("*")

class GeneralImporter:
    names = set()

    def find_module(self, fullname, path=None):
        if fullname in self.names:
            return None

        print("find", fullname)
        self.names.add(fullname)
        print("hi", import_module(name=fullname, error=False))
        sys.modules.pop(fullname, None)
        return self

    def load_module(self, fullname):
        print("load", fullname)
        sys.modules[fullname] = 5

# sys.meta_path.insert(0, GeneralImporter())
#
# import generalvector
# print(generalvector)


