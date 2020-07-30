import re
import sys
from pathlib import Path


def _get_sys_path_answer() -> str:
    from runtime_syspath import filtered_sorted_syspath
    sys_path_answer: str = 'if the list below: \n\t* contains 1 entry'
    sys_path_answer = sys_path_answer + '\n\t* it is the directory of this script:'
    sys_path_answer = sys_path_answer + f'\n\t  {Path.cwd()}'
    sys_path_answer = sys_path_answer + '\n\tThen it is as expected...<drumroll>'
    sys_path_answer = sys_path_answer + f"\n\tProject-related members " \
                                        f"of 'sys.path':\n\t\t{filtered_sorted_syspath()}"
    return sys_path_answer


def _get_src_answer() -> str:
    import src
    return f"'src' is a 'namespace package': {str(src)}"


def _get_the_project_answer() -> str:
    import src.the_project
    the_project_str = str(src.the_project)
    the_project_answer: str = re.sub(r"from '.+the_project", "from '.../the_project",
                                     the_project_str)
    the_project_answer = f"{the_project_answer}\n\t'the_package' is a package initializer!"
    return the_project_answer


def _import_with_src_package():
    print("Referencing 'src.the_project.")
    print("Q: What are the project-related members of 'sys.path'?")
    print(f"A: {_get_sys_path_answer()}\n")

    # 'src' has no __init__.py. AND it NEVER should! Why does these imports work?
    import src.the_project
    src.the_project.Module0().func0()
    print("\nExecuting 'src.the_project.Module0.func0()' must have worked.\n")

    print("Q: What is 'src'?")
    print(f'A: {_get_src_answer()}\n')

    print("Q: What is 'the_package'?")
    print(f'A: {_get_the_project_answer()}\n')


def _import_without_src_package():
    print("Referencing 'the_project without 'src'.")

    from runtime_syspath import print_syspath

    project_path = Path(__file__).parent.absolute()
    sys.path.append(str(project_path / 'src'))
    # Now sys.path should contain both the directory containing this script and the 'src' directory.
    print_syspath(sort=False)

    # Though this runs, Pycharm cannot determine references made possible by runtime
    # augmentation of sys.path.  If Pycharm can't find 'the_project' statically, refactoring
    # is severely hampered. There is a fix...
    import the_project
    the_project.Module0().func0()
    print("\nExecuting 'src.the_project.Module0.func0()' must have worked.\n")


if __name__ == '__main__':
    _import_with_src_package()
    _import_without_src_package()
