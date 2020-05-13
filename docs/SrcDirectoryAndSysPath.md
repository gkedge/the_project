## The Source Directory and sys.path
[The Source Directory and `sys.path`]: #thesourcedirectoryandsyspath

There are very valid reasons to have a `src` directory within a project.
Most of the reasons pertain to the development testing of packages
intended for publication to PyPi. The definitive treatise on the topic
is covered in the oft referenced article on
[Python Packaging: The Structure](https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure)

Subscribing to that guidance provides a pattern to alter `sys.path` in
the most minimum of ways: only append `src` directories to `sys.path`

> *Hint of things to come:* though there is only one `src` directory at
> this time, later in this tutorial set, we will accommodate `git
> submodules` that will have `src` directories that will be easy to
> programmatically discover to add to `sys.path` at the beginning of
> each run of a script or test case.

For `pytest` test cases, the most natural location to add the `src`
directory to the `sys.path` is to the `conftest.py`:  
\[See conftest.py]
```
PROJECT_DIR = Path(__file__).parent
sys.path.append(str(PROJECT_DIR / 'src'))
```
Notice that Pycharm is noting that the src packages can't be resolve
statically anymore. This can be solved by telling Pycharm that the `src`
directory is marked as a _Source Root_.

Running a test, our `sys.path` report will show the addition:
```
sys.path(2 paths):
	/Users/greg/PycharmProjects/the_project
	/Users/greg/PycharmProjects/the_project/src
```

For regular Python script running, the `src` directory would have to be
added. \[See the_project_main.py]


