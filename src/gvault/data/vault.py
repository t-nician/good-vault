import dataclasses

from gvault import tool
from gvault.data import entry


@dataclasses.dataclass
class VaultData(tool.DataToDictHandler):
    encrypted_entries: list[entry.EncryptedEntryData] = dataclasses.field(
        metadata={"save": True},
        default_factory=list
    )
    
    decrypted_entries: list[
        entry.AccountEntryData
        | entry.FileEntryData
        | entry.NoteEntryData
    ] = dataclasses.field(
        metadata={"save": True},
        default_factory=list
    )
    
    