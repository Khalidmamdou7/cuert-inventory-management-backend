# router.py
# Defining the API endpoints go here and calling the service layer


from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from ..models import ResponseModel
from ..auth.dependencies import authenticate_user_jwt, get_current_user
from ..auth.models import RoleEnum, User

from . import service as jobs_service
from .models import *


router = APIRouter()

@router.post("/", response_model=ResponseModel[Job], status_code=status.HTTP_201_CREATED)
def create_job(job: JobCreateRequest, current_user: User = Depends(get_current_user)):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only admins can create Jobs")
    
    job = jobs_service.create_job(job)
    return {
        "status": "success",
        "message": "Job created successfully",
        "data": job
    }

@router.get("/", response_model=ResponseModel[list[Job]])
def get_jobs(current_user: User = Depends(get_current_user)):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only admins can get Jobs")
    jobs = jobs_service.get_jobs()
    return {
        "status": "success",
        "message": "Jobs retrieved successfully",
        "data": jobs
    }

@router.get("/{job_id}", response_model=ResponseModel[Job])
def get_job(job_id: str, current_user: User = Depends(get_current_user) ):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only admins can get Jobs")
    job = jobs_service.get_job(job_id)
    return {
        "status": "success",
        "message": "Job retrieved successfully",
        "data": job
    }

@router.put("/{job_id}", response_model=ResponseModel[Job])
def update_job(job_id: str, job: JobCreateRequest, current_user: User = Depends(get_current_user)):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only admins can update Jobs")
    job = jobs_service.update_job(job_id, job)
    return {
        "status": "success",
        "message": "Job updated successfully",
        "data": job
    }

@router.delete("/{job_id}", response_model=ResponseModel[None], status_code=status.HTTP_200_OK)
def delete_job(job_id: str, current_user: User = Depends(get_current_user)):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only admins can delete Jobs")
    jobs_service.delete_job(job_id)
    return {
        "status": "success",
        "message": "Job deleted successfully",
        "data": None
    }
