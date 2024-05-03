import json
import uuid
import dataclasses


from Crypto.Cipher import AES


@dataclasses.dataclass
class EntryProperties:
    for_encryption: dict[str, bool] = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class AnyEntry:
    properties: EntryProperties = dataclasses.field(
        default_factory=EntryProperties
    )
    
    uuid: str = dataclasses.field(default_factory=lambda: uuid.uuid4().hex)
    

@dataclasses.dataclass
class AccountEntry(AnyEntry):
    properties: EntryProperties = dataclasses.field(
        default_factory=lambda: EntryProperties(
            for_encryption={
                "username": False,
                "password": True,
                "website": False
            }
        )
    )
    
    username: str = dataclasses.field(default="")
    password: str = dataclasses.field(default="")
    website: str = dataclasses.field(default="")


@dataclasses.dataclass
class NoteEntry(AnyEntry):
    properties: EntryProperties = dataclasses.field(
        default_factory=lambda: EntryProperties(
            for_encryption={
                "name": False,
                "content": True
            }
        )
    )
    
    name: str = dataclasses.field(default="")
    content: str = dataclasses.field(default="")


@dataclasses.dataclass
class EncryptedEntry(AnyEntry):
    properties: EntryProperties = dataclasses.field(
        default_factory=lambda: EntryProperties(
            for_encryption={
                "decrypted_fields": False,
                "encrypted_fields": False
            }
        )
    )
    
    decrypted_fields: dict[str, any] = dataclasses.field(default_factory=dict)
    encrypted_fields: dict[str, any] = dataclasses.field(default_factory=dict)
    

@dataclasses.dataclass
class VaultEntry:
    entry_data: EncryptedEntry | AccountEntry | NoteEntry | AnyEntry = dataclasses.field(
        default_factory=AnyEntry
    )
    
    def encrypt(self, key: bytes):
        if type(self.entry_data) is EncryptedEntry:
            raise Exception("Cannot encrypt an already encrypted entry!")

        for_encryption_dict = self.entry_data.properties.for_encryption

        decrypted_fields = {}
        encrypted_fields = {}
        
        for (field_name, encrypt_field) in for_encryption_dict.items():
            attribute = getattr(self.entry_data, field_name, None)

            if attribute is not None:
                if encrypt_field:
                    _attribute = attribute
                    
                    if type(attribute) is str:
                        _attribute = attribute.encode()
                    elif type(attribute) is not bytes:
                        _attribute = json.dumps(attribute).encode()
                    
                    cipher = AES.new(key=key, mode=AES.MODE_EAX)
                    
                    encrypted_fields[field_name] = {
                        "nonce": cipher.nonce,
                        "data": cipher.encrypt(_attribute)
                    }
                else:
                    decrypted_fields[field_name] = attribute
        
        encrypted_entry = EncryptedEntry(
            decrypted_fields=decrypted_fields,
            encrypted_fields=encrypted_fields
        )
        
        self.entry_data = encrypted_entry
        
        return encrypted_entry