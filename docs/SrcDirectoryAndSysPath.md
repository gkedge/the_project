## The src Directory and sys.path

There are very valid reasons to have a `src` directory within a project.
Most of the reasons pertain to the development testing of packages
intended for publication to PyPi. The definitive treatise on the topic
is covered in the oft referenced article on
[Python Packaging: The Structure, by Ionel Cristian Mărieș(Yonel Cristian Mariesh)](https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure)

\[share
[Python Packaging: The Structure](https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure)]

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
\[Comment out trick and run again.]

#### Just because you can

Now, let's go over something that falls under the category of *just
because you can, doesn't mean...*

\[See run_just_because_you_can.py]

Subscribing to that `src` directory guidance, that guidance infers:
* when importing, don't take advantage of `src` being a *namespace*
  package. *More on when namespace packages are awesome later*
* you need to dynamically augment the `sys.path` to include the `src`
  directory ^§^
* don't introduce a `__init_.py` to make `src` a package ^§^

^§^ These two inferences are related. General Guidance:
> *Never add a package directory, or any directory inside a package,
> directly to `sys.path`. Doing so can easily lead to 'double imports'.*

Since we are recognizing the need to augment the `sys.path` with `src`,
it cannot be a package.  
From
[The Double-Import Trap](http://python-notes.curiousefficiency.org/en/latest/python_concepts/import_traps.html#the-double-import-trap):

> The reason this is problematic is that every module in that directory
> is now potentially accessible under two different names: as a top
> level module (since the directory is on sys.path) and as a submodule
> of the package (if the higher level directory containing the package
> itself is also on sys.path).

My goal is to only ever add the `src` directory (or `src` directories)
to the `sys.path`.

For `pytest` test cases, the most natural location to add the `src`
directory to the `sys.path` is to the `conftest.py`:  
\[See conftest.py]

```
PROJECT_PATH = Path(__file__).parent.absolute()
sys.path.append(str(PROJECT_PATH / 'src'))
```

Running a test, our `sys.path` report will show the addition:

```
sys.path(2 paths):
	/Users/greg/PycharmProjects/the_project
	/Users/greg/PycharmProjects/the_project/src
```

As we learned during the regular Python script running, the `src`
directory would have to be added. \[See `run_the_project_main.py`]

Notice that Pycharm is noting that the `src` packages can't be resolve
statically anymore. This can be solved by telling Pycharm that the `src`
directory is marked as a _Source Root_. This is very important to allow
Pycharm to be able to refactor across the entire project! \[demo]

For another lesson: Having a `src` directory has a *pattern* advantage
when it comes to augmenting `sys.path`: It is a simple pattern to search
for `src` directories throughout the project (including git submodules)
in an automated fashion to augment `sys.path` .

