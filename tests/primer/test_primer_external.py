# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

import subprocess

import pytest

from pylint.testutils.primer import (
    PRIMER_DIRECTORY,
    PackageToLint,
    clone_primer_packages,
)

PACKAGES_TO_LINT = {
    "black": PackageToLint(
        "https://github.com/psf/black.git", "main", None, "/psf/black", "src tests"
    ),
    "home-assistant": PackageToLint(
        "https://github.com/home-assistant/core.git",
        "dev",
        None,
        "/home-assistant/core",
        "homeassistant",
    ),
    "graph-explorer": PackageToLint(
        "https://github.com/vimeo/graph-explorer",
        "master",
        None,
        "/vimeo/graph-explorer",
        "graph_explorer",
    ),
}
"""Dictionary of external packages used during the primer test"""


class TestPrimer:
    @staticmethod
    @pytest.mark.primer
    @pytest.mark.parametrize(
        ("package"), PACKAGES_TO_LINT.values(), ids=PACKAGES_TO_LINT
    )
    def test_primer_external_packages_no_crash(package: PackageToLint) -> None:
        """Runs pylint over external packages to check for crashes and fatal messages

        We only check for crashes (bit-encoded exit code 32) and
        fatal messages (bit-encoded exit code 1). We assume that these external repositories
        do not have any fatal errors in their code so that any fatal errors are pylint false
        positives
        """
        # Clone the packages repository
        clone_primer_packages(package)
        try:
            subprocess.run(
                ["pylint"]
                + [
                    f"{PRIMER_DIRECTORY}{package.clone_directory}/{i}"
                    for i in package.directories.split(" ")
                ]
                + ["--rcfile=./pylintrc"],
                check=True,
            )
        except subprocess.CalledProcessError as ex:
            msg = f"Encountered {{}} during primer test for {package}"
            assert ex.returncode != 32, msg.format("a crash")
            assert ex.returncode % 2 == 0, msg.format("a message of category 'fatal'")
