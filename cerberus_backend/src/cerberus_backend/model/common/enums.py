from enum import StrEnum


class ParamType(StrEnum):
    STRING = "STRING"
    INTEGER = "INTEGER"
    BOOLEAN = "BOOLEAN"


class UserRole(StrEnum):
    USER = "USER"
    ADMIN = "ADMIN"

class TaskStatus(StrEnum): 
    PENDING = "PENDING"
    SENT = "SENT"
    FAILED = "FAILED"
    SUCCESSFUL = "SUCCESSFUL"