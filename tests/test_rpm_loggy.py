from pathlib import Path

import pytest
from loggy import App


TESTS_DIR = Path(__file__).parent
DATA_DIR = TESTS_DIR / "data"


@pytest.fixture()
def unpackaged_files_log():
    return DATA_DIR / "unpackaged_files.txt"


@pytest.fixture()
def missing_build_deps_log():
    return DATA_DIR / "missing_build_deps.txt"


def test_unpackaged_files(unpackaged_files_log):
    a = App()
    result = a.parse_build_log(unpackaged_files_log)

    assert (
        "Installed (but unpackaged) file(s) found:\n"
        "   /usr/lib/python3.11/site-packages/ogr-0.41.1."
        "dev5+gde29f3a.d20221209-py3.11.egg-info/PKG-INFO"
    ) in result["File not listed in %files"]["details"]


def test_missing_build_deps(missing_build_deps_log):
    a = App()
    result = a.parse_build_log(missing_build_deps_log)

    assert (
        "        python3dist(setuptools-scm-git-archive) is needed by python-ogr-"
        "0.41.1.dev5+gde29f3a-1.20221214163333694618.main.5.gde29f3a.fc37.noarch\n"
    ) == result["Build dependency not installed"]["details"]
