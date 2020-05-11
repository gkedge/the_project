## [The Module]

Every big_project starts small. We are starting with a flat, unrecommended file structure just to show simple access to a module in a directory from a sibling test case. \[`test_module0.py`]

There is nothing special with Python to statically (no runtime, dynamic alteration of the `sys.path`) access the imported module. If Pycharm couldn't find the import, it would have a red underline under it.  
*Picture of red underline*

Because, it is statically accessible, Pycharm can navigate directly to a dependency with a click. It can also dependably refactor updating all usages of a change. \[demo Module0 name refactor]

> **Reason**: Python automatically puts the directory containing the execution script in the `sys.path` for you at runtime. Equally notable is that **no part** of the parental chain of that directory OR the current working directory is placed in the `sys.path`! That the current working directory is the same location as the script being executed is a very rare and unusual case of serendipity.

To better illustrate what is being added to `sys.path`, tests will print out the `sys.path` contents at the start of execution.  \[open `conftest.py`]

```
sys.path(1 paths):
	/Users/greg/PycharmProjects/big_project
```

The print out is filtered to just show `sys.path` augmentation related to project; no system or site-package paths. \[run `test_module` and highlight `sys.path in output]

Developers can run pytests in two different ways:
- `python -p pytest test_script.py` OR
- `pytest test_script.py`

Their primary difference lies with the fact that calling via `python -p pytest` **will** add the current working directory to `sys.path` in addition to the directory location of the `test_script.py`. Due to the the nature of using `pytest` this way, calling `pytest` directly will become unusable over time. This be sad for all IDE test runner goodness.


For the case of [The Module] demo with both module and test being in the same directory, there is no difference. But, I want to make sure through each demo that follows, both ways to start a `pytest` work. So, all the tests that are added for these demos will be run sequentially using both command patterns via \[test_all_the_tests_on_cli.py] \[run `test_all_the_tests_on_cli.py`]

> If relying upon dynamic augmentation of `sys.path` is eradicated, can't we rely on `*.ini` files? E.g.: `pytest.ini`

[The Module]: #the-module

