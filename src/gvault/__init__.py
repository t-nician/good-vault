from dataclasses import dataclass, field

from gvault import data, util


@dataclass
class VaultManager:
    data_entries: list = field(default_factory=list)

    def add_data_entry_from_dict(self, entry: dict):
        if entry.get("type") is None:
            return None

        result_cls = util.vault_data_class_dictionary[entry["type"]]

        if result_cls:
            prepped_vault_fields: dict[str, util.VaultField] = {}
            field_names = dir(result_cls.cls)

            for field_name in field_names:
                if field_name != "type" and entry.get(field_name) is not None:
                    prepped_vault_fields[field_name] = util.VaultField(
                        **entry[field_name]
                    )

            self.data_entries.append(
                result_cls(**prepped_vault_fields)
            )


    def load_data_entries_from_list(self, data_list: list):
        pass


    def load_data_entries_from_json(self, data_json: str):
        pass
    