from gvault.core import entry, tool

from Crypto.Cipher import AES


class VaultController:
    def __init__(self):
        self.vault_entries: list[entry.BaseEntry] = []


    def add_entry(self, entry_data: entry.BaseEntry):
        self.vault_entries.append(entry_data)


    def model_dump(
        self, 
        encrypt: bool | None = False,
        key: bytes | None = None
    ) -> list[entry.BaseEntry]:
        if encrypt:
            assert key, "Key required to encrypt entries!"
            
            for entry in self.vault_entries:
                target_fields = [
                    getattr(entry, field)
                    for field in entry.model_fields
                ]

                for field in target_fields:
                    if not field.encrypt:
                        continue

                    cipher = AES.new(key=key, mode=AES.MODE_EAX)
                
                    nonce = cipher.nonce
                    value = field.value

                    data = cipher.encrypt(
                        type(value) is str and value.encode() or value
                    )

                    field.nonce = nonce
                    field.value = data

        return [
            entry.model_dump() for entry in self.vault_entries
        ]