from gvault.core import entry, tool

from pydantic import BaseModel, Field


class VaultController(BaseModel):
    vault_entries: list[entry.BaseEntry] = Field(default_factory=list)

    def add_entry(self, entry_data: entry.BaseEntry):
        self.vault_entries.append(entry_data)