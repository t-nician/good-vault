from pydantic import BaseModel


available_entry_classes: dict[str, BaseModel] = {}


def add_entry_class(entry_class: object):
    available_entry_classes[entry_class.__name__] = entry_class
    return entry_class