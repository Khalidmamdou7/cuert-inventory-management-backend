# item_requests_service.py

from typing import List, Optional

from fastapi import HTTPException
from fastapi import status
from fastapi.param_functions import Depends
from fastapi.responses import JSONResponse

from .models import ItemRequestCreateRequest, ItemRequestInDB, ItemRequestResponse, ItemRequestUpdateRequest, ItemRequestStatusEnum
from ..auth.models import UserResponse, User

# Dummy data for testing
item_requests_data = [
    # ... populate with dummy data as needed
]

def create_item_request(item_data: ItemRequestCreateRequest, current_user: User) -> ItemRequestResponse:
    # TODO: Add your logic to insert a new item request into MongoDB
    new_item_request = ItemRequestInDB(**item_data.dict(), _id="new_dummy_id")
    print(new_item_request)
    item_requests_data.append(new_item_request.dict())
    return ItemRequestResponse(**new_item_request.model_dump())

def get_user_item_requests(user_id: str) -> list[ItemRequestResponse]:
    # TODO: Implement the function
    items_requests = [ItemRequestResponse(**request) for request in item_requests_data if request["request_by_id"] == user_id]
    return items_requests


def get_all_item_requests(
        current_user: User,
        item_id: Optional[str] = None,
        filtered_status: Optional[ItemRequestStatusEnum] = None,
        filtered_team_id: Optional[str] = None,
        filtered_requested_by_user_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> list[ItemRequestResponse]:
    # TODO: Add your logic to fetch item requests from MongoDB
    dummy_data = [
        ItemRequestResponse(**request) for request in item_requests_data
    ]
    return dummy_data

def get_item_request_by_id(request_id: str) -> ItemRequestResponse:
    # TODO: Add your logic to fetch a specific item request from MongoDB by ID
    dummy_data = next((request for request in item_requests_data if request["id"] == request_id), None)
    if dummy_data:
        return ItemRequestResponse(**dummy_data)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item request not found",
        )

def update_item_request(request_id: str, item_data: ItemRequestUpdateRequest, current_user: User) -> ItemRequestResponse:
    # TODO: Add your logic to update a specific item request in MongoDB
    dummy_data = next((request for request in item_requests_data if request["id"] == request_id), None)
    if dummy_data:
        dummy_data.update(item_data.dict())
        return ItemRequestResponse(**dummy_data)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item request not found",
        )

def delete_item_request(request_id: str, current_user: User) -> None:
    # TODO: Add your logic to delete a specific item request from MongoDB
    global item_requests_data
    # if the request is not found, raise an HTTPException
    if not any(request["id"] == request_id for request in item_requests_data):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item request not found",
        )
    item_requests_data = [request for request in item_requests_data if request["id"] != request_id]


def update_item_request_status(request_id: str, new_status: ItemRequestStatusEnum) -> ItemRequestResponse:
    """
    Update the status of an item request.
    Dummy implementation with TODO comment.
    """
    # TODO: Add your logic to update the status of a specific item request in MongoDB
    dummy_data = next((request for request in item_requests_data if request["id"] == request_id), None)
    if dummy_data:
        dummy_data["status"] = new_status
        return ItemRequestResponse(**dummy_data)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item request not found",
        )

