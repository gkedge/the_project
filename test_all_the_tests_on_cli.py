TESTS: List[TestCasePaths] = [
    TestCasePaths.gen_test_case_paths(PROJECT_PATH, Path('test_module0.py')),
    TestCasePaths.gen_test_case_paths(PROJECT_PATH, Path('test_package.py')),
    TestCasePaths.gen_test_case_paths(PROJECT_PATH, Path('test_the_project_main_reusable_func.py')),
    TestCasePaths.gen_test_case_paths(PROJECT_PATH, Path('src/run_the_project_main.py')),
    TestCasePaths.gen_test_case_paths(PROJECT_PATH, Path('run_just_because_you_can.py')),
    # TestCasePaths.gen_test_case_paths(PROJECT_PATH, Path('run_the_project_main_reusable_func.py')),
]
