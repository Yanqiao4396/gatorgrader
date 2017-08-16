""" GatorGrader tests for files """

import pytest

import gatorgrader_files


files = pytest.mark.skipif(
    not pytest.config.getoption("--runfiles"),
    reason="needs the --runfiles option to run")


@files
def test_file_exists_in_directory(checkfile, directory):
    """ Check that the file exists in the directory """
    print("file", checkfile)
    print("directory", directory)
