from gvault.core import instance


vault_instance = instance.VaultInstance(
    key=b"password12345678",
    vault_data="[]"
)

entry_instance = vault_instance.create_entry(

)

website_item = entry_instance.create_item(

)

username_item = entry_instance.create_item(

)

password_item = entry_instance.create_item(

)


