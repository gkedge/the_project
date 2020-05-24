## [The Package]

Still, not the recommended file structure for a project, just a package
example where the `the_project` package is created by having a directory
named `the_project` and minimally contains an `__init__.py` file.

All source (except for the `__main__` `run_the_project_main.py`)
associated with the `the_project` *project* so at this point has been
moved from the project's root directory to the package directory making
them all package members.

\[See `__init__.py` for its public API imports and `test_package.py` to
see how imports don't include the module]

Again, there is nothing special with Python to statically access the
imported `the_project` modules. To statically access the content of
`module0.py` within the package from `test_package.py`, the import:

```
import module0
```

... need only change to prepend the package name:

```
from the_project import Module0
```

Since the `test_package.py` script is in the same directory (project
root directory) as the `the_project` package directory, all imports are
statically discovered by Python & Pycharm automatically. with adding the
directory containing the script run (`test_package.py`) to `sys.path`.

[The Package]: #the-package

