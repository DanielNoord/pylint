# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE


class MissingArgumentManager(Exception):
    """Raised if an ArgumentManager instance to register options to is missing."""


class UnrecognizedArgumentAction(Exception):
    """Raised if an ArgumentManager instance tries to add an argument for which the action
    is not recognized.
    """
