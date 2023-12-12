# models.py
# Pydantic models go here (not DB models) 


from enum import Enum as PyEnum
from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, Annotated
import re
import bcrypt
from ..auth.models import RoleEnum, User
from datetime import datetime


class TeamCreateRequest(BaseModel):
    name: Annotated[str, Field(..., min_length=3, examples=['Logistics'])] = "Logistics"
    description: Annotated[str | None, Field(..., examples=['Logistics team'])] = None

class TeamInDB(TeamCreateRequest):
    id: Optional[str] = Field(alias='_id', default=None)
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()

class TeamWithoutMembers(BaseModel):
    id: Optional[str]
    name: Annotated[str, Field(..., min_length=3, examples=['Logistics'])] = "Logistics"
    description: Annotated[str | None, Field(..., examples=['Logistics team'])] = None
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()


class TeamWithMembers(BaseModel):
    id: Optional[str]
    name: Annotated[str, Field(..., min_length=3, examples=['Logistics'])] = "Logistics"
    description: Annotated[str | None, Field(..., examples=['Logistics team'])] = None
    members: Annotated[list[User], Field(..., examples=[])] = []
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()


