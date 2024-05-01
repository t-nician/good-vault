import gvault, json

from Crypto.Cipher import AES

vault_data = gvault.data.vault.VaultData()

vault_data.assign_vault_key(b"password12345678")


vault_entry = gvault.data.vault.VaultEntryData(
    entry_data=gvault.data.entry.AccountEntryData(
        account_username="Username",
        account_password="Password",
        account_website="Wesbite.com"
    )
)


