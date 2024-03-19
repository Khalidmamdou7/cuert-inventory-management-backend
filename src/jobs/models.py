# models.py
# Pydantic models go here (not DB models) 



from pydantic import BaseModel, validator, Field
from typing import Optional, Annotated
from datetime import datetime
from enum import Enum as PyEnum


class QuestionTypeEnum(str,PyEnum):
    SHORT = 'short'
    MCQ = 'mcq'
    ESSAY = 'essay'


class Question(BaseModel):
    question: Annotated[str, Field(..., examples=['write a question'])]
    type: Annotated[QuestionTypeEnum, Field(..., examples=['short'])] = QuestionTypeEnum.SHORT
    options: Annotated[list[str], Field(..., examples=[['option 1', 'option 2']])] = "No Options"


class Team(BaseModel):
    team_name: Annotated[str, Field(..., examples=['web development'])]
    division_name: Annotated[str, Field(..., examples=['logistics and planning'])]



class JobCreateRequest(BaseModel):
    title: Annotated[str, Field(..., examples=['Team member'])]
    description: Annotated[str, Field(..., examples=['description about the job'])] = "No description"
    requirements: Annotated[str, Field(..., examples=['requirements for the job'])] = "No requirements"
    date_created: str = datetime.now().isoformat()
    date_posted: Annotated[datetime, Field(..., examples=['2024-03-19T18:37:24.543197'])]
    deadline: Annotated[datetime, Field(..., examples=['2024-03-19T18:37:24.543197'])]
    isActive: Annotated[bool, Field(..., examples=[False])]
    team: Team
    questions: list[Question]


class JobInDB(JobCreateRequest):
    id: Optional[str] = None
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()


class Job(BaseModel):
    id: Optional[str]
    created_at: str = datetime.now().isoformat()
    updated_at: str = datetime.now().isoformat()
    title: Annotated[str, Field(..., examples=['Team member'])]
    description: Annotated[str, Field(..., examples=['description about the job'])] = "No description"
    requirements: Annotated[str, Field(..., examples=['requirements for the job'])] = "No requirements"
    date_created: str = datetime.now().isoformat()
    date_posted: Annotated[datetime, Field(..., examples=['2024-03-19T18:37:24.543197'])]
    deadline: Annotated[datetime, Field(..., examples=['2024-03-19T18:37:24.543197'])]
    isActive: Annotated[bool, Field(..., examples=[False])]
    team: Team
    questions: list[Question]

