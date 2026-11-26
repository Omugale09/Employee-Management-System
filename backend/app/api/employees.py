
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.db.dependencies import get_db
from app.models.employee import Employee
from app.models.department import Department
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeRead,
    EmployeePage,
)

router = APIRouter(
    prefix="/api/v1/employees",
    tags=["Employees"]
)


def check_department(db: Session, department_id: int | None):
    if department_id is None:
        return

    department = db.get(Department, department_id)

    if department is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )


# CREATE EMPLOYEE
@router.post("/", response_model=EmployeeRead, status_code=201)
def create_employee(
    data: EmployeeCreate,
    db: Session = Depends(get_db)
):
    check_department(db, data.department_id)

    employee = Employee(**data.model_dump())

    db.add(employee)

    try:
        db.flush()

        # Generate employee code when one was not provided.
        if not employee.employee_code:
            employee.employee_code = f"EMP-{employee.id:05d}"

        db.commit()
        db.refresh(employee)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Employee email or employee code already exists"
        )

    return employee


# GET EMPLOYEES WITH SEARCH, FILTERS AND PAGINATION
@router.get("/", response_model=EmployeePage)
def get_employees(
    q: str | None = Query(default=None, max_length=100),
    department_id: int | None = Query(default=None, gt=0),
    employment_status: str | None = Query(
        default=None,
        pattern="^(active|inactive)$"
    ),
    employment_type: str | None = Query(
        default=None,
        pattern="^(full-time|part-time|contract|intern)$"
    ),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    statement = select(Employee).options(
        joinedload(Employee.department)
    )

    count_statement = select(func.count(Employee.id))

    conditions = []

    if q:
        search = f"%{q.strip()}%"

        conditions.append(
            or_(
                Employee.first_name.ilike(search),
                Employee.last_name.ilike(search),
                Employee.email.ilike(search),
                Employee.employee_code.ilike(search),
                Employee.job_title.ilike(search),
            )
        )

    if department_id is not None:
        conditions.append(
            Employee.department_id == department_id
        )

    if employment_status is not None:
        conditions.append(
            Employee.employment_status == employment_status
        )

    if employment_type is not None:
        conditions.append(
            Employee.employment_type == employment_type
        )

    if conditions:
        statement = statement.where(*conditions)
        count_statement = count_statement.where(*conditions)

    total = db.scalar(count_statement) or 0

    statement = (
        statement
        .order_by(Employee.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )

    employees = db.scalars(statement).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": employees,
    }


# GET EMPLOYEE BY ID
@router.get("/{employee_id}", response_model=EmployeeRead)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = db.scalar(
        select(Employee)
        .options(joinedload(Employee.department))
        .where(Employee.id == employee_id)
    )

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee


# UPDATE EMPLOYEE
@router.put("/{employee_id}", response_model=EmployeeRead)
def update_employee(
    employee_id: int,
    data: EmployeeUpdate,
    db: Session = Depends(get_db)
):
    employee = db.get(Employee, employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    updates = data.model_dump(exclude_unset=True)

    required_fields = {
        "first_name",
        "last_name",
        "email",
        "employment_status",
    }

    for field in required_fields:
        if field in updates and updates[field] is None:
            raise HTTPException(
                status_code=422,
                detail=f"{field} cannot be null"
            )

    check_department(
        db,
        updates.get("department_id", employee.department_id)
    )

    for key, value in updates.items():
        setattr(employee, key, value)

    try:
        db.commit()
        db.refresh(employee)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Employee email or employee code already exists"
        )

    return employee


# DELETE EMPLOYEE
@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = db.get(Employee, employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    db.delete(employee)
    db.commit()

    return {
        "message": "Employee deleted successfully"
    }
