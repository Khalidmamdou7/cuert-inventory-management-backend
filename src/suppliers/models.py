# models.py
# Pydantic models go here (not DB models) 


from enum import Enum as PyEnum
from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, Annotated
from datetime import datetime, timedelta
import re

from ..auth.models import RoleEnum, User, UserResponse


class SupplierCreateRequest(BaseModel):
    name: Annotated[str, Field(..., examples=['Supplier X'])]
    address: Annotated[str, Field(..., examples=['123 Main St, City, State, Zip'])] = "No address was provided"
    mobile: Optional[Annotated[str, Field(..., examples=['01234567890'])]] = None
    notes: Annotated[str, Field(..., examples=['Notes about the supplier: This supplier provides high quality products but is expensive'])] = ""

class SupplierInDB(SupplierCreateRequest):
    id: Optional[str] = Field(alias='_id', default=None)
    created_at: str
    updated_at: str

class SupplierResponse(SupplierCreateRequest):
    id: Optional[str]
    created_at: str
    updated_at: str

class SupplierUpdateRequest(SupplierCreateRequest):
    pass

