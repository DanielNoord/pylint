from typing import NamedTuple, Optional

PRIMER_DIRECTORY = ".pylint_primer_tests"


class PackageToLint(NamedTuple):
    """Represents data about a package to be tested during primer tests"""

    url: str
    """URL of the repository to clone"""

    branch: str
    """Branch of the repository to clone"""

    commit: Optional[str]
    """Commit hash to pin the repository on"""

    clone_directory: str
    """Directory to clone repository in to"""

    directories: str
    """Directories within the repostiory to run pylint over"""


PACKAGES_TO_LINT = {
    "black": PackageToLint(
        "https://github.com/psf/black.git", "main", None, "/psf/black", "src tests"
    ),
    "numpy": PackageToLint(
        "https://github.com/numpy/numpy.git", "main", None, "/numpy/numpy", "numpy"
    ),
}
"""Dictionary of external packages used during the primer test"""
