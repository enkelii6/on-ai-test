from enum import StrEnum, unique, auto


@unique
class RoleEnum(StrEnum):
    SYSTEM = auto()
    USER = auto()
