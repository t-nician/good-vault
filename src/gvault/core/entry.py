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
    uuid: EntryField = EntryField(save=False, encrypt=False)
    type: EntryField = EntryField(save=True, encrypt=False)

    def model_post_init(self, *args, **kwargs):
        self.type.value = type(self).__name__
        
        if self.uuid.value == "":
            self.uuid.value = uuid4().hex
    

    def model_dump(self) -> dict:
        target_fields = [
            getattr(self, field)
                and getattr(self, field).save is True
                and field 
                or None 
            for field in self.model_fields
        ]

        for _ in range(0, target_fields.count(None)):
            target_fields.remove(None)

        entry_fields = []

        for field in self.model_fields:
            entry_field = getattr(self, field)

            if field is not None and entry_field.save:
                entry_fields.append(entry_field)

        return dict(zip(target_fields, entry_fields))


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
