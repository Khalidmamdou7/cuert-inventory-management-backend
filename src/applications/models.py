# models.py
# Pydantic models go here (not DB models) 



from pydantic import BaseModel, validator, Field, AnyUrl
from typing import Optional, Annotated
from datetime import datetime
from enum import Enum as PyEnum



class Candidate(BaseModel):
    address: Annotated[str, Field(..., examples=['123 Main St, City, State, Zip'])] = "No Address"
    cv_link: AnyUrl



class ApplicationCreateRequest(BaseModel):
    candidate: Candidate


class ApplicationInDB(ApplicationCreateRequest):
    id: Optional[str] = None
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()


class Application(BaseModel):
    id: Optional[str]
    candidate: Candidate
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()

