import enum
import json

import dataclasses


class EntryDataType(enum.StrEnum):
    """Available EntryData types.
    """
    ENCRYPTED = "encrypted"
    ACCOUNT = "account"
    NOTE = "note"
    NONE = "none"


@dataclasses.dataclass
class BaseEntryData:
    """
        Core data for all EntryData.
    """
    entry_type: EntryDataType = dataclasses.field(
        metadata={"save": True, "encrypt": False},
        default=EntryDataType.NONE
    )


    def to_dict(self, bytes_to_hex: bool | None = False) -> dict:
        __self_dict = dataclasses.asdict(self)
        __self_fields = dataclasses.fields(self)
        
        __processed_dict = {}
        
        for field in __self_fields:
            __field_data = __self_dict[field.name]
            
            if field.metadata["save"]:
                if bytes_to_hex and type(__field_data) is bytes:
                    __processed_dict[field.name] = __field_data.hex()
                else:
                    __processed_dict[field.name] = __field_data
        
        return __processed_dict


@dataclasses.dataclass
class AccountEntryData(BaseEntryData):
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
    pass