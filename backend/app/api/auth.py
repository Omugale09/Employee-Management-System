
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.limiter import limiter
from app.core.dependencies import get_current_user
from app.db.dependencies import get_db

from app.models.user import User
from app.models.employee import Employee

from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    UserResponse,
)

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)

from app.core.config import settings


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)


# REGISTER
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db),
):
    email = str(data.email).lower()

    existing_user = db.scalar(
        select(User).where(User.email == email)
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Account already exists",
        )

    # Only employees with an existing employee record can register.
    employee = db.scalar(
        select(Employee).where(Employee.email == email)
    )

    if employee is None:
        raise HTTPException(
            status_code=403,
            detail="No employee record found for this email. Contact HR.",
        )

    user = User(
        email=email,
        hashed_password=hash_password(data.password),
        role="employee",
        is_active=True,
    )

    db.add(user)

    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Account already exists",
        )

    return user


# LOGIN
@router.post(
    "/login",
    response_model=TokenResponse,
)
@limiter.limit("5/minute")
def login(
    request: Request,
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    email = str(data.email).lower()

    user = db.scalar(
        select(User).where(User.email == email)
    )

    if user is None or not verify_password(
        data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Your account is inactive",
        )

    token = create_access_token(
        user_id=user.id,
        role=user.role,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": user,
    }


# GET CURRENT USER
@router.get(
    "/me",
    response_model=UserResponse,
)
def get_profile(
    current_user: User = Depends(get_current_user),
):
    return current_user
