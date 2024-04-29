import gvault

from Crypto.Cipher import AES

vault_data = gvault.data.vault.VaultData()

vault_data.assign_vault_key(b"password12345678")

print(vault_data.to_dict(True))

