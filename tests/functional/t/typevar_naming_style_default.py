"""Test case for typevar-name-missing-variance with default settings"""

from typing import TypeVar

# PascalCase names with prefix
T_GoodName = TypeVar("T_GoodName")
T_GoodNameWithoutContra = TypeVar(  # [typevar-name-missing-variance]]
    "T_GoodNameWithoutContra", contravariant=True
)
T_GoodName_co = TypeVar("T_GoodName_co", covariant=True)
T_GoodName_contra = TypeVar("T_GoodName_contra", contravariant=True)

# PascalCase names without prefix
BadName = TypeVar("BadName")  # [invalid-name]
BadNameWithoutContra = TypeVar(  # [invalid-name, typevar-name-missing-variance]
    "BadNameWithoutContra", contravariant=True
)
BadName_co = TypeVar("BadName_co", covariant=True)  # [invalid-name]
BadName_contra = TypeVar("BadName_contra", contravariant=True)  # [invalid-name]

# camelCase names with prefix
T_goodName = TypeVar("T_goodName")  # [invalid-name]
T_goodNameWithoutContra = TypeVar(  # [invalid-name, typevar-name-missing-variance]]
    "T_goodNameWithoutContra", contravariant=True
)
T_goodName_co = TypeVar("T_goodName_co", covariant=True)  # [invalid-name]
T_goodName_contra = TypeVar("T_goodName_contra", contravariant=True)  # [invalid-name]
