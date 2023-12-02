# root of the project, which inits the FastAPI app

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from .routes import routes
from .config import APP_SETTINGS
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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

# app.add_exception_handler(HTTPException, custom_http_exception_handler)
# app.add_exception_handler(RequestValidationError, validation_exception_handler)



@app.get("/")
async def root():
    return {"message": "Hello World from the root of the project"}