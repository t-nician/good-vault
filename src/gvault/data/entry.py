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
    FILE = "file"
    NOTE = "note"
    NONE = "none"


@dataclasses.dataclass
class BaseEntryData(tool.DataToDictHandler):
    """Core data for all EntryData.
    
    entry_type:\n       save: True, encrypt: False
    
    entry_uuid:\n       save: True, encrypt: False
    
    """
    entry_type: EntryDataType = dataclasses.field(
        metadata={"save": True, "encrypt": False},
        default=EntryDataType.NONE
    )
    
    entry_uuid: str = dataclasses.field(
        metadata={"save": True, "encrypt": False},
        default_factory=lambda: uuid.uuid4().hex
    )


@dataclasses.dataclass
class AccountEntryData(BaseEntryData):
    """AccountEntryData

    account_username:\n      save: True, encrypt: False
    
    account_password:\n      save: True, encrypt: True
    
    account_website:\n      save: True, encrypt: False
    
    entry_type:\n       save: True, encrypt: False
    
    entry_uuid:\n       save: True, encrypt: False
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
    
    entry_type: EntryDataType = dataclasses.field(
        metadata={"save": True, "encrypt": False},
        default=EntryDataType.ACCOUNT
    )
    
    
@dataclasses.dataclass
class FileEntryData(BaseEntryData):
    """FileEntryData

    file_name:\n        save: True, encrypt: False
    
    file_data:\n        save: True, encrypt: True
    
    entry_type:\n       save: True, encrypt: False
    
    entry_uuid:\n       save: True, encrypt: False
    """
    file_name: str = dataclasses.field(
        metadata={"save": True, "encrypt": False},
        default=""
    )
    
    file_data: bytes = dataclasses.field(
        metadata={"save": True, "encrypt": True},
        default=b""
    )
    
    entry_type: EntryDataType = dataclasses.field(
        metadata={"save": True, "encrypt": False},
        default=EntryDataType.FILE
    )


@dataclasses.dataclass
class NoteEntryData(BaseEntryData):
    """NoteEntryData

    note_name:\n        save: True, encrypt: False
    
    note_content:\n        save: True, encrypt: True
    
    entry_type:\n       save: True, encrypt: False
    
    entry_uuid:\n       save: True, encrypt: False
    """
    note_name: str = dataclasses.field(
        metadata={"save": True, "encrypt": False},
        default=""
    )
    
    note_content: str = dataclasses.field(
        metadata={"save": True, "encrypt": True},
        default=""
    )
    
    entry_type: EntryDataType = dataclasses.field(
        metadata={"save": True, "encrypt": False},
        default=EntryDataType.NOTE
    )


@dataclasses.dataclass
class EncryptedEntryData(BaseEntryData):
    """FileEntryData

    encrypted_type:\n       save: True, encrypt: False

    encryption_nonce:\n        save: True, encrypt: False
    
    encrypted_data:\n        save: True, encrypt: False
    
    decrypted_data:\n        save: True, encrypt: False
    
    entry_type:\n       save: True, encrypt: False
    
    entry_uuid:\n       save: True, encrypt: False
    """
    encrypted_type: EntryDataType = dataclasses.field(
        metadata={"save": True, "encrypt": False},
        default=EntryDataType.NONE
    )
    
    encryption_nonce: bytes = dataclasses.field(
        metadata={"save": True, "encrypt": False},
        default=""
    )
    
    encrypted_data: bytes = dataclasses.field(
        metadata={"save": True, "encrypt": False},
        default=b""
    )
    
    decrypted_data: dict = dataclasses.field(
        metadata={"save": True, "encrypt": False},
        default_factory=dict
    )
    
    entry_type: EntryDataType = dataclasses.field(
        metadata={"save": True, "encrypt": False},
        default=EntryDataType.ENCRYPTED
    )


def get_entry_data_class_by_type(
    type: EntryDataType
) -> BaseEntryData | EncryptedEntryData | AccountEntryData | FileEntryData | NoteEntryData:
    if type is EntryDataType.ENCRYPTED:
        return EncryptedEntryData
    
    if type is EntryDataType.ACCOUNT:
        return AccountEntryData
    
    if type is EntryDataType.FILE:
        return FileEntryData
    
    if type is EntryDataType.NOTE:
        return NoteEntryData
    
    if type is EntryDataType.NONE:
        return BaseEntryData