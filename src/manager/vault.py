import json

from manager import entry
from Crypto.Cipher import AES

class VaultObject:
    def __init__(
        self, 
        data: bytes | str | None = None, 
        nonce: bytes | str | None = None
    ):
        self.public = {
            "entries": []
        }
        
        self.private = {
            "entries": []
        }
        
        self.private_data = data
        self.private_nonce = nonce
    
    
    def update_public_data(self, data: dict):
        self.public = data
    
    
    def retrieve_public_data(self) -> dict:
        return self.public
    
    
    def retrieve_private_data(self, key: bytes) -> dict | None:
        result = AES.new(
            key=key, 
            nonce=self.private_nonce, 
            mode=AES.MODE_EAX
        ).decrypt(self.private_data)
        
        if result:
            self.private = json.loads(result)
        
        return self.private
    
    
    def update_private_data(self, key: bytes, data: dict):
        cipher = AES.new(key=key, mode=AES.MODE_EAX)
        
        self.private_data = cipher.encrypt(json.dumps(data).encode())
        self.private_nonce = cipher.nonce