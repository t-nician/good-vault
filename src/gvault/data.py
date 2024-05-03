import json
import uuid
import dataclasses


from gvault import base


@dataclasses.dataclass
class BaseItemData(base.BaseFunctions):
    uuid: str = base.data_field(
        save=True, encrypt=False, default_factory=lambda: uuid.uuid4().hex
    )


@dataclasses.dataclass
class AccountItemData(BaseItemData):
    username: str = base.data_field(save=True, encrypt=False, default="")
    password: str = base.data_field(save=True, encrypt=True, default="")
    website: str = base.data_field(save=True, encrypt=False, default="")


@dataclasses.dataclass
class NoteItemData(BaseItemData):
    name: str = base.data_field(save=True, encrypt=False, default="")
    content: str = base.data_field(save=True, encrypt=True, default="")


@dataclasses.dataclass
class VaultItem(base.BaseFunctions):
    name: str = base.data_field(save=True, encrypt=False, default="")
    note: str = base.data_field(save=True, encrypt=False, default="")
    
    item_data: BaseItemData = base.data_field(
        save=True, encrypt=False, default_factory=BaseItemData
    )
    

@dataclasses.dataclass
class VaultData(base.BaseFunctions):
    vault_items: list[VaultItem] = base.data_field(
        save=True, encrypt=False, default_factory=list
    )
    
    