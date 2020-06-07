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

1. Ensure all source is contained within a `src` directory
2. All test cases to test a project are contained in a `tests`
   directory.
3. Neither `src` or `tests` directories contain a package initializer
   (no `src/__init__.py` or `tests/__init__.py`)
4. The project's `src` directory minimally contains one package by the
   name of the project since the package is the minimal unit of code
   distribution in Python.
5. Use relative imports for intra-package importation.
6. All _Entry Point_ scripts appear in the `src` directory or a suitable
   namespace directory within source; always _outside_ the top-level
   package. Just import and leverage the top-level package from the
   entry point's `__name__ == '__main__'` code.
   > **Entry points and relative imports:** relative importation is
   > based upon the importing module's **name**. Since the name of the
   > main module is always "`__main__`", modules intended for use as the
   > main module of a Python application **must always** use absolute
   > imports.

