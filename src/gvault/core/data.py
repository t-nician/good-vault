from enum import Enum
from dataclasses import dataclass, field


class ItemType(Enum):
    ENCRYPTED = "encrypted"
    PRIVATE = "private"

    DECRYPTED = "decrypted"
    PUBLIC = "public"


@dataclass
class ItemData:
    name: str = field(default="")
    note: str = field(default="")
    value: bytes | str = field(default="")

    nonce: bytes = field(default=b"")
    type: ItemType = field(default=ItemType.DECRYPTED)


@dataclass
class EntryData:
    name: str = field(default="")
    note: str = field(default="")
    items: list[ItemData] = field(default_factory=list)

