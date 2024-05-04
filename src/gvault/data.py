import json
import uuid
import dataclasses


from Crypto.Cipher import AES


@dataclasses.dataclass
class FieldData:
    uuid: str = dataclasses.field(default_factory=lambda: uuid.uuid4().hex)
    
    name: str = dataclasses.field(default="")
    note: str = dataclasses.field(default="")

    nonce: bytes = dataclasses.field(default=b"")    
    data: str | bytes = dataclasses.field(default="")

    encrypted: bool = dataclasses.field(default=False)
    do_i_encrypt: bool = dataclasses.field(default=False)
    
    def __post_init__(self):
        if self.nonce != b"":
            if type(self.data) is bytes:
                self.encrypted = True
            else:
                raise Exception("FieldData has nonce but data is not bytes?")


@dataclasses.dataclass
class ItemData:
    name: str = dataclasses.field(default="")
    note: str = dataclasses.field(default="")
    
    fields: list[FieldData] = dataclasses.field(default_factory=list)
    private_field_uuids: list[str] = dataclasses.field(default_factory=list)

    def add_field(
        self, name: str, note: str, data: str | bytes, 
        do_i_encrypt: bool | None = False,
        key: bytes | None = None,
    ) -> FieldData:
        if do_i_encrypt and key:
            cipher = AES.new(key=key, mode=AES.MODE_EAX)
            
            new_field = FieldData(
                name=name,
                note=note,
                data=cipher.encrypt(
                    type(data) is str and data.encode() or data
                ),
                nonce=cipher.nonce,
                do_i_encrypt=do_i_encrypt
            )
            
            self.private_field_uuids.append(new_field.uuid)
            self.fields.append(new_field)
            
            return new_field

        else:
            new_field = FieldData(
                name=name,
                note=note,
                data=data
            )
            
            self.fields.append(new_field)
            
            return new_field