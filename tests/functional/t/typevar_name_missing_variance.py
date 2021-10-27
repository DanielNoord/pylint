"""Test case for typevar-name-missing-variance."""

from typing import TypeVar

# Type variables without variance
T = TypeVar("T")
T_co = TypeVar("T_co")  # [typevar-name-missing-variance]
T_contra = TypeVar("T_contra")  # [typevar-name-missing-variance]

# Type variables not starting with T_
N = TypeVar("N")
N_co = TypeVar("N_co", covariant=True)
N_contra = TypeVar("N_contra", contravariant=True)

# Tests for combinations with contravariance
CT_co = TypeVar("CT_co", contravariant=True)  # [typevar-name-missing-variance]
CT_contra = TypeVar("CT_contra")  # [typevar-name-missing-variance]
CT_contra = TypeVar("CT_contra", contravariant=True)

# Tests for combinations with covariance

VT = TypeVar("VT", covariant=True)  # [typevar-name-missing-variance]
VT_contra = TypeVar("VT_contra", covariant=True)  # [typevar-name-missing-variance]
VT_co = TypeVar("VT_co", covariant=True)
