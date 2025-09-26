from enum import Enum

class StatusEnum(Enum):
    PENDING = "PENDING"
    REPROCESS = "REPROCESS"
    PROCESSING = "PROCESSING"
    DONE = "DONE"
    ERROR = "ERROR"
