import json

from gvault.core.data import EntryData, ItemData, ItemType

from Crypto.Cipher import AES
from dataclasses import dataclass, field, asdict

@dataclass
class ItemInstance:
    item_data: ItemData


@dataclass
class EntryInstance:
    entry_data: EntryData = field(default_factory=EntryData)
    
    def create_item(self) -> ItemInstance:
        pass


@dataclass
class VaultInstance:
    """
    key: 16 or 32 characters long
    vault_data: list[EntryData] or json string
    """
    key: bytes | None = field(default=None)
    vault_data: list[EntryData] | str = field(default_factory=list)

    def __post_init__(self):
        if type(self.vault_data) is not EntryData:
            self.vault_data = json.loads(self.vault_data)
    

    def create_entry(self) -> EntryInstance:
        pass