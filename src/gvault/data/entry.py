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
    
    entry_values_to_save: list[str]
    entry_values_to_encrypt: list[str]
    
    def to_dict(
        self, 
        bytes_to_hex: bool | None = False
    ) -> dict:
        __dataclass_dict = dataclasses.asdict(self)
        __processed_dict = {}
        
        for value_name in self.entry_values_to_save:
            __data_value: bytes | any = __dataclass_dict[value_name]
            __data_type: type[bytes] | any = type(__data_value)
            
            if bytes_to_hex and __data_type is bytes:
                __processed_dict[value_name] = __data_value.hex()
            else:
                __processed_dict[value_name] = __data_value
        
        return __processed_dict


@dataclasses.dataclass
class AccountEntryData(BaseEntryData):
    account_username: str = ""
    account_password: str = ""
    account_website: str = ""
    
    entry_type: EntryDataType = EntryDataType.ACCOUNT
    
    entry_values_to_save: list[str] = dataclasses.field(
        default_factory=lambda: [
            "account_username", "account_password", "account_website"
        ]
    )
    
    entry_values_to_encrypt: list[str] = dataclasses.field(
        default_factory=lambda: [ "account_password" ]
    )


@dataclasses.dataclass
class NoteEntryData(BaseEntryData):
    note_title: str = ""
    note_content: str = ""
    
    entry_type: EntryDataType = EntryDataType.NOTE
    
    entry_values_to_save: list[str] = dataclasses.field(
        default_factory=lambda: [ "note_title", "note_content" ]
    )
    
    entry_values_to_encrypt: list[str] = dataclasses.field(
        default_factory=lambda: [ "note_content" ]
    )


@dataclasses.dataclass
class EncryptedEntryData(BaseEntryData):
    cipher_nonce: bytes = b""
    encrypted_data: bytes = b""
    
    entry_type: EntryDataType = EntryDataType.ENCRYPTED
    
    entry_values_to_save: list[str] = dataclasses.field(
        default_factory=lambda: [ "cipher_nonce", "encrypted_data" ]
    )
    
    entry_values_to_encrypt: list[str] = dataclasses.field(
        default_factory=lambda: [ ]
    )