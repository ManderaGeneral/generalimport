# generalimport
Handle all your optional dependencies with a single call!

## Contents
<pre>
<a href='#generalimport'>generalimport</a>
├─ <a href='#Dependency-Diagram'>Dependency Diagram</a>
├─ <a href='#Installation-showing-dependencies'>Installation showing dependencies</a>
├─ <a href='#Information'>Information</a>
├─ <a href='#Examples'>Examples</a>
│  ├─ <a href='#Minimal-Example'>Minimal Example</a>
│  ├─ <a href='#Tests-Showcase'>Tests Showcase</a>
│  ├─ <a href='#Recommended-Installation'>Recommended Installation</a>
│  └─ <a href='#How-It-Works'>How It Works</a>
├─ <a href='#Attributes'>Attributes</a>
├─ <a href='#Contributions'>Contributions</a>
└─ <a href='#Todo'>Todo</a>
</pre>

## Dependency Diagram
```mermaid
flowchart LR
2([file]) --> 4([packager])
1([library]) --> 4([packager])
0([import]) --> 1([library])
0([import]) --> 2([file])
1([library]) --> 2([file])
1([library]) --> 3([vector])
click 0 "https://github.com/ManderaGeneral/generalimport"
click 1 "https://github.com/ManderaGeneral/generallibrary"
click 2 "https://github.com/ManderaGeneral/generalfile"
click 3 "https://github.com/ManderaGeneral/generalvector"
click 4 "https://github.com/ManderaGeneral/generalpackager"
style 0 fill:#482
```

## Installation showing dependencies
| `pip install`     | `generalimport`   |
|:------------------|:------------------|
| *No dependencies* | ✔️                |

## Information
| Package                                                          | Ver                                              | Latest Release        | Python                                                                                                                                                                                  | Platform        | Cover   |
|:-----------------------------------------------------------------|:-------------------------------------------------|:----------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------|:--------|
| [generalimport](https://github.com/ManderaGeneral/generalimport) | [0.2.1](https://pypi.org/project/generalimport/) | 2022-10-07 16:07 CEST | [3.8](https://www.python.org/downloads/release/python-380/), [3.9](https://www.python.org/downloads/release/python-390/), [3.10](https://www.python.org/downloads/release/python-3100/) | Windows, Ubuntu | 98.4 %  |

## Examples

### Minimal Example

Call `generalimport` before importing any optional dependencies.

Here is a minimal example:

``` python
from generalimport import generalimport
generalimport("notinstalled")

from notinstalled import missing_func  # No error

missing_func()  # Error occurs here
```


```
MissingOptionalDependency: Optional dependency 'notinstalled' was used but it isn't installed.
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
from generalimport import generalimport
generalimport("optional_uninstalled_package")

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
from generalimport import generalimport
generalimport("your", "optional", "dependencies")
```

This is all you need to write to use this package.

You can also write `generalimport("*")` to make **any** package importable.

### How It Works


- When `generalimport` is instantiated it creates a new importer for `sys.meta_path`.
- This importer will return 'fake' modules for specified names.
- The fake module will recursively return itself when asked for an attribute.
- When used in any way (\_\_call\_\_, \_\_add\_\_, \_\_str\_\_ etc) it raises `generalimport.MissingOptionalDependency`.
- This exception has the 'skip-exceptions' from `unittest` and `pytest` as bases, which means that tests will automatically be skipped.

## Attributes
<pre>
<a href='https://github.com/ManderaGeneral/generalimport/blob/master/generalimport/__init__.py#L1'>Module: generalimport</a>
├─ <a href='https://github.com/ManderaGeneral/generalimport/blob/master/generalimport/fake_module.py#L4'>Class: FakeModule</a> <b>(Untested)</b>
│  └─ <a href='https://github.com/ManderaGeneral/generalimport/blob/master/generalimport/fake_module.py#L17'>Method: error_func</a> <b>(Untested)</b>
├─ <a href='https://github.com/ManderaGeneral/generalimport/blob/master/generalimport/general_importer.py#L8'>Class: GeneralImporter</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalimport/blob/master/generalimport/general_importer.py#L23'>Method: catch</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalimport/blob/master/generalimport/general_importer.py#L47'>Method: create_module</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalimport/blob/master/generalimport/general_importer.py#L50'>Method: exec_module</a> <b>(Untested)</b>
│  └─ <a href='https://github.com/ManderaGeneral/generalimport/blob/master/generalimport/general_importer.py#L31'>Method: find_spec</a> <b>(Untested)</b>
├─ <a href='https://github.com/ManderaGeneral/generalimport/blob/master/generalimport/import_catcher.py#L6'>Class: ImportCatcher</a> <b>(Untested)</b>
│  └─ <a href='https://github.com/ManderaGeneral/generalimport/blob/master/generalimport/import_catcher.py#L20'>Method: handle</a> <b>(Untested)</b>
├─ <a href='https://github.com/ManderaGeneral/generalimport/blob/master/generalimport/exception.py#L13'>Class: MissingOptionalDependency</a>
├─ <a href='https://github.com/ManderaGeneral/generalimport/blob/master/generalimport_bottom.py#L63'>Function: fake_module_check</a>
├─ <a href='https://github.com/ManderaGeneral/generalimport/blob/master/generalimport/top.py#L14'>Function: generalimport</a>
├─ <a href='https://github.com/ManderaGeneral/generalimport/blob/master/generalimport/top.py#L10'>Function: get_importer</a>
├─ <a href='https://github.com/ManderaGeneral/generalimport/blob/master/generalimport_bottom.py#L7'>Function: get_installed_modules_names</a>
├─ <a href='https://github.com/ManderaGeneral/generalimport/blob/master/generalimport_bottom.py#L42'>Function: get_spec</a> <b>(Untested)</b>
├─ <a href='https://github.com/ManderaGeneral/generalimport/blob/master/generalimport_bottom.py#L29'>Function: import_module</a>
├─ <a href='https://github.com/ManderaGeneral/generalimport/blob/master/generalimport_bottom.py#L13'>Function: module_is_installed</a>
├─ <a href='https://github.com/ManderaGeneral/generalimport/blob/master/generalimport_bottom.py#L48'>Function: module_is_namespace</a> <b>(Untested)</b>
├─ <a href='https://github.com/ManderaGeneral/generalimport/blob/master/generalimport_bottom.py#L52'>Function: module_name_is_namespace</a>
├─ <a href='https://github.com/ManderaGeneral/generalimport/blob/master/generalimport/top.py#L36'>Function: reset_generalimport</a>
└─ <a href='https://github.com/ManderaGeneral/generalimport/blob/master/generalimport_bottom.py#L45'>Function: spec_is_namespace</a> <b>(Untested)</b>
</pre>

## Contributions
Issue-creation and discussions are most welcome!

Pull requests are not wanted, please discuss with me before investing any time

## Todo
| Module                                                                                                                                     | Message                                                                                                                                                                  |
|:-------------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| <a href='https://github.com/ManderaGeneral/generalimport/blob/master/generalimport/generalimport_bottom.py#L1'>generalimport_bottom.py</a> | <a href='https://github.com/ManderaGeneral/generalimport/blob/master/generalimport/generalimport_bottom.py#L16'>Change back to find_spec if spec_is_namespace works.</a> |

<sup>
Generated 2022-10-15 08:45 CEST for commit <a href='https://github.com/ManderaGeneral/generalimport/commit/master'>master</a>.
</sup>
