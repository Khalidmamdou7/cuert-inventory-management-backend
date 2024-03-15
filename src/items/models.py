# models.py
# Pydantic models go here (not DB models) 



from pydantic import BaseModel, validator, Field
from typing import Optional, Annotated
from datetime import datetime
from enum import Enum as PyEnum


class ItemStatusEnum(str,PyEnum):
    AVAILABLE = 'available'
    UNAVAILABLE = 'unavailable'



class ItemCreateRequest(BaseModel):
    name: str
    code: str
    unit_of_measure: str
    quantity: int
    specifications: Optional[str] = None
    status: Annotated[ItemStatusEnum, Field(..., examples=['available'])] = ItemStatusEnum.AVAILABLE


class ItemInDB(ItemCreateRequest):
    id: Optional[str] = None
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()


class Item(BaseModel):
    id: Optional[str]
    name: str
    code: str
    unit_of_measure: str
    quantity: int
    specifications: Optional[str] = None
    status: Annotated[ItemStatusEnum, Field(..., examples=['available'])] = ItemStatusEnum.AVAILABLE
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()

