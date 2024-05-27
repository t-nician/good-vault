from gvault.core import vault


vault_instance = vault.VaultInstance(
    key=b"password12345678",
    vault_data="[]"
)

print(vault_instance)