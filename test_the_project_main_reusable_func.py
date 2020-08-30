from run_the_project_main import main_reusable_func


def test_the_project_main_reusable_func():
    result: str = main_reusable_func()
    print(result)
    assert result == (
        "Exercise module0.py:func0 (with help from: utils.py:util0) on class module0.py:Module0."
    )
