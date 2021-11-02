# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

import os
import shutil

import git
from tests.primer.primer_external_packages import (
    PACKAGES_TO_LINT,
    PRIMER_DIRECTORY,
    PackageToLint,
)


def _lazy_git_clone(data: PackageToLint, target_directory: str) -> None:
    """Clones a repository while checking if it hasn't already been cloned"""
    if os.path.exists(target_directory):
        remote_sha1_commit = (
            git.cmd.Git().ls_remote(data.url, data.branch).split("\t")[0]
        )
        local_sha1_commit = git.Repo(target_directory).head.object.hexsha
        if remote_sha1_commit != local_sha1_commit:
            shutil.rmtree(target_directory)
            git.Repo.clone_from(
                data.url,
                target_directory,
            )
    else:
        git.Repo.clone_from(data.url, target_directory, branch=data.branch)


def clone_primer_packages() -> None:
    """Iterates over the list of packages to clone"""
    for data in PACKAGES_TO_LINT.values():
        target_directory = f"{PRIMER_DIRECTORY}{data.clone_directory}"
        _lazy_git_clone(data, target_directory)
