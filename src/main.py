# root of the project, which inits the FastAPI app

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from .routes import routes
from .config import APP_SETTINGS
from fastapi.middleware.cors import CORSMiddleware
from .exceptions import custom_http_exception_handler, validation_exception_handler
from .database import Database
from contextlib import asynccontextmanager
from .auth.service import create_admin_user

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to be executed on application startup
    print("App startup, access the docs at: http://localhost:" + str(APP_SETTINGS.PORT) + "/docs")
    try:
        Database() # Initialize the database connection
        create_admin_user() # Create the admin user if it doesn't exist

    except Exception as e:
        raise e
        print("Error: Database connection failed")
    
    yield
    # Code to be executed on application shutdown
    print("App is shutting down")

description = """
This is the backend for the CUERT Inventory app, as well as the CUERT Recruitment system.

The app is currently in development, so expect bugs and unfinished features. If you find any bugs, please open an issue on the GitHub repository
"""

app = FastAPI(
    lifespan=lifespan, 
    title=APP_SETTINGS.APP_NAME,
    description=description,
    version="0.0.1",
    contact={
        "name": "CUERT-WEB-REPO",
        "url": "https://github.com/cuert-web/cuert-backend/issues"
    },
)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes)

app.add_exception_handler(HTTPException, custom_http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
    


@app.get("/")
async def root():
    return {"message": "Hello World from the root of the project"}