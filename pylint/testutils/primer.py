import logging
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

    directories: str
    """Directories within the repository to run pylint over"""

    commit: Optional[str] = None
    """Commit hash to pin the repository on"""

    pylint_additional_args: List[str] = []
    """Arguments to give to pylint"""

    pylintrc_relpath: Optional[str] = None
    """Path relative to project's main directory to the pylintrc if it exists"""

    @property
    def pylintrc(self):
        if self.pylintrc_relpath is None:
            return None
        return f"{self.clone_directory}/{self.pylintrc_relpath}"

    @property
    def clone_directory(self) -> Path:
        """Directory to clone repository into"""
        return PRIMER_DIRECTORY_PATH / "/".join(self.url.split("/")[-2:]).replace(
            ".git", ""
        )

    @property
    def paths_to_lint(self) -> List[str]:
        """The paths we need to lint"""
        return [
            f"{self.clone_directory}/{path}" for path in self.directories.split(" ")
        ]

    @property
    def pylint_args(self):
        # We want to test all the code we can
        options = ["--enable-all-extensions", "--enable=all"]
        if self.pylintrc is not None:
            # There is an error if rcfile is given but does not exists
            options += [f"--rcfile={self.pylintrc}"]
        return options + self.pylint_additional_args

    def lazy_clone(self) -> None:
        """Concatenates the target directory and clones the file"""
        logging.info("Lazy cloning %s", self.url)
        if not self.clone_directory.exists():
            options = {
                "url": self.url,
                "to_path": self.clone_directory,
                "branch": self.branch,
                "depth": 1,
            }
            logging.info("Directory does not exists, cloning: %s", options)
            git.Repo.clone_from(**options)
            return
        remote_sha1_commit = (
            git.cmd.Git().ls_remote(self.url, self.branch).split("\t")[0]
        )
        local_sha1_commit = git.Repo(self.clone_directory).head.object.hexsha
        if remote_sha1_commit != local_sha1_commit:
            logging.info(
                "Remote sha is %s while local sha is %s : pulling",
                remote_sha1_commit,
                local_sha1_commit,
            )
            repo = git.Repo(self.clone_directory)
            origin = repo.remotes.origin
            origin.pull()
        else:
            logging.info("Already up to date.")
