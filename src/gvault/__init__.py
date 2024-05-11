from dataclasses import dataclass, field

from gvault import data, util


@dataclass
class VaultManager:
    data_entries: list = field(default_factory=list)

    def load_data_entries_from_list(self, data_list: list):
        pass


    def load_data_entries_from_json(self, data_json: str):
        pass
    