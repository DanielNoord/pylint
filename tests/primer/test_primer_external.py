# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
import logging
import subprocess
from pathlib import Path

import pytest
from pytest import LogCaptureFixture

from pylint.testutils.primer import PackageToLint

PRIMER_DIRECTORY = Path(".pylint_primer_tests/").resolve()
PACKAGES_TO_LINT = {
    "scikit-learn": PackageToLint(
        url="https://github.com/scikit-learn/scikit-learn.git",
        branch="main",
        directories="sklearn",
    ),
    "flask": PackageToLint(
        url="https://github.com/pallets/flask.git",
        branch="main",
        directories="src",
    ),
    "keras": PackageToLint(
        url="https://github.com/keras-team/keras.git",
        branch="master",
        directories="keras",
    ),
    "sentry": PackageToLint(
        url="https://github.com/getsentry/sentry.git",
        branch="master",
        directories="src tests",
    ),
    "django": PackageToLint(
        url="https://github.com/django/django.git",
        branch="main",
        directories="django tests",
    ),
    "pandas": PackageToLint(
        url="https://github.com/pandas-dev/pandas.git",
        branch="master",
        directories="pandas",
    ),
    "black": PackageToLint(
        url="https://github.com/psf/black.git",
        branch="main",
        directories="src tests",
    ),
    "home-assistant": PackageToLint(
        url="https://github.com/home-assistant/core.git",
        branch="dev",
        directories="homeassistant",
    ),
    "graph-explorer": PackageToLint(
        url="https://github.com/vimeo/graph-explorer.git",
        branch="master",
        directories="graph_explorer",
        pylintrc_relpath=".pylintrc",
    ),
    "pygame": PackageToLint(
        url="https://github.com/pygame/pygame.git",
        branch="main",
        directories="src_py",
    ),
}
"""Dictionary of external packages used during the primer test"""


class TestPrimer:
    @staticmethod
    @pytest.mark.primer
    @pytest.mark.parametrize("package", PACKAGES_TO_LINT.values(), ids=PACKAGES_TO_LINT)
    def test_primer_external_packages_no_crash(
        package: PackageToLint,
        caplog: LogCaptureFixture,
    ) -> None:
        """Runs pylint over external packages to check for crashes and fatal messages

        We only check for crashes (bit-encoded exit code 32) and
        fatal messages (bit-encoded exit code 1). We assume that these external repositories
        do not have any fatal errors in their code so that any fatal errors are pylint false
        positives
        """
        caplog.set_level(logging.INFO)
        package.lazy_clone()
        try:
            # We want to test all the code we can
            command = (
                [
                    "pylint",
                    "--enable-all-extensions",
                    "--enable=all",
                    "--disable=duplicate-code",
                ]
                + package.paths_to_lint
                + package.pylint_args
            )
            logging.info(
                "Launching primer '%s':\n%s", package.clone_directory, " ".join(command)
            )
            subprocess.run(command, check=True)

        except subprocess.CalledProcessError as ex:
            msg = f"Encountered {{}} during primer test for {package}"
            assert ex.returncode != 32, msg.format("a crash")
            assert ex.returncode % 2 == 0, msg.format("a message of category 'fatal'")
