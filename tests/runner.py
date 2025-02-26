from tests.file_tests import run_file_tests
from tests.unit_tests import run_unit_tests


def run_tests():
    """Run all unit and file tests"""
    run_unit_tests()
    run_file_tests('tests')
