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



class JobsDB():
    def __init__(self):
        self.db = Database()
        self.collection = self.db.get_collection('jobs')
    
    def add_job(self, job: JobCreateRequest):
        """
        Add a new job to the database.

        Args:
            job (JobCreateRequest): the job to be added

        Returns:
            JobInDB: the job that was added
        
        Raises:
            HTTPException: if the job already exists, or data validation fails
        """
        try:
            job_in_db = job.model_dump()
            job_in_db["created_at"] = datetime.now().isoformat()
            job_in_db["updated_at"] = datetime.now().isoformat()
            job_in_db["_id"] = self.collection.insert_one(job_in_db).inserted_id
            print(job_in_db)
            return Job(**db_to_dict(job_in_db))
        except DuplicateKeyError as e:
            duplicate_key = list(e.details['keyPattern'].keys())[0]
            raise HTTPException(status_code=400, detail="job already exists with the same " + duplicate_key)
        

    
    def get_job(self, job_id: str):
        """
        Get a job from the database.

        Args:
            job_id (str): the id of the job to be retrieved

        Returns:
            the job that was retrieved
        
        """
        try:
            job = self.collection.find_one({"_id": ObjectId(job_id)})
        except bson.errors.InvalidId:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="job id is invalid")
        
        if job is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="job not found")

        return Job(**db_to_dict(job))
    
    def get_jobs(self):
        """
        Get all jobs from the database.

        Returns:
            the jobs that were retrieved
        
        """
        jobs = self.collection.find()
        return [Job(**db_to_dict(job)) for job in jobs]
    
    def update_job(self, job_id: str, job: JobCreateRequest):
        """
        Update a job in the database.

        Args:
            job_id (str): the id of the job to be updated
            job (JobCreateRequest): the job data to be updated

        Returns:
            JobInDB: the job that was updated
        
        Raises:
            HTTPException: if the job doesn't exist, or data validation fails
        """
        job_in_db = job.model_dump()
        job_in_db["updated_at"] = datetime.now().isoformat()
        try:
            self.collection.update_one({"_id": ObjectId(job_id)}, {"$set": job_in_db})
        except DuplicateKeyError as e:
            duplicate_key = list(e.details['keyPattern'].keys())[0]
            raise HTTPException(status_code=400, detail="job already exists with the same " + duplicate_key)
        except bson.errors.InvalidId:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="job id is invalid")
        return self.get_job(job_id)
    
    def delete_job(self, job_id: str):
        """
        Delete a job from the database.

        Args:
            job_id (str): the id of the job to be deleted

        Returns:
            JobInDB: the job that was deleted
        
        Raises:
            HTTPException: if the job doesn't exist
        """
        try:
            job = self.get_job(job_id)
        except bson.errors.InvalidId:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="job id is invalid")
        self.collection.delete_one({"_id": ObjectId(job_id)})
        self.db.get_collection('users_jobs').delete_many({"job_id": ObjectId(job_id)})
        return job

