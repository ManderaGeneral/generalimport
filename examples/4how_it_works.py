"""
 - When `generalimport` is instantiated it creates a new importer for `sys.meta_path`.
 - This importer will return 'fake' modules for specified names.
 - The fake module will recursively return itself when asked for an attribute.
 - When used in any way (\_\_call\_\_, \_\_add\_\_, \_\_str\_\_ etc) it raises `generalimport.MissingOptionalDependency`.
 - This exception has the 'skip-exceptions' from `unittest` and `pytest` as bases, which means that tests will automatically be skipped.
"""
