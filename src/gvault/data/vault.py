from gvault.data import item


class VaultData:
    def __init__(
        self,
        vault_key: bytes | None = None,
    ):
        self.private_items: list[item.PrivateItem] = []
        self.public_items: list[item.PublicItem] = []

        self.vault_key = vault_key
    
    
    def get_all_items_by_name(
        self, item_name: str
    ) -> list[item.PrivateItem | item.PublicItem]:
        private_result = self.get_private_items_by_name(item_name)
        public_result = self.get_public_items_by_name(item_name)
        
        return private_result + public_result
    
    
    def get_private_items_by_name(
        self, item_name: str
    ) -> list[item.PrivateItem]:
        
        return [item.item_name == item_name 
                and item for item in self.private_items]
    
    
    def get_public_items_by_name(
        self, item_name: str
    ) -> list[item.PublicItem]:
        
        return [item.item_name == item_name 
                and item for item in self.public_items] 
    
    
    def create_private_item(
        self, item_name: str, item_note: str, item_data: item.EncryptedItemData
                                                        | item.AccountItemData
                                                        | item.MessageItemData
                                                        | item.FileItemData,
        encrypt_on_create: bool | None = False,
        decrypt_on_create: bool | None = False,
        key: bytes | None = None
    ) -> item.PrivateItem:
        new_private_item = item.PrivateItem(
            item_name=item_name,
            item_note=item_note,
            item_data=item_data,
            encrypt_on_create=encrypt_on_create,
            decrypt_on_create=decrypt_on_create,
            key=key or self.vault_key
        )
        
        self.private_items.append(new_private_item)
        
        return new_private_item
    
    
    def create_public_item(
        self, item_name: str, item_note: str, item_data: item.AccountItemData
                                                        | item.MessageItemData
                                                        | item.FileItemData
    ) -> item.PublicItem:
        new_public_account = item.PublicItem(
            item_name=item_name,
            item_note=item_note,
            item_data=item_data
        )
        
        self.public_items.append(new_public_account)
        
        return new_public_account
    