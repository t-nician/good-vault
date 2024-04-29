import dataclasses


class DataToDictHandler:
    def to_dict(self, bytes_to_hex: bool | None = False) -> dict:
        __self_dict = dataclasses.asdict(self)
        __self_fields = dataclasses.fields(self)
        
        __processed_dict = {}
        
        for field in __self_fields:
            __field_data = __self_dict[field.name]
            
            if field.metadata["save"]:
                if bytes_to_hex and type(__field_data) is bytes:
                    __processed_dict[field.name] = __field_data.hex()
                else:
                    __processed_dict[field.name] = __field_data
        
        return __processed_dict