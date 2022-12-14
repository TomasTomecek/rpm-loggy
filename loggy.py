#!/usr/bin/python3 -tt
# -*- coding: utf-8 -*-
# vim:expandtab:autoindent:tabstop=4:shiftwidth=4:filetype=python:textwidth=0:

import argparse
import logging
import re
from pathlib import Path
from typing import Iterable, Any, Dict

FORMAT = "%(levelname)s: %(message)s"
logging.basicConfig(format=FORMAT, level=logging.WARNING)
logger = logging.getLogger()


class Case:
    """
    We are trying to find known patterns in logs that correspond to specific cases.
    For example if a build dependency is not installed, there will be a known error
    message in the log saying that a header file is missing or a python module
    can't be imported.

    The cases are represented by this class.
    """
    # regular expression that can detect the case
    regex = ""
    # short title for the use case
    title = ""
    # detailed description of the problem with steps how to fix it
    description = ""

    def get_details(self, finds: Iterable[re.Match]) -> str:
        """
        provide details that highlight the problem"""
        return "Nothing"


class MissingFileCase(Case):
    regex = r"File\s+not\s+found:"
    regex_details = ""  # TODO: we need to get the actual filenames
    title = "File not found"  # the most iconic error message
    description = "TBD"


class UnpackagedFileCase(Case):
    regex = r"Installed\s+\(but\s+unpackaged\)\s+file\(s\)\s+found:"
    title = "File not listed in %files"  # the most iconic error message
    description = "TBD"

    def get_details(self, finds: Iterable[re.Match]):
        for f in finds:
            return f.string[f.start():]


class MissingBuildDepCase(Case):
    """
    error: Failed build dependencies:
        python3dist(setuptools-scm-git-archive) is needed by python-ogr-0.41.1.dev5+gde29f3a.d20221209-1.20221209124209182599.main.5.gde29f3a.fc37.noarch
    """
    regex = r"error: Failed\s+build\s+dependencies\:\n"
    title = "Build dependency not installed"
    description = "Your spec file set a build dependency in `BuildRequires` that is not installed."

    def get_details(self, finds: Iterable[re.Match]):
        for f in finds:
            return f.string[f.end():]


# TODO: use decorator
cases = [MissingFileCase, UnpackagedFileCase, MissingBuildDepCase]


def argumentParser():
    parser = argparse.ArgumentParser(
        description="Parses the build.log and return an error why build failed.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-p", "--path", required=True, help="Path to build.log")
    arguments = parser.parse_args()
    return arguments


class App:
    def parse_build_log(self, path: str) -> dict:
        try:
            log_content = Path(path).read_text()
        except IOError as error:
            logger.error("There was an error opening %s, %s", path, error)
            return {}

        result = {}
        for case_kls in cases:
            case = case_kls()
            finds = re.finditer(case.regex, log_content)
            result[case.title]: Dict[str, Any] = {"match": False}
            if finds:
                result[case.title]["match"] = True
                result[case.title]["details"] = case.get_details(finds)

        return result


def main(log_path):
    a = App()
    result = a.parse_build_log(log_path)
    for case_title, content in result.items():
        print(f"{case_title}\n{content['details']}\n\n")


if __name__ == "__main__":
    programArguments = argumentParser()
    main(programArguments.path)
