import json
import dataclasses


def base_field(
    save: bool, encrypt: bool, 
    default: any = None, 
    default_factory: any = None
) -> dataclasses.Field:
    metadata = {"save": save, "encrypt": encrypt}
    
    if default is not None:
        return dataclasses.field(
            metadata=metadata,
            default=default
        )
    else:
        return dataclasses.field(
            metadata=metadata,
            default_factory=default_factory
        )


class ToDictToJSON:
    def __str__(self) -> str:
        return self.to_json(True)
    
    
    def to_dict(self, bytes_to_hex: bool | None = False) -> dict:
        processed_dict = {}
        unprocessed_dict = dataclasses.asdict(self)
        
        for field in dataclasses.fields(self):
            if field.metadata["save"]:
                data = unprocessed_dict[field.name]
                if type(data) is bytes and bytes_to_hex:
                    processed_dict[field.name] = data.hex()
                elif "to_dict" in dir(data):
                    print("get_attr")
                    processed_dict[field.name] = data.to_dict(bytes_to_hex)
                elif type(data) is list:
                    processed_dict[field.name] = []
                    for item in data:
                        if type(item) is ToDictToJSON:
                            print("dict")
                            processed_dict[field.name].append(
                                item.to_dict(bytes_to_hex)
                            )
                        else:
                            processed_dict[field.name].append(
                                item
                            )
                    
                else:
                    processed_dict[field.name] = data
                    
        
        return processed_dict

    
    def to_json(self, bytes_to_hex: bool | None = False) -> str:
        return json.dumps(self.to_dict(bytes_to_hex))
    


@dataclasses.dataclass
class StatusResult(ToDictToJSON):
    __locked: bool = base_field(save=True, encrypt=False, default=False)
    
    success: bool = base_field(save=False, encrypt=False, default=False)
    message: str = base_field(save=True, encrypt=False, default="")
    
    data: any = base_field(save=True, encrypt=False, default="")
    
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
    
    
    def is_locked(self) -> bool:
        return self.__locked
    
    