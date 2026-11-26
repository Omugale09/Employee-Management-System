from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.db.base import Base
from app.db.session import engine
from app import models

# API routers
from app.api.auth import router as auth_router
from app.api.employees import router as employee_router
from app.api.departments import router as department_router
from app.api.attendance import router as attendance_router
from app.api.leaves import router as leave_router
from app.api.reports import router as reports_router
from app.core.limiter import limiter


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Employee Management System API",
    description="Employee and Department Management APIs",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://192.168.0.114:5173",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)

# Register API routers
app.include_router(auth_router)
app.include_router(employee_router)
app.include_router(department_router)
app.include_router(attendance_router)
app.include_router(leave_router)
app.include_router(reports_router)

@app.get("/")
def home():
    return {
        "message": "Employee Management System API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "EMS",
    }