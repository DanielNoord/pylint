# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Helper for primer tests"""

__all__ = [
    "clone_primer_packages",
    "PackageToLint",
    "PRIMER_DIRECTORY",
]

from pylint.testutils.primer.primer_clone_external import clone_primer_packages
from pylint.testutils.primer.primer_external_packages import (
    PRIMER_DIRECTORY,
    PackageToLint,
)
