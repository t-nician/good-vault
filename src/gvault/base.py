import json
import dataclasses


def data_field(
    save: bool,
    encrypt: bool,
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


def _to_dict(obj: object, bytes_to_hex: bool | None = False) -> dict:
    processed_dict = {}
    
    for field in dataclasses.fields(obj):
        if field.metadata["save"]:
            result_data = getattr(obj, field.name, None)
            result_type = type(result_data)
            
            if callable(getattr(result_data, "to_dict", None)):
                processed_dict[field.name] = result_data.to_dict(
                    bytes_to_hex
                )
            elif result_type is bytes and bytes_to_hex:
                processed_dict[field.name] = result_data.hex()
                
            elif result_type is list:
                processed_dict[field.name] = []
                
                for item in result_data:
                    if callable(getattr(item, "to_dict", None)):
                        processed_dict[field.name].append(
                            item.to_dict(
                                bytes_to_hex
                            )
                        )
                    else:
                        processed_dict[field.name].append(item)
                          
            else:
                processed_dict[field.name] = result_data              
    
    return processed_dict


class BaseFunctions:
    def __str__(self) -> str:
        return self.to_json(True)
    
    
    def to_dict(self, bytes_to_hex: bool | None = False) -> dict:
        processed_dict = {}
    
        for field in dataclasses.fields(self):
            if field.metadata["save"]:
                result_data = getattr(self, field.name, None)
                result_type = type(result_data)
                
                if callable(getattr(result_data, "to_dict", None)):
                    processed_dict[field.name] = result_data.to_dict(
                        bytes_to_hex
                    )
                    
                elif result_type is bytes and bytes_to_hex:
                    processed_dict[field.name] = result_data.hex()
                    
                elif result_type is list:
                    processed_dict[field.name] = []
                    
                    for item in result_data:
                        if callable(getattr(item, "to_dict", None)):
                            processed_dict[field.name].append(
                                item.to_dict(
                                    bytes_to_hex
                                )
                            )
                        else:
                            processed_dict[field.name].append(item)
                            
                else:
                    processed_dict[field.name] = result_data              
        
        return processed_dict
    
    
    def to_json(self, bytes_to_hex: bool | None = False) -> str:
        return json.dumps(self.to_dict(bytes_to_hex))