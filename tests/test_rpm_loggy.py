import inspect
from pathlib import Path

import pytest
from loggy import App


TESTS_DIR = Path(__file__).parent
DATA_DIR = TESTS_DIR / "data"


@pytest.fixture()
def unpackaged_files_log():
    return DATA_DIR / "unpackaged_files.txt"

def test_unpackaged_files(unpackaged_files_log):
    a = App()
    result = a.parse_build_log(unpackaged_files_log)

    assert (
               "Installed (but unpackaged) file(s) found:\n"
               "   /usr/lib/python3.11/site-packages/ogr-0.41.1.dev5+gde29f3a.d20221209-py3.11.egg-info/PKG-INFO"
            ) in result["File not listed in %files"]["details"]
