import json
import uuid


from dataclasses import dataclass, field, asdict, is_dataclass


vault_data_class_dictionary = {}


@dataclass
class VaultField:
    save: bool = field(default=False)
    encrypt: bool = field(default=False)

    data: str | bytes = field(default="")
    nonce: str | bytes = field(default="")

    is_encrypted: bool = field(default=False)

    def __post_init__(self):
        if self.nonce != "":
            self.is_encrypted = True


def vault_data(obj: object):
    class Wrapper:
        cls = obj
        def __init__(self, **kwargs):
            self.wrap = obj()
            self.uuid = uuid.uuid4().hex
            for (key, value) in kwargs.items():
                setattr(self.wrap, key, value)

    vault_data_class_dictionary[obj.type] = Wrapper
    return Wrapper