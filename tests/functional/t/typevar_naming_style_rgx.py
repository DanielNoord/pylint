"""Test case for typevar-name-missing-variance with default settings"""

from typing import TypeVar

# Name set by regex pattern
TypeVarsShouldBeLikeThis = TypeVar("TypeVarsShouldBeLikeThis")
TypeVarsShouldBeLikeThis_contra = TypeVar(
    "TypeVarsShouldBeLikeThis_contra", contravariant=True
)
TypeVarsShouldBeLikeThis_co = TypeVar("TypeVarsShouldBeLikeThis_co", covariant=True)

# Name using the standard style
T_GoodName = TypeVar("T_GoodName")  # [invalid-name]
T_GoodName_co = TypeVar("T_GoodName_co", covariant=True)  # [invalid-name]
T_GoodName_contra = TypeVar("T_GoodName_contra", contravariant=True)  # [invalid-name]
