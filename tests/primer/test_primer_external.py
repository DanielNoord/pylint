# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

import os
import subprocess

import pytest
from tests.primer.primer_clone_external import clone_primer_packages
from tests.primer.primer_external_packages import PACKAGES_TO_LINT, PRIMER_DIRECTORY


@pytest.mark.primer
def test_primer_external_packages():
    """Downloads external packages and runs pylint over them to check for crashes"""
    clone_primer_packages()
    for data in PACKAGES_TO_LINT.values():
        os.chdir(f"{PRIMER_DIRECTORY}{data.clone_directory}")
        try:
            # We only check for crash and errors as warning are not stable
            # We suppose that errors in a big lib come from a pylint false positive
            subprocess.run(
                ["pylint"] + data.directories.split(" ") + ["--errors-only"],
                check=True,
            )
        except SystemExit as ex:
            assert ex.code == 0
            return
