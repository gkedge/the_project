import pytest


# @pytest.mark.xfail  # Should this be deleted or uncommented?
def test_can_test_case_import_from_root_dir():
    try:
        import can_test_case_import  # in root directory...

        print("Really? Test case imported a module from the root directory?\n"
              "That seems strange since I am not augmenting sys.path... Promise!\n")
    except ImportError as e:
        pytest.fail("No, you cannot import 'can_test_case_import' in the root directory. Whew.")
