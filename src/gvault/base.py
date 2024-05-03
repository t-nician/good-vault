import json
import dataclasses


class ToDictToJSON:
    def to_dict(self, bytes_to_hex: bool | None = False) -> dict:
        processed_dict = {}
        unprocessed_dict = dataclasses.asdict(self)
        
        for field in dataclasses.fields(self):
            if field.metadata["save"]:
                data = unprocessed_dict[field.name]
                if type(data) is bytes and bytes_to_hex:
                    processed_dict[field.name] = data.hex()
                else:
                    processed_dict[field.name] = data
        
        return processed_dict

    
    def to_json(self, bytes_to_hex: bool | None = False) -> str:
        return json.dumps(self.to_dict(bytes_to_hex))


@dataclasses.dataclass
class StatusResult(ToDictToJSON):
    success: bool = dataclasses.field(
        metadata={"save": True, "encrypt": False},
        default=False
    )
    
    message: str = dataclasses.field(
        metadata={"save": True, "encrypt": False},
        default=""
    )
    
    data: any = dataclasses.field(
        metadata={"save": True, "encrypt": False},
        default=""
    )

    __locked: bool = False
    
    def complete(self, message: str, data: any):
        if self.__locked:
            return None
        
        self.success = True
        self.message = message
        self.data = data
        
        self.__locked = True

    
    def failure(self, message: str, data: any):
        if self.__locked:
            return None
        
        self.success = False
        self.message = message
        self.data = data
        
        self.__locked = True
    
    
    def unpack(self) -> tuple[bool, str, any]:
        return self.success, self.message, self.data
    
    