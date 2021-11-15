# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

import os
import shutil

import git

from pylint.testutils.primer.primer_external_packages import (
    PRIMER_DIRECTORY,
    PackageToLint,
)


def _lazy_git_clone(data: PackageToLint, target_directory: str) -> None:
    """Clones a repository while checking if it hasn't already been cloned"""
    if os.path.exists(target_directory):
        # Get SHA1 hash of latest commit on remote branch
        remote_sha1_commit = (
            git.cmd.Git().ls_remote(data.url, data.branch).split("\t")[0]
        )
        # Get SHA1 hash of latest commit on locally downloaded branch
        local_sha1_commit = git.Repo(target_directory).head.object.hexsha

        if remote_sha1_commit != local_sha1_commit:
            # Remove directory and all its files
            shutil.rmtree(target_directory)
            git.Repo.clone_from(
                data.url,
                target_directory,
            )
    else:
        git.Repo.clone_from(data.url, target_directory, branch=data.branch)


def clone_primer_packages(data: PackageToLint) -> None:
    """Concatenates the target directory and clones the file"""
    target_directory = f"{PRIMER_DIRECTORY}{data.clone_directory}"
    _lazy_git_clone(data, target_directory)
