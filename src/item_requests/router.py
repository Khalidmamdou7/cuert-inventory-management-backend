# router.py
# Defining the API endpoints go here and calling the service layer

from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from ..models import ResponseModel

# An example of importing sth from the same directory (importing the whole file as module)
from . import service as item_request_service

# An example of importing sth from the same directory (importing specific functinos from the file)
from ..auth.dependencies import authenticate_user_jwt, get_current_user

from .models import *


router = APIRouter()


@router.post("/", response_model=ResponseModel[ItemRequestResponse], status_code=status.HTTP_201_CREATED)
def create_item_request(item_request: ItemRequestCreateRequest, current_user: User = Depends(get_current_user)):
    item_request = item_request_service.create_item_request(item_request, current_user)
    return {
        "status": "success",
        "message": "Item request created successfully",
        "data": item_request
    }

@router.get("/", response_model=ResponseModel[list[ItemRequestResponse]],
            description="Get all item requests of the current user") 
def get_user_item_requests(current_user: User = Depends(get_current_user)):
    item_requests = item_request_service.get_user_item_requests(current_user)
    return {
        "status": "success",
        "message": "Item requests retrieved successfully",
        "data": item_requests
    }

@router.get("/{item_request_id}", response_model=ResponseModel[ItemRequestResponse])
def get_item_request(item_request_id: str):
    item_request = item_request_service.get_item_request_by_id(item_request_id)
    return {
        "status": "success",
        "message": "Item request retrieved successfully",
        "data": item_request
    }

@router.put("/{item_request_id}", response_model=ResponseModel[ItemRequestResponse])
def update_item_request(item_request_id: str, item_request: ItemRequestUpdateRequest, current_user: User = Depends(get_current_user)):
    item_request = item_request_service.update_item_request(item_request_id, item_request, current_user)
    return {
        "status": "success",
        "message": "Item request updated successfully",
        "data": item_request
    }

@router.delete("/{item_request_id}", response_model=ResponseModel[None])
def delete_item_request(item_request_id: str, current_user: User = Depends(get_current_user)):
    item_request_service.delete_item_request(item_request_id, current_user)
    return {
        "status": "success",
        "message": "Item request deleted successfully",
        "data": None
    }

@router.get("/all/", response_model=ResponseModel[list[ItemRequestResponse]],
            description="Get all item requests of all users")
def get_item_requests(
    current_user: User = Depends(get_current_user),
    item_id: Annotated[str, None] = None,
    filtered_status: Annotated[ItemRequestStatusEnum, None] = None,
    filtered_team_id: Annotated[str, None] = None,
    filtered_requested_by_user_id: Annotated[str, None] = None,
    skip: int = 0,
    limit: int = 10,
):
    if current_user.role == RoleEnum.TEAM_MEMBER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action"
        )
    
    print(current_user.role)
    item_requests = item_request_service.get_all_item_requests(
        current_user, item_id, filtered_status, filtered_team_id, filtered_requested_by_user_id, skip, limit
    )
    print(item_requests)
    return {
        "status": "success",
        "message": "Item requests retrieved successfully",
        "data": item_requests
    }

 