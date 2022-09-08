# generalimport
Handle all your optional dependencies with a single call!

## Contents
<pre>
<a href='#generalimport'>generalimport</a>
├─ <a href='#Examples'>Examples</a>
│  ├─ <a href='#Minimal-Example'>Minimal Example</a>
│  ├─ <a href='#Tests-Showcase'>Tests Showcase</a>
│  ├─ <a href='#Recommended-Installation'>Recommended Installation</a>
│  └─ <a href='#How-It-Works'>How It Works</a>
├─ <a href='#Installation'>Installation</a>
├─ <a href='#Information'>Information</a>
├─ <a href='#Attributes'>Attributes</a>
└─ <a href='#Contributions'>Contributions</a>
</pre>

## Examples

### Minimal Example

Call `GeneralImporter` before importing any optional dependencies.

Here is a minimal example:

``` python
from generalimport import GeneralImporter
GeneralImporter("notinstalled")

import notinstalled  # No error

def func():
    notinstalled.missing_func()  # Error occurs here

func()
```


```
...MissingOptionalDependency: Optional dependency 'notinstalled' was used but it isn't installed.
```

Imports fail when they are **used**, *not* imported.

This means you don't need to keep checking if the package is installed before importing it.
Simply import your optional package and use it like you would any package and let it fail wherever it fails, with a nice error message.

### Tests Showcase

The beauty of this package is that the error raised isn't just any exception.
It has two base classes: `unittest.case.SkipTest` and `_pytest.outcomes.Skipped` (If available).

This means that if a test method uses an uninstalled optional package then that test is automatically skipped.
This means no more manual skip decorators for optional dependencies!

``` python
from generalimport import GeneralImporter
GeneralImporter("optional_uninstalled_package")

from optional_uninstalled_package import missing_func

from unittest import TestCase

class MyTest(TestCase):
    def test_missing_func(self):
        self.assertEqual(3, missing_func(1, 2))
```


```
Ran 1 test in 0.002s

OK (skipped=1)

Skipped: Optional dependency 'optional_uninstalled_package' was used but it isn't installed.
```

### Recommended Installation

I recommend to put this at the top of your main `__init__.py` file.

``` python
from generalimport import GeneralImporter
GeneralImporter("your", "optional", "dependencies")
```

This is all you need to write to use this package.

You can also write `GeneralImporter("*")` to make **any** package importable.

### How It Works


- When `GeneralImporter` is instantiated it creates a new importer for `sys.meta_path`.
- This importer will return 'fake' modules for specified names.
- The fake module will recursively return itself when asked for an attribute.
- When used in any way (\_\_call\_\_, \_\_add\_\_, \_\_str\_\_ etc) it raises `generalimport.MissingOptionalDependency`.
- This exception has the 'skip-exceptions' from `unittest` and `pytest` as bases, which means that tests will automatically be skipped.

## Installation
| Command                     | <a href='https://pypi.org/project/setuptools'>setuptools</a>   |
|:----------------------------|:---------------------------------------------------------------|
| `pip install generalimport` | Yes                                                            |

## Information
| Package                                                          | Ver                                              | Latest Release        | Python                                                                                                                                                                                  | Platform        |   Lvl | Todo                                                      | Cover   |
|:-----------------------------------------------------------------|:-------------------------------------------------|:----------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------|------:|:----------------------------------------------------------|:--------|
| [generalimport](https://github.com/ManderaGeneral/generalimport) | [0.1.2](https://pypi.org/project/generalimport/) | 2022-09-08 21:27 CEST | [3.8](https://www.python.org/downloads/release/python-380/), [3.9](https://www.python.org/downloads/release/python-390/), [3.10](https://www.python.org/downloads/release/python-3100/) | Windows, Ubuntu |     0 | [0](https://github.com/ManderaGeneral/generalimport#Todo) | 97.3 %  |

## Attributes
<pre>
<a href='https://github.com/ManderaGeneral/generalimport/blob/54e4c36/generalimport/__init__.py#L1'>Module: generalimport</a>
├─ <a href='https://github.com/ManderaGeneral/generalimport/blob/54e4c36/generalimport/optional_import.py#L99'>Class: FakeModule</a>
│  └─ <a href='https://github.com/ManderaGeneral/generalimport/blob/54e4c36/generalimport/optional_import.py#L107'>Method: error_func</a>
├─ <a href='https://github.com/ManderaGeneral/generalimport/blob/54e4c36/generalimport/optional_import.py#L45'>Class: GeneralImporter</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalimport/blob/54e4c36/generalimport/optional_import.py#L78'>Method: disable</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalimport/blob/54e4c36/generalimport/optional_import.py#L93'>Method: disable_all</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalimport/blob/54e4c36/generalimport/optional_import.py#L72'>Method: enable</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalimport/blob/54e4c36/generalimport/optional_import.py#L57'>Method: find_module</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalimport/blob/54e4c36/generalimport/optional_import.py#L88'>Method: get_enabled</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalimport/blob/54e4c36/generalimport/optional_import.py#L68'>Method: is_enabled</a>
│  └─ <a href='https://github.com/ManderaGeneral/generalimport/blob/54e4c36/generalimport/optional_import.py#L62'>Method: load_module</a>
├─ <a href='https://github.com/ManderaGeneral/generalimport/blob/54e4c36/generalimport/optional_import.py#L32'>Class: MissingOptionalDependency</a>
├─ <a href='https://github.com/ManderaGeneral/generalimport/blob/54e4c36/generalimport/optional_import.py#L19'>Function: get_installed_packages</a>
├─ <a href='https://github.com/ManderaGeneral/generalimport/blob/54e4c36/generalimport/optional_import.py#L115'>Function: import_module</a>
└─ <a href='https://github.com/ManderaGeneral/generalimport/blob/54e4c36/generalimport/optional_import.py#L23'>Function: package_is_installed</a>
</pre>

## Contributions
Issue-creation and discussion is most welcome!

Pull requests are **not wanted**, please discuss with me before investing any time.


<sup>
Generated 2022-09-08 21:27 CEST for commit <a href='https://github.com/ManderaGeneral/generalimport/commit/54e4c36'>54e4c36</a>.
</sup>
