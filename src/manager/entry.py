class EntryObject:
    def __init__(
        self, 
        name: str, 
        type: str, 
        data: str | bytes, 
        note: str | None = None,
        nonce: str | bytes | dict | None = None
    ):  
        self.name = name
        self.type = type

        self.data = type(data) is str and bytes.fromhex(data) or data
        self.nonce = type(nonce) is str and bytes.fromhex(nonce) or nonce
        
        self.note = note
    
    
    