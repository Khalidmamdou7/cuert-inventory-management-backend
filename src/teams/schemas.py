# schemas.py
# DB logic goes here


from fastapi import HTTPException, status
from .models import *
from ..database import Database
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
import bson
from datetime import datetime
from ..utils.utils import db_to_dict
from ..auth.models import UserResponse, UserInDB



class TeamsDB():
    def __init__(self):
        self.db = Database()
        self.collection = self.db.get_collection('teams')
    
    def add_team(self, team: TeamCreateRequest):
        """
        Add a new team to the database.

        Args:
            team (TeamCreateRequest): the team to be added

        Returns:
            TeamInDB: the team that was added
        
        Raises:
            HTTPException: if the team already exists, or data validation fails
        """
        try:
            team_in_db = team.model_dump()
            team_in_db["created_at"] = datetime.now().isoformat()
            team_in_db["updated_at"] = datetime.now().isoformat()
            team_in_db["_id"] = self.collection.insert_one(team_in_db).inserted_id
            print(team_in_db)
            return TeamWithMembers(**db_to_dict(team_in_db))
        except DuplicateKeyError as e:
            duplicate_key = list(e.details['keyPattern'].keys())[0]
            raise HTTPException(status_code=400, detail="Team already exists with the same " + duplicate_key)
        

    
    def get_team(self, team_id: str, with_members: bool = False) -> TeamWithoutMembers | TeamWithMembers:
        """
        Get a team from the database.

        Args:
            team_id (str): the id of the team to be retrieved
            with_members (bool): whether to include the members in the response or not

        Returns:
            TeamWithoutMembers | TeamWithMembers: the team that was retrieved
        
        """
        try:
            team = self.collection.find_one({"_id": ObjectId(team_id)})
        except bson.errors.InvalidId:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team id is invalid")
        
        if team is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
        if with_members:
            team["members"] = self._get_team_members(team_id)
            return TeamWithMembers(**db_to_dict(team))

        return TeamWithoutMembers(**db_to_dict(team))
    
    def get_teams(self, with_members: bool = False) -> list[TeamWithoutMembers | TeamWithMembers]:
        """
        Get all teams from the database.

        Args:
            with_members (bool): whether to include the members in the response or not

        Returns:
            list[TeamWithoutMembers | TeamWithMembers]: the teams that were retrieved
        
        """
        
        teams = self.collection.find()
        if with_members:
            # TODO: optimize this
            teams = [team for team in teams]
            for team in teams:
                team["members"] = self._get_team_members(team["_id"])
            return [TeamWithMembers(**db_to_dict(team)) for team in teams]
        return [TeamWithoutMembers(**db_to_dict(team)) for team in teams]
    
    def update_team(self, team_id: str, team: TeamCreateRequest):
        """
        Update a team in the database.

        Args:
            team_id (str): the id of the team to be updated
            team (TeamCreateRequest): the team data to be updated

        Returns:
            TeamInDB: the team that was updated
        
        Raises:
            HTTPException: if the team doesn't exist, or data validation fails
        """
        team_in_db = team.model_dump()
        team_in_db["updated_at"] = datetime.now().isoformat()
        try:
            self.collection.update_one({"_id": ObjectId(team_id)}, {"$set": team_in_db})
        except DuplicateKeyError as e:
            duplicate_key = list(e.details['keyPattern'].keys())[0]
            raise HTTPException(status_code=400, detail="Team already exists with the same " + duplicate_key)
        except bson.errors.InvalidId:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team id is invalid")
        return self.get_team(team_id)
    
    def delete_team(self, team_id: str):
        """
        Delete a team from the database.

        Args:
            team_id (str): the id of the team to be deleted

        Returns:
            TeamInDB: the team that was deleted
        
        Raises:
            HTTPException: if the team doesn't exist
        """
        try:
            team = self.get_team(team_id)
        except bson.errors.InvalidId:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team id is invalid")
        self.collection.delete_one({"_id": ObjectId(team_id)})
        self.db.get_collection('users_teams').delete_many({"team_id": ObjectId(team_id)})
        return team

    def _get_team_members(self, team_id: str) -> list[UserResponse]:
        """
        Get the members of a team from the database.

        Args:
            team_id (str): the id of the team to get its members

        Returns:
            list[UserResponse]: the members of the team
        
        Raises:
            HTTPException: if the team doesn't exist
        """
        try:
            result = self.db.get_collection('users_teams').find({"team_id": ObjectId(team_id)})
        except bson.errors.InvalidId:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team id is invalid")
        users_ids = [entry["user_id"] for entry in result]
        print(users_ids)
        users_db_objs = [self.db.get_collection('users').find_one({"_id": ObjectId(user_id)}) for user_id in users_ids]
        print(users_db_objs)
        return [UserResponse(**db_to_dict(user)) for user in users_db_objs]