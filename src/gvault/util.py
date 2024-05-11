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


def vault_data(cls: object):
    vault_data_class_dictionary[cls.type] = cls
    class Wrapper:
        def __init__(self):
            self.wrap = cls()
            self.uuid = uuid.uuid4().hex
    return Wrapper