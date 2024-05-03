import gvault

vault_item = gvault.data.VaultEntry(
    entry_data=gvault.data.AccountEntry(
        username="Username",
        password="Password",
        website="Website.com"
    )
)

vault_item.encrypt(b"password12345678")

print(vault_item.entry_data)