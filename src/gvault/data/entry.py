import enum
import json
import dataclasses


class EntryDataType(enum.StrEnum):
    ACCOUNT = "account"
    MESSAGE = "message"
    CARD = "card"


@dataclasses.dataclass
class BaseEntryData:
    entry_type: EntryDataType
    