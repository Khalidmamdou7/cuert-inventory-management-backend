# service.py
# Module specific business logic goes here

from typing import Annotated
from .models import *
from .schemas import JobsDB
from ..auth.schemas import UsersDB
from ..auth.models import User, RoleEnum


def create_job(job: JobCreateRequest):
    new_job = JobsDB().add_job(job)
    return new_job

def get_jobs():
    jobs = JobsDB().get_jobs()
    return jobs

def get_job(job_id: str):
    job = JobsDB().get_job(job_id)
    return job

def update_job(job_id: str, job: JobCreateRequest):
    job_in_db = job.model_dump()
    updated_job = JobsDB().update_job(job_id, JobCreateRequest(**job_in_db))
    return updated_job

def delete_job(job_id: str):
    deleted_job = JobsDB().delete_job(job_id)
    return deleted_job
