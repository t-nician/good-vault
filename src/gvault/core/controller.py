from gvault.core import entry, tool


class VaultController:
    def __init__(self):
        self.vault_entries: list[entry.BaseEntry] = []

    def add_entry(self, entry_data: entry.BaseEntry):
        self.vault_entries.append(entry_data)