# models.py
# Pydantic models go here (not DB models) 


# from enum import Enum as PyEnum
# from pydantic import BaseModel, validator, Field
# from typing import Optional, Annotated
# import re
# from datetime import datetime

# class ItemStatusEnum(PyEnum):
#     AVAILABLE = "available"
#     UNAVAILABLE = "unavailable"

# class ItemCreateRequest(BaseModel):
#     name: Annotated[str, Field(..., min_length=3, examples=['motor'])] = "motor"
#     code: Annotated[str, Field(..., min_length=3, examples=['ABC123'])] = "ABC123"
#     unit_of_measure: Annotated[str, Field(..., min_length=1, examples=['kg'])] = "kg"
#     quantity: Annotated[int, Field(..., examples=[10])] = 10
#     specifications: Annotated[str | None, Field(..., examples=['item specifications'])] = None
#     status: Annotated[ItemStatusEnum, Field(..., examples=[ItemStatusEnum.AVAILABLE])] = ItemStatusEnum.AVAILABLE

# class ItemInDB(ItemCreateRequest):
#     id: Optional[str] = Field(alias='_id', default=None)
#     created_at: str = datetime.now().isoformat()
#     updated_at: str = datetime.now().isoformat()


# class Item(BaseModel):
#     id: Optional[str]
#     name: Annotated[str, Field(..., min_length=3, examples=['motor'])] = "motor"
#     code: Annotated[str, Field(..., min_length=3, examples=['ABC123'])] = "ABC123"
#     unit_of_measure: Annotated[str, Field(..., min_length=1, examples=['kg'])] = "kg"
#     quantity: Annotated[int, Field(..., examples=[10])] = 10
#     specifications: Annotated[str | None, Field(..., examples=['item specifications'])] = None
#     status: Annotated[ItemStatusEnum, Field(..., examples=[ItemStatusEnum.AVAILABLE])] = ItemStatusEnum.AVAILABLE
#     created_at: str = datetime.now().isoformat()
#     updated_at: str = datetime.now().isoformat()

# class ItemWithoutSpecifications(BaseModel):
#     id: Optional[str]
#     name: Annotated[str, Field(..., min_length=3, examples=['motor'])] = "motor"
#     code: Annotated[str, Field(..., min_length=3, examples=['ABC123'])] = "ABC123"
#     unit_of_measure: Annotated[str, Field(..., min_length=1, examples=['kg'])] = "kg"
#     quantity: Annotated[int, Field(..., examples=[10])] = 10
#     status: Annotated[ItemStatusEnum, Field(..., examples=[ItemStatusEnum.AVAILABLE])] = ItemStatusEnum.AVAILABLE
#     created_at: str = datetime.now().isoformat()
#     updated_at: str = datetime.now().isoformat()


# class ItemWithSpecifications(BaseModel):
#     id: Optional[str]
#     name: Annotated[str, Field(..., min_length=3, examples=['motor'])] = "motor"
#     code: Annotated[str, Field(..., min_length=3, examples=['ABC123'])] = "ABC123"
#     unit_of_measure: Annotated[str, Field(..., min_length=1, examples=['kg'])] = "kg"
#     quantity: Annotated[int, Field(..., examples=[10])] = 10
#     specifications: Annotated[str | None, Field(..., examples=['item specifications'])] = None
#     status: Annotated[ItemStatusEnum, Field(..., examples=[ItemStatusEnum.AVAILABLE])] = ItemStatusEnum.AVAILABLE
#     created_at: str = datetime.now().isoformat()
#     updated_at: str = datetime.now().isoformat()





from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

class ItemCreateRequest(BaseModel):
    name: str
    code: str
    unit_of_measure: str
    quantity: int
    specifications: Optional[str] = None
    status: str = "available"

    @validator("status")
    def validate_status(cls, v):
        if v not in ["available", "unavailable"]:
            raise ValueError("Status must be 'available' or 'unavailable'")
        return v

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
    status: str = "available"
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()

    @validator("status")
    def validate_status(cls, v):
        if v not in ["available", "unavailable"]:
            raise ValueError("Status must be 'available' or 'unavailable'")
        return v
