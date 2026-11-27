
from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.core.dependencies import get_current_user, require_roles

from app.models.user import User
from app.models.employee import Employee
from app.models.attendance import Attendance

from app.schemas.attendance import (
    AttendanceRead,
    AttendanceAdminRead,
)

router = APIRouter(
    prefix="/api/v1/attendance",
    tags=["Attendance"],
)


def get_employee_for_user(db: Session, user: User):
    """Find the employee record belonging to the logged-in user."""

    employee = db.scalar(
        select(Employee).where(Employee.email == user.email)
    )

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee record not found for this account",
        )

    return employee


# EMPLOYEE CHECK-IN
@router.post(
    "/check-in",
    response_model=AttendanceRead,
    status_code=201,
)
def check_in(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("employee")),
):
    employee = get_employee_for_user(db, current_user)
    today = date.today()

    existing_attendance = db.scalar(
        select(Attendance).where(
            Attendance.employee_id == employee.id,
            Attendance.attendance_date == today,
        )
    )

    if existing_attendance:
        raise HTTPException(
            status_code=409,
            detail="You have already checked in today",
        )

    attendance = Attendance(
        employee_id=employee.id,
        attendance_date=today,
        check_in=datetime.now(),
        status="present",
    )

    db.add(attendance)

    try:
        db.commit()
        db.refresh(attendance)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Attendance already exists for today",
        )

    return attendance


# EMPLOYEE CHECK-OUT
@router.post(
    "/check-out",
    response_model=AttendanceRead,
)
def check_out(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("employee")),
):
    employee = get_employee_for_user(db, current_user)
    today = date.today()

    attendance = db.scalar(
        select(Attendance).where(
            Attendance.employee_id == employee.id,
            Attendance.attendance_date == today,
        )
    )

    if attendance is None:
        raise HTTPException(
            status_code=404,
            detail="Please check in before checking out",
        )

    if attendance.check_out is not None:
        raise HTTPException(
            status_code=409,
            detail="You have already checked out today",
        )

    attendance.check_out = datetime.now()

    db.commit()
    db.refresh(attendance)

    return attendance


# EMPLOYEE: VIEW OWN ATTENDANCE HISTORY
@router.get(
    "/me",
    response_model=list[AttendanceRead],
)
def get_my_attendance(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("employee")),
):
    employee = get_employee_for_user(db, current_user)

    attendance_records = db.scalars(
        select(Attendance)
        .where(Attendance.employee_id == employee.id)
        .order_by(Attendance.attendance_date.desc())
    ).all()

    return attendance_records


# ADMIN / HR: VIEW ALL EMPLOYEE ATTENDANCE
@router.get(
    "/",
    response_model=list[AttendanceAdminRead],
)
def get_all_attendance(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "hr")),
):
    records = db.execute(
        select(Attendance, Employee)
        .join(Employee, Attendance.employee_id == Employee.id)
        .order_by(Attendance.attendance_date.desc())
    ).all()

    return [
        {
            "id": attendance.id,
            "employee_id": attendance.employee_id,
            "attendance_date": attendance.attendance_date,
            "check_in": attendance.check_in,
            "check_out": attendance.check_out,
            "status": attendance.status,
            "created_at": attendance.created_at,
            "employee_name": (
                f"{employee.first_name} {employee.last_name}"
            ),
            "employee_email": employee.email,
        }
        for attendance, employee in records
    ]
