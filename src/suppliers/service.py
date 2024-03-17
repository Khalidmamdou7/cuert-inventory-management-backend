# service.py
# Module specific business logic goes here


from typing import Annotated

from .models import *
from .schemas import SuppliersDB
from ..auth.schemas import UsersDB
from ..auth.models import User, RoleEnum


def create_supplier(supplier: SupplierCreateRequest) -> SupplierInDB:
    new_supplier = SuppliersDB().add_supplier(supplier)
    return new_supplier

def get_suppliers() -> list[SupplierInDB]:
    suppliers = SuppliersDB().get_suppliers()
    return suppliers

def get_supplier_by_id(supplier_id: str) -> SupplierInDB:
    supplier = SuppliersDB().get_supplier(supplier_id)
    return supplier

def update_supplier(supplier_id: str, supplier: SupplierUpdateRequest) -> SupplierInDB:
    supplier_in_db = supplier.model_dump()
    updated_supplier = SuppliersDB().update_supplier(supplier_id, SupplierUpdateRequest(**supplier_in_db))
    return updated_supplier

def delete_supplier(supplier_id: str) -> None:
    SuppliersDB().delete_supplier(supplier_id)
    return None


