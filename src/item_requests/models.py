# models.py
# Pydantic models go here (not DB models) 

from enum import Enum as PyEnum
from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, Annotated
from datetime import datetime, timedelta
import re

from ..auth.models import RoleEnum, User, UserResponse
from ..suppliers.models import SupplierResponse




class ItemRequestStatusEnum(str, PyEnum):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'
    CANCELLED = 'Cancelled'
    

class ItemRequestCreateRequest(BaseModel):
    item_id: Annotated[str, Field(..., examples=['1234567890'])] = "1234567890"
    quantity: Annotated[int, Field(..., examples=[5])] = 5
    due_date: Annotated[str, Field(..., examples=['2022-12-31T00:00:00.000Z'])] = (datetime.now() + timedelta(days=7)).isoformat()
    reason: Annotated[str, Field(..., examples=['Need it for project X'])] = "Need it for project X"
    cost_per_item_estimated: Annotated[float, Field(..., examples=[100.0])] = 100.0

class ItemRequestInDB(ItemRequestCreateRequest):
    id: Optional[str] = Field(alias='_id', default=None)
    # item_id: Annotated[str, Field(..., examples=['1234567890'])] = "1234567890"
    request_by_id: Annotated[str, Field(..., examples=['1234567890'])] = "1234567890"
    approved_by_id: Optional[str] = None
    delivered_by_id: Optional[str] = None
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()
    delivery_date: Optional[str] = None
    # due_date: Annotated[str, Field(..., examples=['2022-12-31T00:00:00.000Z'])] = (datetime.now() + datetime.timedelta(days=7)).isoformat()
    # quantity: Annotated[int, Field(..., examples=[5])] = 5
    status: Annotated[ItemRequestStatusEnum, Field(..., examples=['pending'])] = ItemRequestStatusEnum.PENDING
    cost_per_item: Annotated[float, Field(..., examples=[100.0])] = 100.0
    # cost_per_item_estimated: Annotated[float, Field(..., examples=[100.0])] = 100.0
    # reason: Annotated[str, Field(..., examples=['Need it for project X'])] = "Need it for project X"
    supplier_id: Optional[str] = None

class ItemRequestResponse(ItemRequestCreateRequest):
    id: Optional[str]
    item_name: Annotated[str, Field(..., examples=['motor'])] = "motor"
    request_by: Optional[UserResponse] = None
    approved_by: Optional[UserResponse] = None
    delivered_by: Optional[UserResponse] = None
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()
    delivery_date: Optional[str] = None
    due_date: Annotated[str, Field(..., examples=['2022-12-31T00:00:00.000Z'])] = (datetime.now() + timedelta(days=7)).isoformat()
    quantity: Annotated[int, Field(..., examples=[5])] = 5
    status: Annotated[ItemRequestStatusEnum, Field(..., examples=['pending'])] = ItemRequestStatusEnum.PENDING
    cost_per_item: Annotated[float, Field(..., examples=[100.0])] = 100.0
    cost_per_item_estimated: Annotated[float, Field(..., examples=[100.0])] = 100.0
    reason: Annotated[str, Field(..., examples=['Need it for project X'])] = "Need it for project X"
    supplier: Optional[SupplierResponse] = None


class ItemRequestUpdateRequest(ItemRequestCreateRequest):
    status: Annotated[ItemRequestStatusEnum, Field(..., examples=['pending'])] = ItemRequestStatusEnum.PENDING
    cost_per_item: Annotated[float, Field(..., examples=[100.0])] = 100.0    
    approved_by_id: Optional[str] = None
    delivered_by_id: Optional[str] = None
    delivery_date: Optional[str] = None
    supplier_id: Optional[str] = None

# class UserItemRequestsResponse(BaseModel):
#     item_requests: list[ItemRequestResponse]
#     total: int

# class ItemRequestsResponse(BaseModel):
#     item_requests: list[ItemRequestResponse]
#     total: int
#     limit: int
#     skip: int
#     filtered_status: Optional[ItemRequestStatusEnum]
#     filtered_team_id: Optional[str]
#     filtered_requested_by_user_id: Optional[str]
#     item_id: Optional[str]