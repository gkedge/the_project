# [The Project]

[The Project]: #the-project

The Project, provides a foundational introduction to Python(3.3+)'s
modular programming building blocks (modules, packages (including
namespace packages) and explains Python's runtime mechanics of importing
those building blocks. Based on that foundation, the tutorial offers a
reasoned (opinionated!) way to structure a Python project's source and
test code to facilitate modularity.

The 'reasoned' structure strives to achieve modularity goals, use sane
importation practices that avoid programmatic augmentation of sys.path
yet allow for script execution (including test code) to discover modular
packages in cogently, predictable ways.

Each lesson is a branch on this archive:

- TheModule
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

1. Understand Python 3.3+ import rules:
   - based on namespace location (directory) of _Entry Point_ script
   - based on whether `python -m` module option is leveraged
   - based on leveraging `pytest`
2. Limit relative imports to cohesive (`pip`'able) packages (possibly
   including related sub-packages). _NOTE: The following have **no**
   influence on the success or failure to relatively import:_
   * _imported package directory in `sys.path`_
   * _whether a package has a package initializer(`__init__.py`) or
     not_
3. Understand the difference between a regular package and a _namespace_
   package. (Hint: as related to import rules, there is no difference.)
4. All _Entry Point_ scripts (files having a `__main__`) appear in the
   `src` directory or a suitable namespace directory within `src`;
   always _outside_ the packages that make up the implementation. Only
   absolute-import supporting packages.
5. All pytests can import dependencies:
   - weather tester uses `python -m pytest` or `pytest`
   - when executed from within any directory from the project root to
     the test case script's directory inclusive
     (`/path/to/root/tests/**/test_*.py`)

## Opinionated Project Structure

This structure has value beyond easing the implementation of the goals
above.

1. Ensure all project source or shared testing source (shared pytest
   fixtures) are contained within a `src` directory
2. All test cases to test a project are contained in a `tests`
   directory.
3. Neither `src` or `tests` directories contain a package initializer
   (no `src/__init__.py` or `tests/__init__.py`)
4. The project's `src` directory minimally contains one package by the
   name of the project. A package is the minimal unit of publication in
   Python. E.g.: `src/the_project/the_project_impl.py`


### Notes on entry points and relative imports

> * relative importation is based upon the importing module's
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
>   directory to get to a another module in the `tests` directory
>   hierarchy, that relative import will fail. (This is why _Entry
>   Point_ scripts never belong within a package associated with its
>   implementation.

