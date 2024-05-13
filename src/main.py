from gvault.core import controller, entry, tool


vault = controller.VaultController()
account_entry = entry.AccountEntry()

print(account_entry.password)