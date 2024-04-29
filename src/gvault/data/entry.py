import enum
import json

import dataclasses


class EntryDataType(enum.StrEnum):
    """Available EntryData types.
    """
    ENCRYPTED = "encrypted"
    ACCOUNT = "account"
    NOTE = "note"


@dataclasses.dataclass
class BaseEntryData:
    """
        Core data for all EntryData.
    """
    entry_type: EntryDataType


def to_dict(self) -> dict:
    return {}
