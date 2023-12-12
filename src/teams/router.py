# router.py
# Defining the API endpoints go here and calling the service layer


from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from ..models import ResponseModel
from ..auth.dependencies import authenticate_user_jwt, get_current_user
from ..auth.models import RoleEnum, User

from . import service as teams_service
from .models import *


router = APIRouter()

@router.post("/", response_model=ResponseModel[TeamWithMembers | TeamWithoutMembers], status_code=status.HTTP_201_CREATED)
def create_team(team: TeamCreateRequest, current_user: User = Depends(get_current_user)):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only admins can create teams")
    
    team = teams_service.create_team(team)
    return {
        "status": "success",
        "message": "Team created successfully",
        "data": team
    }

@router.get("/", response_model=ResponseModel[list[TeamWithMembers | TeamWithoutMembers]])
def get_teams(current_user: User = Depends(get_current_user), with_members: bool = False):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only admins can get teams")
    teams = teams_service.get_teams(with_members)
    return {
        "status": "success",
        "message": "Teams retrieved successfully",
        "data": teams
    }

@router.get("/{team_id}", response_model=ResponseModel[TeamWithMembers | TeamWithoutMembers])
def get_team(team_id: str, current_user: User = Depends(get_current_user), with_members: bool = False):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only admins can get teams")
    team = teams_service.get_team(team_id, with_members)
    return {
        "status": "success",
        "message": "Team retrieved successfully",
        "data": team
    }

@router.put("/{team_id}", response_model=ResponseModel[TeamWithMembers | TeamWithoutMembers])
def update_team(team_id: str, team: TeamCreateRequest, current_user: User = Depends(get_current_user)):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only admins can update teams")
    team = teams_service.update_team(team_id, team)
    return {
        "status": "success",
        "message": "Team updated successfully",
        "data": team
    }

@router.delete("/{team_id}", response_model=ResponseModel[None], status_code=status.HTTP_200_OK)
def delete_team(team_id: str, current_user: User = Depends(get_current_user)):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only admins can delete teams")
    teams_service.delete_team(team_id)
    return {
        "status": "success",
        "message": "Team deleted successfully",
        "data": None
    }