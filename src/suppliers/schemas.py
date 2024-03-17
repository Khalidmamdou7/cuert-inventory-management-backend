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


class SuppliersDB():
    def __init__(self):
        self.db = Database()
        self.collection = self.db.get_collection('suppliers')

    def add_supplier(self, supplier: SupplierCreateRequest):
        """
        Add a new supplier to the database.

        Args:
            supplier (SupplierCreateRequest): the supplier to be added

        Returns:
            SupplierInDB: the supplier that was added
        
        Raises:
            HTTPException: if the supplier already exists, or data validation fails
        """
        try:
            supplier_in_db = supplier.model_dump()
            supplier_in_db["created_at"] = datetime.now().isoformat()
            supplier_in_db["updated_at"] = datetime.now().isoformat()
            supplier_in_db["_id"] = self.collection.insert_one(supplier_in_db).inserted_id
            return SupplierInDB(**db_to_dict(supplier_in_db))
        except DuplicateKeyError as e:
            duplicate_key = list(e.details['keyPattern'].keys())[0]
            raise HTTPException(status_code=400, detail="Supplier already exists with the same " + duplicate_key)
        
    def get_suppliers(self):
        """
        Get all suppliers from the database.

        Returns:
            list[SupplierInDB]: the suppliers that were retrieved
        
        """
        suppliers = list(self.collection.find())
        return [SupplierInDB(**db_to_dict(supplier)) for supplier in suppliers]
    
    def get_supplier(self, supplier_id: str) -> SupplierInDB:
        """
        Get a supplier from the database.

        Args:
            supplier_id (str): the id of the supplier to be retrieved

        Returns:
            SupplierInDB: the supplier that was retrieved
        
        """
        supplier = self.collection.find_one({"_id": ObjectId(supplier_id)})
        if supplier:
            return SupplierInDB(**db_to_dict(supplier))
        else:
            raise HTTPException(status_code=404, detail="Supplier not found")
        
    def update_supplier(self, supplier_id: str, supplier: SupplierUpdateRequest) -> SupplierInDB:
        """
        Update a supplier in the database.

        Args:
            supplier_id (str): the id of the supplier to be updated
            supplier (SupplierUpdateRequest): the updated supplier

        Returns:
            SupplierInDB: the supplier that was updated
        
        """
        supplier_in_db = supplier.model_dump()
        supplier_in_db["updated_at"] = datetime.now().isoformat()
        try:
            self.collection.update_one({"_id": ObjectId(supplier_id)}, {"$set": supplier_in_db})
        except DuplicateKeyError as e:
            duplicate_key = list(e.details['keyPattern'].keys())[0]
            raise HTTPException(status_code=400, detail="Supplier already exists with the same " + duplicate_key)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not update supplier")

        return self.get_supplier(supplier_id)
    
    def delete_supplier(self, supplier_id: str):
        """
        Delete a supplier from the database.

        Args:
            supplier_id (str): the id of the supplier to be deleted
        
        """
        try:
            self.collection.delete_one({"_id": ObjectId(supplier_id)})
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not delete supplier")
