import json
import dataclasses

import gvault

vault_item = gvault.data.VaultItem(
    name="name",
    note="note",
    item_data=gvault.data.AccountItemData(
        username="username",
        password="password",
        website="website"
    )
)


vault_item.encrypt_item(b"password12345678")