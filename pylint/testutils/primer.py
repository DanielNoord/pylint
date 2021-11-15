import os
import shutil
from pathlib import Path
from typing import List, NamedTuple, Optional

import git

PRIMER_DIRECTORY_PATH: Path = Path(".pylint_primer_tests")


class PackageToLint(NamedTuple):
    """Represents data about a package to be tested during primer tests"""

    url: str
    """URL of the repository to clone"""

    branch: str
    """Branch of the repository to clone"""

    commit: Optional[str] = None
    """Commit hash to pin the repository on"""

    @property
    def clone_directory(self) -> str:
        """Directory to clone repository into"""
        return str(
            PRIMER_DIRECTORY_PATH
            / "/".join(self.url.split("/")[-2:]).replace(".git", "")
        )

    directories: str
    """Directories within the repository to run pylint over"""

    pylint_additional_args: List[str] = []
    """Arguments to give to pylint"""

    pylintrc: str = "./pylintrc"
    """Path to the pylintrc if it exists"""

    @property
    def paths_to_lint(self) -> List[str]:
        """The paths we need to lint"""
        return [
            f"{self.clone_directory}/{path}" for path in self.directories.split(" ")
        ]

    @property
    def pylint_args(self):
        return [f"--rcfile={self.pylintrc}"] + self.pylint_additional_args

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
        self._lazy_git_clone(self.clone_directory)
