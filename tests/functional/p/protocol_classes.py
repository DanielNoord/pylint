# pylint: disable=missing-docstring
import typing


class Hasher(typing.Protocol):
    """A hashing algorithm, e.g. :func:`hashlib.sha256`."""

    def update(self, blob: bytes):
        ...

    def digest(self) -> bytes:
        ...


T_Generic = typing.TypeVar("T_Generic")


class HasherGeneric(typing.Protocol[T_Generic]):
    """A hashing algorithm, e.g. :func:`hashlib.sha256`."""
    def update(self, blob: bytes):
        ...
    def digest(self) -> bytes:
        ...


class Protocol:  #pylint:disable=too-few-public-methods
    pass

class HasherFake(Protocol):
    """A hashing algorithm, e.g. :func:`hashlib.sha256`."""
    def update(self, blob: bytes): # [no-self-use, unused-argument]
        ...
    def digest(self) -> bytes: # [no-self-use]
        ...
