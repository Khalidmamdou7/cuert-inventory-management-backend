# service.py
# Module specific business logic goes here

from typing import Annotated



from fastapi import Depends, HTTPException, status

from .models import *
from .schemas import ItemsDB
from ..auth.schemas import UsersDB
from ..auth.models import User, RoleEnum


def create_item(item: ItemCreateRequest):
    new_item = ItemsDB().add_item(item)
    return new_item

def get_items():
    items = ItemsDB().get_items()
    return items

def get_item(item_id: str):
    item = ItemsDB().get_item(item_id)
    return item

def update_item(item_id: str, item: ItemCreateRequest):
    item_in_db = item.model_dump()
    updated_item = ItemsDB().update_item(item_id, ItemCreateRequest(**item_in_db))
    return updated_item

def delete_item(item_id: str):
    deleted_item = ItemsDB().delete_item(item_id)
    return deleted_item
