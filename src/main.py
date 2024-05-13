import json
import pydantic

from gvault.core import controller, entry, tool


vault = controller.VaultController()


account_entry = entry.AccountEntry()

account_entry.website.value = "website"
account_entry.username.value = "username"
account_entry.password.value = "password"


vault.add_entry(account_entry)

print(vault.model_dump())