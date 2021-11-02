# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

import subprocess

import pytest
from tests.primer.primer_clone_external import clone_primer_packages
from tests.primer.primer_external_packages import (
    PACKAGES_TO_LINT,
    PRIMER_DIRECTORY,
    PackageToLint,
)


class TestPrimer:
    @staticmethod
    @pytest.mark.primer
    @pytest.mark.parametrize(("package"), PACKAGES_TO_LINT.values())
    def test_primer_external_packages_no_crash(package: PackageToLint):
        """Runs pylint over external packages to check for crashes"""
        clone_primer_packages(package)

        try:
            # We only check for crashes
            # We suppose that errors in a big lib come from a pylint false positive
            subprocess.run(
                ["pylint"]
                + [
                    f"{PRIMER_DIRECTORY}{package.clone_directory}/{i}"
                    for i in package.directories.split(" ")
                ]
                + ["--errors-only", "--rcfile=./pylintrc"],
                check=True,
            )
        except subprocess.CalledProcessError as ex:
            assert ex.returncode != 32
