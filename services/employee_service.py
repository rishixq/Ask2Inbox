from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import (
    Employee,
    EmployeeSalary,
    LeaveRecord,
    SkillRecord,
    GoalRecord,
    AssetRecord
)


def get_employee_by_code(db: Session, employee_code: str):
    return (
        db.query(Employee)
        .filter(Employee.employee_code == employee_code)
        .first()
    )


def get_full_employee_profile(db: Session, employee_id: int):
    # =====================
    # EMPLOYEE
    # =====================
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    # =====================
    # RELATED TABLES
    # =====================
    salary = (
        db.query(EmployeeSalary)
        .filter(EmployeeSalary.employee_id == employee_id)
        .first()
    )

    leaves = (
        db.query(LeaveRecord)
        .filter(LeaveRecord.employee_id == employee_id)
        .all()
    )

    skills = (
        db.query(SkillRecord)
        .filter(SkillRecord.employee_id == employee_id)
        .all()
    )

    goals = (
        db.query(GoalRecord)
        .filter(GoalRecord.employee_id == employee_id)
        .all()
    )

    assets = (
        db.query(AssetRecord)
        .filter(AssetRecord.employee_id == employee_id)
        .all()
    )

    # =====================
    # SERIALIZED RESPONSE
    # =====================
    return {
        # =====================
        # EMPLOYEE MASTER
        # =====================
        "id": employee.id,
        "employee_code": employee.employee_code,
        "name": employee.name,
        "email": employee.email,
        "phone": employee.phone,
        "gender": employee.gender,

        "dob": (
            str(employee.date_of_birth)
            if employee.date_of_birth is not None
            else None
        ),

        "role": employee.role,
        "department": employee.department,
        "job_level": employee.job_level,
        "location": employee.location,

        "join_date": (
            str(employee.join_date)
            if employee.join_date is not None
            else None
        ),

        "employment_type": employee.employment_type,
        "emergency_contact": employee.emergency_contact,
        "address": employee.address,

        # =====================
        # SALARY (ONE-TO-ONE)
        # =====================
        "salary": (
            {
                "ctc": salary.ctc,
                "basic_pay": salary.basic_pay,
                "hra": salary.hra,
                "pf": salary.pf,
                "esi": salary.esi,
                "tax_deduction": salary.tax_deduction,
                "last_updated": (
                    str(salary.last_updated)
                    if salary.last_updated is not None
                    else None
                ),
            }
            if salary is not None
            else None
        ),

        # =====================
        # LEAVES (ONE-TO-MANY)
        # =====================
        "leave_history": [
            {
                "leave_type": l.leave_type,
                "start_date": (
                    str(l.start_date)
                    if l.start_date is not None
                    else None
                ),
                "end_date": (
                    str(l.end_date)
                    if l.end_date is not None
                    else None
                ),
                "status": l.status,
            }
            for l in leaves
        ],

        # =====================
        # SKILLS
        # =====================
        "skills": [
            {
                "skill_name": s.skill_name,
                "experience_years": s.experience_years,
                "certification": s.certification,
            }
            for s in skills
        ],

        # =====================
        # ASSETS
        # =====================
        "assets": [
            {
                "asset_type": a.asset_type,
                "serial_number": a.serial_number,
                "issue_date": (
                    str(a.issue_date)
                    if a.issue_date is not None
                    else None
                ),
                "return_date": (
                    str(a.return_date)
                    if a.return_date is not None
                    else None
                ),
                "status": a.status,
            }
            for a in assets
        ],

        # =====================
        # GOALS
        # =====================
        "goals": [
            {
                "goal_title": g.goal_title,
                "description": g.description,
                "due_date": (
                    str(g.due_date)
                    if g.due_date is not None
                    else None
                ),
                "status": g.status,
            }
            for g in goals
        ],
    }
