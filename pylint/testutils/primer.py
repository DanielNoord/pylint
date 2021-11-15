import os
import shutil
from typing import NamedTuple, Optional

import git

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
    """Directories within the repository to run pylint over"""

    def _lazy_git_clone(self, target_directory: str) -> None:
        """Clones a repository while checking if it hasn't already been cloned"""
        if os.path.exists(target_directory):
            # Get SHA1 hash of latest commit on remote branch
            remote_sha1_commit = (
                git.cmd.Git().ls_remote(self.url, self.branch).split("\t")[0]
            )
            # Get SHA1 hash of latest commit on locally downloaded branch
            local_sha1_commit = git.Repo(target_directory).head.object.hexsha
            if remote_sha1_commit != local_sha1_commit:
                # Remove directory and all its files
                shutil.rmtree(target_directory)
                git.Repo.clone_from(self.url, target_directory)
        else:
            git.Repo.clone_from(self.url, target_directory, branch=self.branch)

    def clone(self) -> None:
        """Concatenates the target directory and clones the file"""
        target_directory = f"{PRIMER_DIRECTORY}{self.clone_directory}"
        self._lazy_git_clone(target_directory)
