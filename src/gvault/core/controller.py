from gvault.core import entry, tool


class VaultController:
    def __init__(self):
        self.vault_entries: list[entry.BaseEntry] = []

    def add_entry(self, entry_data: entry.BaseEntry):
        self.vault_entries.append(entry_data)

    def model_dump(
        self, 
        encrypt_entries: bool | None = False
    ) -> list[entry.BaseEntry]:
        if encrypt_entries:
            for entry in self.vault_entries:
                pass
            
        return [entry.model_dump() for entry in self.vault_entries]