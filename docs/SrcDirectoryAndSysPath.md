## The src Directory and sys.path

There are very valid reasons to have a `src` directory within a project.
Most of the reasons pertain to the development testing of packages
intended for publication to PyPi. The definitive treatise on the topic
is covered in the oft referenced article on
[Python Packaging: The Structure, by Ionel Cristian Mărieș(Yonel Cristian Mariesh)](https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure)

Notice that all our source (`the_package` package and
`run_the_project_main.py`) have moved under the `src` directory.

Let's first look at that main now under source. Would you expect that to
run under `src` without augmenting `sys.path`?  
\[See src/run_the_project_main.py]  
\[Run run_the_project_main.py]  
\[Fail pylint]

\[See run_the_project_main_reusable_func.py]  
Would you expect that to work?

\[Run run_the_project_main_reusable_func.py]  
Why did that work? I tricked ya by adding 'src' directory to the the
sys.path.  
\[Comment out trick and run again.]

#### Just because you can

Now, let's go over something that falls under the category of *just
because you can, doesn't mean...*

\[See run_just_because_you_can.py]


Subscribing to that `src` directory guidance, that guidance infers:
* don't introduce a `__init_.py` to make `src` a package
* when importing, don't take advantage of `src` being a *namespace*
  package. *More on namespace packages later*
* you need to dynamically augment the `sys.path` to include the `src`
  directory.

My goal is to only ever add the `src` directory (or `src` directories)
to the `sys.path`.

For `pytest` test cases, the most natural location to add the `src`
directory to the `sys.path` is to the `conftest.py`:  
\[See conftest.py]

```
PROJECT_PATH = Path(__file__).parent
SRC_DIR_STR = str(PROJECT_PATH / 'src')
if SRC_DIR_STR not in sys.path:
    sys.path.append(SRC_DIR_STR)
```

Running a test, our `sys.path` report will show the addition:

```
sys.path(2 paths):
	/Users/greg/PycharmProjects/the_project
	/Users/greg/PycharmProjects/the_project/src
```

As we learned during the For regular Python script running, the `src`
directory would have to be added. \[See `run_the_project_main.py`]

Notice that Pycharm is noting that the `src` packages can't be resolve
statically anymore. This can be solved by telling Pycharm that the `src`
directory is marked as a _Source Root_. This is very important to allow
Pycharm to be able to refactor across the entire project! \[demo]


For another lesson: Having `src` has advantage when it comes to
augmenting `sys.path`: it provides a pattern that can be automated to
alter `sys.path` in the most minimum of ways: only append `src`
directories to `sys.path` throughout the project's directory tree.

> *Hint of things to come:* though there is only one `src` directory at
> this time, later in this tutorial set, we will accommodate `git
> submodules` that will have `src` directories that will be easy to
> programmatically discover to add to `sys.path` at the beginning of
> each run of a script or test case.

