from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.department import Department
from app.models.employee import Employee
from app.schemas.department import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentRead
)

router = APIRouter(
    prefix="/api/v1/departments",
    tags=["Departments"]
)


# CREATE department
@router.post("/", response_model=DepartmentRead, status_code=201)
def create_department(
    data: DepartmentCreate,
    db: Session = Depends(get_db)
):

    department = Department(**data.model_dump())

    db.add(department)

    try:
        db.commit()
        db.refresh(department)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Department name already exists"
        )

    return department


# GET all departments
@router.get("/", response_model=list[DepartmentRead])
def get_departments(
    db: Session = Depends(get_db)
):

    statement = select(Department).order_by(Department.id)

    return db.scalars(statement).all()


# GET department by ID
@router.get("/{department_id}", response_model=DepartmentRead)
def get_department(
    department_id: int,
    db: Session = Depends(get_db)
):

    department = db.get(Department, department_id)

    if department is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    return department


# UPDATE department
@router.put("/{department_id}", response_model=DepartmentRead)
def update_department(
    department_id: int,
    data: DepartmentUpdate,
    db: Session = Depends(get_db)
):

    department = db.get(Department, department_id)

    if department is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    updates = data.model_dump(exclude_unset=True)

    for key, value in updates.items():
        setattr(department, key, value)

    try:
        db.commit()
        db.refresh(department)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Department name already exists"
        )

    return department


# DELETE department
@router.delete("/{department_id}")
def delete_department(
    department_id: int,
    db: Session = Depends(get_db)
):

    department = db.get(Department, department_id)

    if department is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    employee_count = db.scalar(
        select(func.count(Employee.id)).where(
            Employee.department_id == department_id
        )
    )

    if employee_count:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete department with assigned employees"
        )

    db.delete(department)
    db.commit()

    return {"message": "Department deleted successfully"}