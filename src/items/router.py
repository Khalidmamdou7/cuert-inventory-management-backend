# router.py
# Defining the API endpoints go here and calling the service layer


from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from ..models import ResponseModel
from ..auth.dependencies import authenticate_user_jwt, get_current_user
from ..auth.models import RoleEnum, User

from . import service as items_service
from .models import *


router = APIRouter()

@router.post("/", response_model=ResponseModel[Item], status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreateRequest, current_user: User = Depends(get_current_user)):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only admins can create items")
    
    item = items_service.create_item(item)
    return {
        "status": "success",
        "message": "item created successfully",
        "data": item
    }

@router.get("/", response_model=ResponseModel[list[Item]])
def get_items(current_user: User = Depends(get_current_user)):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only admins can get items")
    items = items_service.get_items()
    return {
        "status": "success",
        "message": "items retrieved successfully",
        "data": items
    }

@router.get("/{item_id}", response_model=ResponseModel[Item])
def get_item(item_id: str, current_user: User = Depends(get_current_user) ):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only admins can get items")
    item = items_service.get_item(item_id)
    return {
        "status": "success",
        "message": "item retrieved successfully",
        "data": item
    }

@router.put("/{item_id}", response_model=ResponseModel[Item])
def update_item(item_id: str, item: ItemCreateRequest, current_user: User = Depends(get_current_user)):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only admins can update items")
    item = items_service.update_item(item_id, item)
    return {
        "status": "success",
        "message": "item updated successfully",
        "data": item
    }

@router.delete("/{item_id}", response_model=ResponseModel[None], status_code=status.HTTP_200_OK)
def delete_item(item_id: str, current_user: User = Depends(get_current_user)):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only admins can delete items")
    items_service.delete_item(item_id)
    return {
        "status": "success",
        "message": "item deleted successfully",
        "data": None
    }
