from gvault.core import tool

from uuid import uuid4
from pydantic import BaseModel, Field


class EntryField(BaseModel):
    value: str = Field("")
    nonce: str = Field("")

    save: bool = Field(False)
    encrypt: bool = Field(False)


class BaseEntry(BaseModel):
    uuid: str = EntryField(save=True, encrypt=False)
    type: str = EntryField(save=True, encrypt=False)

    def model_post_init(self, *args, **kwargs):
        self.type.value = type(self).__name__


@tool.add_entry_class
class AccountEntry(BaseEntry):
    website: str = EntryField(save=True, encrypt=False)
    username: str = EntryField(save=True, encrypt=False)
    password: str = EntryField(save=True, encrypt=True)


@tool.add_entry_class
class NoteEntry(BaseEntry):
    title: str = EntryField(save=True, encrypt=False)
    content: str = EntryField(save=True, encrypt=True)