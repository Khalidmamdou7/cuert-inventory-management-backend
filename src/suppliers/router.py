# router.py
# Defining the API endpoints go here and calling the service layer


from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from ..models import ResponseModel

from . import service as suppliers_service

from ..auth.dependencies import authenticate_user_jwt, get_current_user

from .models import *

router = APIRouter()


@router.post("/", response_model=ResponseModel[SupplierResponse], status_code=status.HTTP_201_CREATED)
def create_supplier(supplier: SupplierCreateRequest, current_user: User = Depends(get_current_user)):
    supplier = suppliers_service.create_supplier(supplier)
    return {
        "status": "success",
        "message": "Supplier created successfully",
        "data": supplier
    }

@router.get("/", 
            response_model=ResponseModel[list[SupplierResponse]], 
            description="Get all suppliers",
            status_code=status.HTTP_200_OK)
def get_suppliers(current_user: User = Depends(get_current_user)):
    suppliers = suppliers_service.get_suppliers()
    return {
        "status": "success",
        "message": "Suppliers retrieved successfully",
        "data": suppliers
    }

@router.get("/{supplier_id}", response_model=ResponseModel[SupplierResponse])
def get_supplier(supplier_id: str, current_user: User = Depends(get_current_user)):
    supplier = suppliers_service.get_supplier_by_id(supplier_id)
    return {
        "status": "success",
        "message": "Supplier retrieved successfully",
        "data": supplier
    }

@router.put("/{supplier_id}", response_model=ResponseModel[SupplierResponse])
def update_supplier(supplier_id: str, supplier: SupplierUpdateRequest, current_user: User = Depends(get_current_user)):
    supplier = suppliers_service.update_supplier(supplier_id, supplier)
    return {
        "status": "success",
        "message": "Supplier updated successfully",
        "data": supplier
    }

@router.delete("/{supplier_id}", response_model=ResponseModel[None])
def delete_supplier(supplier_id: str, current_user: User = Depends(get_current_user)):
    suppliers_service.delete_supplier(supplier_id)
    return {
        "status": "success",
        "message": "Supplier deleted successfully",
        "data": None
    }


