## [The Module]

Every project starts small. We are starting with a flat, unrecommended
file structure just to show simple access to a module in a directory
from a sibling test case. \[`test_module0.py`]

There is nothing special with Python to statically (no runtime, dynamic
alteration of the `sys.path`) access the imported module. If Pycharm
couldn't find the import, it would have a red underline under it.  
*Picture of red underline*

Because, it is statically accessible, Pycharm can navigate directly to a
dependency with a click. It can also dependably refactor updating all
usages of a change. \[demo Module0 name refactor]

> **Reason**: Python automatically adds the parent directory containing
> of the execution script to `sys.path` at runtime. Equally notable is
> that **no part** of the parental chain of that directory OR the
> current working directory is placed in the `sys.path`! That the
> current working directory is the same location as the script being
> executed is a rare case of serendipity.

To better illustrate what is being added to `sys.path`, tests will print
out the `sys.path` contents at the start of execution. \[open
`conftest.py`]

```
sys.path(1 paths):
	/Users/greg/PycharmProjects/the_project
```

The output is filtered to just show `sys.path` additions related to the
project; no system or site-package paths. \[run `test_module` and
highlight `sys.path in output]

Developers can run pytests in two different ways:
- `python -p pytest test_script.py` OR
- `pytest test_script.py`

Their primary difference lies with the fact that calling via `python -p
pytest` **will** add the current working directory to `sys.path` in
addition to `test_script.py`'s parent directory. Due to the the nature
of using `pytest` this way, calling `pytest` directly will become
unusable over time as code becomes relient upon the inclusion of the
working directory. This be sad for all IDE test runner goodness.

For the case of [The Module] demo with both module and test being in the
same directory, there is no difference. But, I want to make sure through
each demo that follows, both ways to start a `pytest` work. So, all the
tests that are added for these demos will be run sequentially using both
command patterns via \[test_all_the_tests_on_cli.py] \[run
`test_all_the_tests_on_cli.py`]

> Q: If relying upon dynamic augmentation of `sys.path` is eradicated,
> can't we rely on `*.ini` files? E.g.: `pytest.ini`

[The Module]: #the-module

