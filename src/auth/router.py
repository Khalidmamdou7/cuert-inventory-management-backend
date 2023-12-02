# router.py
# Defining the API endpoints go here and calling the service layer


from typing import Annotated

from fastapi import APIRouter, Depends, status

# An example of importing sth from a parent directory
# from ..models import ResponseModel

# An example of importing sth from the same directory (importing the whole file as module)
# from . import service as auth_service

# An example of importing sth from the same directory (importing specific functinos from the file)
# from .dependencies import authenticate_user_jwt, get_current_user


router = APIRouter()


# An example of a router
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register():
    # Calling the service layer here
    return {
        "status": "success",
        "message": "Account created successfully, Please confirm your email to login",
        "data": None,
    }
