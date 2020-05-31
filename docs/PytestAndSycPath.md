## The pytest and sys.path
[The pytest and sys.path]: #the-pytest-and-syspath
All `pytest`'s are now under the `tests` directory as they should be.

As noted in the [SrcDirectoryAndSysPath](./SrcDirectoryAndSysPath.md)
lesson, `src` should never be a package. Same applies to the `tests`
directory; never put a `__init__.py` in `test`. Since you will execute
test cases in the `tests` directory, `tests` is automatically added to
the `sys.path`. And...

> \[Adding a package to `sys.path`] is problematic in that every module
> in that directory is now potentially accessible under two different
> names: as a top level module (since the directory is on sys.path) and
> as a submodule of the package (if the higher level directory
> containing the package itself is also on sys.path).

