import json
import gvault

vault_data = gvault.data.VaultData()

status_result = gvault.base.StatusResult()
status_result.complete("Hello", "World!")

vault_data.decrypted.append(status_result)

print(vault_data.to_dict(True))
print(dir(vault_data))

print("test" in ["hello", "test"])