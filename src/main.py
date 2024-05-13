from gvault.core import controller, default, tool


vault = controller.VaultController()
account_entry = default.AccountEntry()

print(account_entry.username)