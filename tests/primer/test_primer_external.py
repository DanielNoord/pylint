# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

import os
import subprocess

import pytest
from tests.primer.primer_clone_external import clone_primer_packages
from tests.primer.primer_external_packages import PACKAGES_TO_LINT, PRIMER_DIRECTORY


class TestPrimer:
    @staticmethod
    @pytest.mark.primer
    @pytest.mark.parametrize(("package"), PACKAGES_TO_LINT)
    def test_primer_external_packages_no_crash(package: str):
        """Runs pylint over external packages to check for crashes"""
        package_data = PACKAGES_TO_LINT[package]

        clone_primer_packages(package_data)

        os.chdir(f"{PRIMER_DIRECTORY}{package_data.clone_directory}")
        try:
            # We only check for crashs
            # We suppose that errors in a big lib come from a pylint false positive
            subprocess.run(
                ["pylint"] + package_data.directories.split(" ") + ["--errors-only"],
                check=True,
            )
        except SystemExit as ex:
            assert ex.code != 32
            return
