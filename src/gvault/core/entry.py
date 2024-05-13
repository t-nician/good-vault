from gvault.core import tool

from uuid import uuid4
from pydantic import BaseModel, Field


class EntryField(BaseModel):
    value: str | bytes = Field("")
    nonce: str | bytes = Field("")

    save: bool = Field(False)
    encrypt: bool = Field(False)

    def is_encrypted(self) -> bool:
        return self.nonce != ""
    

class BaseEntry(BaseModel):
    uuid: EntryField = EntryField(save=True, encrypt=False)
    type: EntryField = EntryField(save=True, encrypt=False)

    def model_post_init(self, *args, **kwargs):
        self.type.value = type(self).__name__
        
        if self.uuid.value == "":
            self.uuid.value = uuid4().hex


class AccountEntry(BaseEntry):
    website: EntryField = EntryField(save=True, encrypt=False)
    username: EntryField = EntryField(save=True, encrypt=False)
    password: EntryField = EntryField(save=True, encrypt=True)
tool.add_entry_class(AccountEntry)


class FileEntry(BaseEntry):
    name: EntryField = EntryField(save=True, encrypt=False)
    data: EntryField = EntryField(save=True, encrypt=True)
tool.add_entry_class(FileEntry)


class NoteEntry(BaseEntry):
    title: EntryField = EntryField(save=True, encrypt=False)
    content: EntryField = EntryField(save=True, encrypt=True)
tool.add_entry_class(NoteEntry)


class DataEntry(BaseEntry):
    name: EntryField = EntryField(save=True, encrypt=False)
    note: EntryField = EntryField(save=True, encrypt=False)
    data: EntryField = EntryField(save=True, encrypt=True)
tool.add_entry_class(DataEntry)
