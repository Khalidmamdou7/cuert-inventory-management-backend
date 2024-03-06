# schemas.py
# DB logic goes here


from fastapi import HTTPException, status
from .models import *
from ..database import Database
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
import bson
from datetime import datetime
from ..utils.utils import db_to_dict
from ..auth.models import UserResponse, UserInDB



class ItemsDB():
    def __init__(self):
        self.db = Database()
        self.collection = self.db.get_collection('items')
    
    def add_item(self, item: ItemCreateRequest):
        """
        Add a new item to the database.

        Args:
            item (ItemCreateRequest): the item to be added

        Returns:
            itemInDB: the item that was added
        
        Raises:
            HTTPException: if the item already exists, or data validation fails
        """
        try:
            item_in_db = item.model_dump()
            item_in_db["created_at"] = datetime.now().isoformat()
            item_in_db["updated_at"] = datetime.now().isoformat()
            item_in_db["_id"] = self.collection.insert_one(item_in_db).inserted_id
            print(item_in_db)
            return Item(**db_to_dict(item_in_db))
        except DuplicateKeyError as e:
            duplicate_key = list(e.details['keyPattern'].keys())[0]
            raise HTTPException(status_code=400, detail="item already exists with the same " + duplicate_key)
        

    
    def get_item(self, item_id: str):
        """
        Get a item from the database.

        Args:
            item_id (str): the id of the item to be retrieved

        Returns:
            the item that was retrieved
        
        """
        try:
            item = self.collection.find_one({"_id": ObjectId(item_id)})
        except bson.errors.InvalidId:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item id is invalid")
        
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")
        # if with_specifications:
        #     item["specifications"] = self._get_item_specifications(item_id)
        #     return ItemWithSpecifications(**db_to_dict(item))

        return Item(**db_to_dict(item))
    
    def get_items(self):
        """
        Get all items from the database.

        Returns:
            the items that were retrieved
        
        """
        
        items = self.collection.find()
        # if with_specifications:
        #     # TODO: optimize this
        #     items = [item for item in items]
        #     for item in items:
        #         item["specifications"] = self._get_item_specifications(item["_id"])
        #     return [ItemWithSpecifications(**db_to_dict(item)) for item in items]
        return [Item(**db_to_dict(item)) for item in items]
    
    def update_item(self, item_id: str, item: ItemCreateRequest):
        """
        Update a item in the database.

        Args:
            item_id (str): the id of the item to be updated
            item (ItemCreateRequest): the item data to be updated

        Returns:
            itemInDB: the item that was updated
        
        Raises:
            HTTPException: if the item doesn't exist, or data validation fails
        """
        item_in_db = item.model_dump()
        item_in_db["updated_at"] = datetime.now().isoformat()
        try:
            self.collection.update_one({"_id": ObjectId(item_id)}, {"$set": item_in_db})
        except DuplicateKeyError as e:
            duplicate_key = list(e.details['keyPattern'].keys())[0]
            raise HTTPException(status_code=400, detail="item already exists with the same " + duplicate_key)
        except bson.errors.InvalidId:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item id is invalid")
        return self.get_item(item_id)
    
    def delete_item(self, item_id: str):
        """
        Delete a item from the database.

        Args:
            item_id (str): the id of the item to be deleted

        Returns:
            itemInDB: the item that was deleted
        
        Raises:
            HTTPException: if the item doesn't exist
        """
        try:
            item = self.get_item(item_id)
        except bson.errors.InvalidId:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item id is invalid")
        self.collection.delete_one({"_id": ObjectId(item_id)})
        self.db.get_collection('users_items').delete_many({"item_id": ObjectId(item_id)})
        return item

    # def _get_item_specifications(self, item_id: str) -> list[UserResponse]:
    #     """
    #     Get the specifications of a item from the database.

    #     Args:
    #         item_id (str): the id of the item to get its specifications

    #     Returns:
    #         list[UserResponse]: the specifications of the item
        
    #     Raises:
    #         HTTPException: if the item doesn't exist
    #     """
    #     try:
    #         result = self.db.get_collection('users_items').find({"item_id": ObjectId(item_id)})
    #     except bson.errors.InvalidId:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item id is invalid")
    #     users_ids = [entry["user_id"] for entry in result]
    #     print(users_ids)
    #     users_db_objs = [self.db.get_collection('users').find_one({"_id": ObjectId(user_id)}) for user_id in users_ids]
    #     print(users_db_objs)
    #     return [UserResponse(**db_to_dict(user)) for user in users_db_objs]