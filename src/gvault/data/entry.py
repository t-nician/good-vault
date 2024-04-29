import enum
import uuid
import json

import dataclasses

from gvault import tool

class EntryDataType(enum.StrEnum):
    """Available EntryData types.
    """
    ENCRYPTED = "encrypted"
    ACCOUNT = "account"
    NOTE = "note"
    NONE = "none"


@dataclasses.dataclass
class BaseEntryData(tool.DataToDictHandler):
    """
        Core data for all EntryData.
    """
    entry_type: EntryDataType = dataclasses.field(
        metadata={"save": True, "encrypt": False},
        default=EntryDataType.NONE
    )
    
    entry_uuid: str = dataclasses.field(
        metadata={"save": True, "encrypt": False},
        default_factory=uuid.uuid4
    )


@dataclasses.dataclass
class AccountEntryData(BaseEntryData):
    """AccountEntryData

    account_username:\n      save: True, encrypt: False
    
    account_password:\n      save: True, encrypt: True
    
    account_website:\n      save: True, encrypt: False
    """
    account_username: str = dataclasses.field(
        metadata={"save": True, "encrypt": False},
        default=""
    )
    
    account_password: str = dataclasses.field(
        metadata={"save": True, "encrypt": True},
        default=""
    )
    
    account_website: str = dataclasses.field(
        metadata={"save": True, "encrypt": False},
        default=""
    )
    
    
@dataclasses.dataclass
class FileEntryData(BaseEntryData):
    """FileEntryData

    file_name:\n        save: True, encrypt: False
    
    file_data:\n        save: True, encrypt: True
    """
    file_name: str = dataclasses.field(
        metadata={"save": True, "encrypt": False},
        default=""
    )
    
    file_data: bytes = dataclasses.field(
        metadata={"save": True, "encrypt": True},
        default=b""
    )


@dataclasses.dataclass
class NoteEntryData(BaseEntryData):
    """NoteEntryData

    note_name:\n        save: True, encrypt: False
    
    note_content:\n        save: True, encrypt: True
    """
    note_name: str = dataclasses.field(
        metadata={"save": True, "encrypt": False},
        default=""
    )
    
    note_content: str = dataclasses.field(
        metadata={"save": True, "encrypt": True},
        default=""
    )


@dataclasses.dataclass
class EncryptedEntryData(BaseEntryData):
    """FileEntryData

    encryption_nonce:\n        save: True, encrypt: False
    
    encrypted_data:\n        save: True, encrypt: False
    """
    encryption_nonce: bytes = dataclasses.field(
        metadata={"save": True, "encrypt": False},
        default=""
    )
    
    encrypted_data: bytes = dataclasses.field(
        metadata={"save": True, "encrypt": False},
        default=b""
    )

    