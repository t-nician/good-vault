from uuid import uuid4
from dataclasses import field, fields, dataclass

available_data_classes: dict[str, object] = {}

def add_dataclass_to_vault(cls: object, type_name: str):
    available_data_classes[type_name] = cls


@dataclass
class DataField:
    value: str | bytes = field(default="")
    nonce: str | bytes = field(default="")

    save: bool = field(default=False)
    encrypt: bool = field(default=False)


@dataclass
class BaseData:
    uuid: DataField = field(
        default_factory=lambda: DataField(
            value=uuid4().hex,

            save=True,
            encrypt=False
        )
    )


@dataclass
class AccountData(BaseData):
    website: DataField = field(
        default_factory=lambda: DataField(save=True, encrypt=False)
    )
    
    username: DataField = field(
        default_factory=lambda: DataField(save=True, encrypt=False)
    )

    password: DataField = field(
        default_factory=lambda: DataField(save=True, encrypt=True)
    )
add_dataclass_to_vault(AccountData, "account")


@dataclass
class NoteData(BaseData):
    title: DataField = field(
        default_factory=lambda: DataField(save=True, encrypt=False)
    )

    content: DataField = field(
        default_factory=lambda: DataField(save=True, encrypt=True)
    )
add_dataclass_to_vault(NoteData, "note")


@dataclass
class VaultData(BaseData):
    vault_data: list[AccountData | NoteData] = field(default_factory=list)


    def add_vault_data_from_dict(self, data: dict):
        type_name = data.get("type")
        class_object = available_data_classes.get(type_name)
        
        if type_name and class_object:
            keys = [field.name for field in fields(class_object)]
            self.vault_data.append(
                    class_object(**dict(zip(
                        keys,
                        [DataField(**data.get(key) or {}) for key in keys]
                    ))
                )
            )