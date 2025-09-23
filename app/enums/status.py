from enum import Enum


class StatusEnum(str, Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    SOLD = "sold"