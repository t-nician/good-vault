from object import hash


class PublicEntryObject:
    def __init__(self, name: str, type: str, note: str, data: str | dict | list):
        self.name = name
        self.type = type
        self.note = note
        self.data = data



class PrivateEntryObject:
    def __init__(self, name: str, entry_type: str, note: str, data: dict | list | str, hash: hash.HashObject):
        self.name = name
        self.type = entry_type
        self.note = note
        
        self.hash = hash
        
        self.data = type(data) is str and bytes.fromhex(data) or data