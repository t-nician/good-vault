import dataclasses


class DataToDictHandler:
    def to_dict(
        self, 
        bytes_to_hex: bool | None = False, 
    ) -> dict:
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
    
    
    def to_encrypt_and_not_encrypt_dicts(
        self, 
        bytes_to_hex: bool | None = False
    ) -> tuple[dict, dict]:
        __self_dict = dataclasses.asdict(self)
        __self_fields = dataclasses.fields(self)
        
        __encrypt_dict = {}
        __not_encrypt_dict = {}
        
        for field in __self_fields:
            __field_data = __self_dict[field.name]
            
            if field.metadata["encrypt"]:
                if bytes_to_hex and type(__field_data) is bytes:
                    __encrypt_dict[field.name] = __field_data.hex()
                else:
                    __encrypt_dict[field.name] = __field_data
            else:
                if bytes_to_hex and type(__field_data) is bytes:
                    __not_encrypt_dict[field.name] = __field_data.hex()
                else:
                    __not_encrypt_dict[field.name] = __field_data
        
        return __encrypt_dict, __not_encrypt_dict