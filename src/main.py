import gvault

from Crypto.Cipher import AES

vault_data = gvault.data.vault.VaultData()

print(vault_data.assign_vault_key(b"password12345678"))

recreated_vault = gvault.data.vault.VaultData(
    key_check_data=vault_data.key_check_data,
    key_check_nonce=vault_data.key_check_nonce
)

print(recreated_vault.assign_vault_key(b"password12345678"))