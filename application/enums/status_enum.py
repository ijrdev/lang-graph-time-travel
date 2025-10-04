from enum import Enum

class StatusEnum(Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    DONE = "DONE"
    ERROR = "ERROR"
    REPROCESS = "REPROCESS"
