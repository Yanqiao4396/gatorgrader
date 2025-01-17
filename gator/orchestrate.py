"""Orchestrate the preliminary actions and checks performed on writing and source code."""

import sys

from gator import arguments
from gator import checkers
from gator import constants
from gator import description

from gator import leave
from gator import report

# pylint: disable=unused-import
from gator import display  # noqa: F401
from gator import invoke  # noqa: F401
from gator import run  # noqa: F401

# define the name of this module
ORCHESTRATE = sys.modules[__name__]

# define the modules that contain invokable functions
DISPLAY = sys.modules[constants.modules.Display]
INVOKE = sys.modules[constants.modules.Invoke]
RUN = sys.modules[constants.modules.Run]
REPORT = sys.modules[constants.modules.Report]

# define the format for the output of the checks
OUTPUT_TYPE = getattr(REPORT, constants.outputs.Text)


def parse_arguments(system_arguments):
    """Parse and then return the parsed command-line arguments and those that remain."""
    parsed_arguments, remaining_arguments = arguments.parse(system_arguments)
    return parsed_arguments, remaining_arguments


def verify_arguments(parsed_arguments):
    """Parse, verify, and then return the parsed command-line arguments."""
    # verify the command-line arguments
    did_verify_arguments = arguments.verify(parsed_arguments)
    return did_verify_arguments


def get_actions(parsed_arguments, verification_status):
    """Get the actions to perform before running any specified checker."""
    needed_actions = []
    # Needed Action: display the welcome message
    if parsed_arguments.nowelcome is not True:
        needed_actions.append([DISPLAY, "welcome_message", constants.arguments.Void])
    # Needed Action: configure to produce JSON output for external interface
    if parsed_arguments.json is True:
        # pylint: disable=global-statement
        global OUTPUT_TYPE
        OUTPUT_TYPE = getattr(REPORT, constants.outputs.Json)
    # arguments were not verified, create actions for error message display and an exit
    if verification_status is False:
        # Needed Action: display incorrect arguments message
        needed_actions.append([DISPLAY, "incorrect_message", constants.arguments.Void])
        # Needed Action: display a message to remind about using help
        needed_actions.append([DISPLAY, "help_reminder", constants.arguments.Void])
        # Needed Action: exit the program
        needed_actions.append([RUN, "run_exit", [constants.arguments.Incorrect]])
    return needed_actions


def perform_actions(actions):
    """Perform the specified actions."""
    results = []
    # iteratively run all of the actions in the list
    for module, function, parameters in actions:
        function_to_invoke = getattr(module, function)
        # no parameters were specified, do not pass
        if parameters == []:
            function_result = function_to_invoke()
        # parameters were specified, do pass
        else:
            function_result = function_to_invoke(*parameters)
        results.append(function_result)
    return results


def check(system_arguments):
    """Orchestrate a full check of the specified deliverables."""
    # *Section: Initialize
    # step_results = []
    check_results = []
    # **Step: Parse and then verify the arguments, extract remaining arguments
    parsed_arguments, remaining_arguments = parse_arguments(system_arguments)
    verification_status = verify_arguments(parsed_arguments)
    # **Step: Get the source of all the checkers available from either:
    # --> the internal directory of checkers (e.g., "./gator/checks")
    # --> the directory specified on the command-line
    external_checker_directory = checkers.get_checker_dir(parsed_arguments)
    checker_source = checkers.get_source([external_checker_directory])
    # **Step: Get and perform the preliminary actions before running a checker
    # if the arguments did not parse or verify correctly, then:
    # --> argparse will cause the program to crash with an error OR
    # --> one of the actions will be to display the help message and exit
    actions = get_actions(parsed_arguments, verification_status)
    perform_actions(actions)
    # *Section: Perform the check
    # **Step: Get and transform the name of the chosen checker and
    # then prepare for running it by ensuring that it is:
    # --> available for use (i.e., pluginbase found and loaded it)
    check_name = checkers.get_chosen_check(parsed_arguments)
    check_file = checkers.transform_check(check_name)
    check_exists = checkers.verify_check_existence(check_file, checker_source)
    # **Step: Load the check and verify that it is valid:
    check_verified = False
    check = None
    if check_exists:
        check = checker_source.load_plugin(check_file)
        check_verified = checkers.verify_check_functions(check)
    # produce error message and exit because the check is not valid
    if not check_exists or not check_verified:
        # do not potentially produce the welcome message again
        parsed_arguments.nowelcome = True
        actions = get_actions(parsed_arguments, check_verified)
        perform_actions(actions)
    # **Step: Perform the check since it exists and it is verified
    check_result = check.act(parsed_arguments, remaining_arguments)
    check_results.extend(check_result)
    # *Section: Output the report
    # **Step: get the report's details
    result = report.get_result()
    # **Step: Override the result's description if a user-provided description exists
    result = description.transform_result_dictionary(parsed_arguments, result)
    # **Step: produce the output
    produced_output = report.output(report.get_result(), OUTPUT_TYPE)
    # **Step: display the output
    display.message(produced_output)
    # Section: Return control back to __main__ in gatorgrader
    # Only step: determine the correct exit code for the checks
    correct_exit_code = leave.get_code(check_results)
    return correct_exit_code
