"""Tests for the input and checking of command-line arguments"""

import pytest

from gator import arguments

EMPTY_STRING = ""
ERROR = "error:"

VERIFIED = True
NOT_VERIFIED = False


@pytest.fixture
def no_gg_args():
    """Return no command-line arguments"""
    return []


@pytest.fixture
def verifiable_gg_args():
    """Return arguments that are verifiable"""
    return ["--directory", "D", "--file", "a"]


# pylint: disable=redefined-outer-name
def test_default_argument_values_correct(no_gg_args):
    """The default command-line arguments are correct"""
    gg_arguments = arguments.parse(no_gg_args)
    arguments_args_verified = arguments.verify(gg_arguments)
    assert arguments_args_verified == NOT_VERIFIED


# pylint: disable=redefined-outer-name
def test_arguments_verified(verifiable_gg_args):
    """Run arguments with verifiable arguments and it is verified"""
    gg_arguments = arguments.parse(verifiable_gg_args)
    gg_args_verified = arguments.verify(gg_arguments)
    assert gg_args_verified == VERIFIED


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--directoryy", "D"]),
        (["--directory", "D", "F"]),
        (["--filles", "F"]),
        (["--file", "m", "f"]),
        (["-file", "f"]),
        (["-directory", "f"]),
    ],
)
def test_module_argument_not_verifiable_syserror(chosen_arguments, capsys):
    """Check that not valid arguments will not verify correctly"""
    with pytest.raises(SystemExit):
        arguments.parse(chosen_arguments)
    standard_out, standard_err = capsys.readouterr()
    assert standard_out is EMPTY_STRING
    assert ERROR in standard_err


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome"]),
        (["--nowelcome", "--directory", "D"]),
        (["--directory", "D"]),
        (["--nowelcome", "--file", "F"]),
        (["--file", "F"]),
    ],
)
def test_invalid_argument_combinations_not_accepted(chosen_arguments):
    """Check that not valid argument combinations do not verify correctly"""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.verify(parsed_arguments)
    assert verified_arguments is False


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome", "--directory", "D", "--file", "f"]),
        (["--nowelcome", "--directory", "D", "--file", "f", "--singlecomments", "2"]),
        (["--nowelcome", "--directory", "D", "--file", "f", "--multicomments", "2"]),
        (["--nowelcome", "--directory", "D", "--file", "f", "--paragraphs", "2"]),
    ],
)
def test_valid_argument_combinations_accepted(chosen_arguments):
    """Check that valid argument combinations do verify correctly"""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.verify(parsed_arguments)
    assert verified_arguments is True


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome"]),
        (["--nowelcome", "--directory", "D"]),
        (["--directory", "D"]),
        (["--nowelcome", "--file", "F"]),
        (["--file", "F"]),
    ],
)
def test_is_valid_file_not_valid(chosen_arguments):
    """Check that invalid argument combinations do not verify correctly"""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_file(parsed_arguments)
    assert verified_arguments is False


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome"]),
        (["--nowelcome", "--directory", "D", "--singlecomments", "2"]),
        (["--nowelcome", "--directory", "D", "--multicomments", "1"]),
        (["--directory", "D", "--singlecomments", "2"]),
        (["--directory", "D", "--multicomments", "3"]),
        (["--nowelcome", "--file", "F", "--singlecomments", "1"]),
        (["--nowelcome", "--file", "F", "--multicomments", "2"]),
        (["--file", "F", "--singlecomments", "1"]),
        (["--file", "F", "--multicomments", "1"]),
    ],
)
def test_is_not_valid_file_not_valid_comments_wrong(chosen_arguments):
    """Check that invalid argument combinations do not verify correctly"""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_comments(parsed_arguments)
    assert verified_arguments is False


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome"]),
        (["--nowelcome", "--directory", "D", "--paragraphs", "2"]),
        (["--directory", "D", "--paragraphs", "2"]),
        (["--nowelcome", "--file", "F", "--paragraphs", "1"]),
        (["--file", "F", "--paragraphs", "1"]),
    ],
)
def test_is_not_valid_file_not_valid_paragraphs_wrong(chosen_arguments):
    """Check that invalid argument combinations do not verify correctly"""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_paragraphs(parsed_arguments)
    assert verified_arguments is False


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome", "--directory", "D", "--file", "f"]),
        (["--nowelcome", "--file", "f", "--directory", "D"]),
        (["--file", "f", "--directory", "D"]),
        (["--directory", "D", "--file", "F"]),
    ],
)
def test_is_valid_file_valid(chosen_arguments):
    """Check that valid argument combinations do not verify correctly"""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_file(parsed_arguments)
    assert verified_arguments is True


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome", "--directory", "D", "--file", "f", "--singlecomments", "2"]),
        (["--nowelcome", "--directory", "D", "--file", "f", "--multicomments", "2"]),
        (["--nowelcome", "--file", "f", "--directory", "D", "--singlecomments", "2"]),
        (["--nowelcome", "--file", "f", "--directory", "D", "--multicomments", "2"]),
        (["--file", "f", "--directory", "D", "--singlecomments", "2"]),
        (["--file", "f", "--directory", "D", "--multicomments", "2"]),
        (["--directory", "D", "--file", "F", "--singlecomments", "2"]),
        (["--directory", "D", "--file", "F", "--multicomments", "2"]),
    ],
)
def test_is_valid_comments_valid(chosen_arguments):
    """Check that valid argument combinations do not verify correctly"""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_comments(parsed_arguments)
    assert verified_arguments is True


@pytest.mark.parametrize(
    "chosen_arguments",
    [
        (["--nowelcome", "--directory", "D", "--file", "f", "--paragraphs", "2"]),
        (["--nowelcome", "--file", "f", "--directory", "D", "--paragraphs", "2"]),
        (["--file", "f", "--directory", "D", "--paragraphs", "2"]),
        (["--directory", "D", "--file", "F", "--paragraphs", "2"]),
    ],
)
def test_is_valid_paragraphs_valid(chosen_arguments):
    """Check that valid argument combinations do not verify correctly"""
    parsed_arguments = arguments.parse(chosen_arguments)
    verified_arguments = arguments.is_valid_paragraphs(parsed_arguments)
    assert verified_arguments is True
