from the_project_main import main


def test_the_project_main():
    result: str = main()
    print(result)
    assert result == ('Exercise module0.py:func0 (with help from: utils.py:util0) on class '
                      'module0.py:Module0.')
