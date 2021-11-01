"""Test case for typevar-name-missing-variance with default settings"""

from typing import TypeVar

# PascalCase names with prefix
T_GoodName = TypeVar("T_GoodName")
_T = TypeVar("_T")
_T_GoodName = TypeVar("_T_GoodName")
T_GoodNameWithoutContra = TypeVar(  # [typevar-name-missing-variance]
    "T_GoodNameWithoutContra", contravariant=True
)
T_GoodName_co = TypeVar("T_GoodName_co", covariant=True)
T_GoodName_contra = TypeVar("T_GoodName_contra", contravariant=True)

# PascalCase names without prefix
AnyStr = TypeVar("AnyStr")
BadNameWithoutContra = TypeVar(  # [typevar-name-missing-variance]
    "BadNameWithoutContra", contravariant=True
)
BadName_co = TypeVar("BadName_co", covariant=True)
BadName_contra = TypeVar("BadName_contra", contravariant=True)

# camelCase names with prefix
T_goodName = TypeVar("T_goodName")  # [invalid-name]
T_goodNameWithoutContra = TypeVar(  # [invalid-name, typevar-name-missing-variance]]
    "T_goodNameWithoutContra", contravariant=True
)
T_goodName_co = TypeVar("T_goodName_co", covariant=True)  # [invalid-name]
T_goodName_contra = TypeVar("T_goodName_contra", contravariant=True)  # [invalid-name]

# PascalCase names with lower letter prefix in tuple assignment
(
    a_BadName,  # [invalid-name]
    a_BadNameWithoutContra,  # [invalid-name, typevar-name-missing-variance]
) = TypeVar("a_BadName"), TypeVar("a_BadNameWithoutContra", contravariant=True)
GoodName_co, a_BadName_contra = TypeVar(  # [invalid-name]
    "GoodName_co", covariant=True
), TypeVar("a_BadName_contra", contravariant=True)
GoodName_co, VAR = TypeVar("GoodName_co", covariant=True), "a string"
