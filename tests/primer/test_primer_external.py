# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
import subprocess
from pathlib import Path

import pytest

from pylint.testutils.primer import PackageToLint

PRIMER_DIRECTORY = Path(".pylint_primer_tests/").resolve()
PACKAGES_TO_LINT = {
    "black": PackageToLint(
        url="https://github.com/psf/black.git",
        branch="main",
        commit=None,
        clone_directory="psf/black",
        directories="src tests",
    ),
    "home-assistant": PackageToLint(
        url="https://github.com/home-assistant/core.git",
        branch="dev",
        commit=None,
        clone_directory="home-assistant/core",
        directories="homeassistant",
    ),
    "graph-explorer": PackageToLint(
        url="https://github.com/vimeo/graph-explorer",
        branch="master",
        commit=None,
        clone_directory="vimeo/graph-explorer",
        directories="graph_explorer",
        pylintrc=".pylintrc",
    ),
    "pygame": PackageToLint(
        url="https://github.com/pygame/pygame",
        branch="main",
        commit=None,
        clone_directory="pygame/pygame",
        directories="src_py",
    ),
}
"""Dictionary of external packages used during the primer test"""


class TestPrimer:
    @staticmethod
    @pytest.mark.primer
    @pytest.mark.parametrize("package", PACKAGES_TO_LINT.values(), ids=PACKAGES_TO_LINT)
    def test_primer_external_packages_no_crash(package: PackageToLint) -> None:
        """Runs pylint over external packages to check for crashes and fatal messages

        We only check for crashes (bit-encoded exit code 32) and
        fatal messages (bit-encoded exit code 1). We assume that these external repositories
        do not have any fatal errors in their code so that any fatal errors are pylint false
        positives
        """
        package.clone()
        try:
            subprocess.run(
                ["pylint"]
                + [
                    f"{PRIMER_DIRECTORY}{package.clone_directory}/{i}"
                    for i in package.directories.split(" ")
                ]
                + package.pylint_args,
                check=True,
            )
        except subprocess.CalledProcessError as ex:
            msg = f"Encountered {{}} during primer test for {package}"
            assert ex.returncode != 32, msg.format("a crash")
            assert ex.returncode % 2 == 0, msg.format("a message of category 'fatal'")
