##  The src Directory and sys.path
Now that the `src` directory is marked as a _Source Root_ in PyCharm …

\[run_the_project_main.py]

… and `sys.path` has been augmented with the `the_project/src` directory
…

\[conftest.py]  
\[test_the_project_reusable_func.py]  
… all tests pass with using the current reasonable rules

1. Only add `the_project/src` to `sys.path`.
2. Don't use `src` namespace to access packages.
