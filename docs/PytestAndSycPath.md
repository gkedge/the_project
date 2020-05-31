## The pytest and sys.path
[The pytest and sys.path]: #the-pytest-and-syspath
All pytests are now under the `tests` directory as they should be. If
you ever make `tests` a package by placing an `__init.py__` the `tests`
directory, you are on the road to ruin. It may get you out of a jam, but
odd test discovery problems may arises(?).
