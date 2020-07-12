# [The Project]

[The Project]: #the-project

The Project, provides a foundational introduction to Python's modular
programming building blocks (modules, packages (including namespace
packages) and explains Python's runtime mechanics of ingesting
(importing) those building blocks. Based on that foundation, the
tutorial offers a reasoned (opinionated!) way to structure a Python
project's modular source and test code.

The 'reasoned' structure strives to achieve modularity goals, use sane
importation practices that avoid programmatic augmentation of sys.path
yet allow for script execution (including test code) to discover modular
packages in cogently predictable ways.

Each lesson is a branch on this archive:

- [TheModule](./TheModule.md)
- ThePackage
- SrcDirectoryAndSysPath; Part 1
- SrcDirectoryAndSysPath; Part 2
- PytestSysPath
- TheNamespacePackage
- SubProjects
- SubProjectTestSupport
- TheProject

## The Goals
[The Goals]: #the-goals

1. Ensure all source is contained within a `src` directory
2. All test cases to test a project are contained in a `tests`
   directory.
3. Neither `src` or `tests` directories contain a package initializer
   (no `src/__init__.py` or `tests/__init__.py`)
4. The project's `src` directory minimally contains one package by the
   name of the project since the package is the minimal unit of code
   distribution in Python.
5. Use relative imports for intra-package importation; not inter-package
   importation. _The following have **no** influence on the success or
   failure to relatively import:_
   * _members of `sys.path`_
   * _whether a package has a package initializer(`__init__.py`) or
     not(a namespace package)_
6. All _Entry Point_ scripts appear in the `src` directory or a suitable
   namespace directory within `src`; always _outside_ the packages that
   make up the implementation. Just leverage the supporting packages
   using absolute imports.

> **Note on entry points and relative imports:**
> * Relative importation is based upon the importing module's
>   **`__package__`** value. Since a main module's `__package__` is
>   always `None`, a main module is always in the top-level pacakge.
>   Therefore, main module imports **must always** use absolute imports.
>   ~
>   [5.4.4. Import-related module attributes](https://docs.python.org/3/reference/import.html#__package__)
> * For relative imports, the dots `.` can only navigate up to (but not
>   including) the directory containing the script run from the command
>   line. This applies to `pytest` cases within the `tests` directory!
>   Even if a `pytest` test case module sticks to absolute imports
>   within its module, if that imported module attempts to use relative
>   imports that would relatively traverse over the running test case's
>   directory get to a another module in the `tests` directory
>   hierarchy, that relative import will fail.

