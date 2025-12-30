from datetime import date
from sqlalchemy.orm import Session

from models import LeaveRecord


def apply_leave(
    db: Session,
    employee_id: int,
    leave_type: str,
    start_date: date,
    end_date: date
) -> LeaveRecord:
    """
    Creates a new leave request for an employee.
    Default status is set to 'Pending'.
    """

    leave = LeaveRecord(
        employee_id=employee_id,
        leave_type=leave_type,
        start_date=start_date,
        end_date=end_date,
        status="Pending"
    )

    db.add(leave)
    db.commit()
    db.refresh(leave)

    return leave
