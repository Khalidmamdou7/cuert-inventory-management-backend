# service.py
# Module specific business logic goes here

from typing import Annotated



from fastapi import Depends, HTTPException, status

from .models import *
from .schemas import TeamsDB
from ..auth.schemas import UsersDB
from ..auth.models import User, RoleEnum


def create_team(team: TeamCreateRequest) -> TeamWithMembers | TeamWithoutMembers:
    new_team = TeamsDB().add_team(team)
    return new_team

def get_teams(with_members: bool = False) -> list[TeamWithMembers | TeamWithoutMembers]:
    teams = TeamsDB().get_teams(with_members)
    return teams

def get_team(team_id: str, with_members: bool = False) -> TeamWithMembers | TeamWithoutMembers:
    team = TeamsDB().get_team(team_id, with_members)
    return team

def update_team(team_id: str, team: TeamCreateRequest) -> TeamWithMembers | TeamWithoutMembers:
    team_in_db = team.model_dump()
    updated_team = TeamsDB().update_team(team_id, TeamCreateRequest(**team_in_db))
    return updated_team

def delete_team(team_id: str) -> TeamWithMembers | TeamWithoutMembers:
    deleted_team = TeamsDB().delete_team(team_id)
    return deleted_team



