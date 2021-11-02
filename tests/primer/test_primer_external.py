# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

import subprocess

import pytest
from tests.primer.primer_clone_external import clone_primer_packages
from tests.primer.primer_external_packages import PACKAGES_TO_LINT, PRIMER_DIRECTORY


class TestPrimer:
    @staticmethod
    @pytest.mark.primer
    @pytest.mark.parametrize(("package"), PACKAGES_TO_LINT)
    def test_primer_external_packages_no_crash(package: str) -> None:
        """Runs pylint over external packages to check for crashes and fatal messages

        We only check for crashes (bit-encoded exit code 32) and
        fatal messages (bit-encoded exit code 1). We assume that these external repositories
        do not have any fatal errors in their code so that any fatal errors are pylint false
        positives
        """
        package_data = PACKAGES_TO_LINT[package]

        # Clone the packages repository
        clone_primer_packages(package_data)

        try:
            subprocess.run(
                ["pylint"]
                + [
                    f"{PRIMER_DIRECTORY}{package_data.clone_directory}/{i}"
                    for i in package_data.directories.split(" ")
                ]
                + ["--errors-only", "--rcfile=./pylintrc"],
                check=True,
            )
        except subprocess.CalledProcessError as ex:
            assert ex.returncode != 32  # Crash
            assert ex.returncode % 2 == 0  # Message of category Fatal has
