import random
from datetime import date, timedelta
from sqlalchemy.orm import Session
from models import (
    Employee, EmployeeSalary, LeaveRecord,
    SkillRecord, AssetRecord, GoalRecord
)
from database import SessionLocal, engine

# -------------------------------------------
# Utility Generators
# -------------------------------------------
DEPARTMENTS = ["Engineering", "HR", "Finance", "Marketing", "IT Support", "AI Research"]
ROLES = ["Software Engineer", "Data Analyst", "AI Engineer", "HR Executive", "Finance Associate"]
LOCATIONS = ["Chennai", "Bangalore", "Hyderabad", "Mumbai"]

SKILLS = ["Python", "SQL", "Machine Learning", "Excel", "ReactJS", "Leadership"]
CERTIFICATIONS = ["AWS Practitioner", "Azure AI-900", "PMP", None, None]

ASSETS = ["Laptop", "Monitor", "Employee ID Card", "Access Card"]

LEAVE_TYPES = ["Sick Leave", "Casual Leave", "Earned Leave"]

GOAL_STATUS = ["In Progress", "Completed", "Pending Review"]

# -------------------------------------------
# Create Fake Employee Records
# -------------------------------------------
def create_employee(i):
    join_date = date(2022, random.randint(1, 12), random.randint(1, 28))

    return Employee(
        employee_code=f"EMP{i:03d}",
        name=f"Employee {i}",
        email=f"employee{i}@axisme.com",
        phone=f"98765{random.randint(10000, 99999)}",
        gender=random.choice(["Male", "Female"]),
        date_of_birth=date(1998 + random.randint(0, 5), random.randint(1, 12), random.randint(1, 28)),
        role=random.choice(ROLES),
        department=random.choice(DEPARTMENTS),
        job_level=random.choice(["L1", "L2", "L3"]),
        location=random.choice(LOCATIONS),
        join_date=join_date,
        employment_type=random.choice(["Full-Time", "Contract", "Intern"]),
        manager_id=None,  # Manager link optional
        emergency_contact="9876543210",
        address="123 Corporate Street, Chennai"
    )


def create_salary(employee_id):
    base = random.randint(400000, 1200000)

    return EmployeeSalary(
        employee_id=employee_id,
        ctc=base,
        basic_pay=base * 0.40,
        hra=base * 0.20,
        pf=base * 0.05,
        esi=base * 0.01,
        tax_deduction=base * 0.15,
        last_updated=date.today()
    )


def create_skill(employee_id):
    return SkillRecord(
        employee_id=employee_id,
        skill_name=random.choice(SKILLS),
        experience_years=random.randint(1, 7),
        certification=random.choice(CERTIFICATIONS)
    )


def create_leave(employee_id):
    start = date.today() - timedelta(days=random.randint(1, 60))
    return LeaveRecord(
        employee_id=employee_id,
        leave_type=random.choice(LEAVE_TYPES),
        start_date=start,
        end_date=start + timedelta(days=1),
        status=random.choice(["Approved", "Pending"])
    )


def create_asset(employee_id):
    return AssetRecord(
        employee_id=employee_id,
        asset_type=random.choice(ASSETS),
        serial_number=f"SN{random.randint(10000, 99999)}",
        issue_date=date.today() - timedelta(days=random.randint(30, 300)),
        status="Active"
    )


def create_goal(employee_id):
    return GoalRecord(
        employee_id=employee_id,
        goal_title="Quarterly Performance Objective",
        description="Improve productivity and meet team OKRs",
        due_date=date.today() + timedelta(days=90),
        status=random.choice(GOAL_STATUS)
    )


# -------------------------------------------
# Seed Database
# -------------------------------------------
def seed_database():
    db: Session = SessionLocal()

    print("⏳ Seeding HRMS employee database…")

    for i in range(1, 6):  # Create 5 employees (increase if needed)
        emp = create_employee(i)
        db.add(emp)
        db.commit()
        db.refresh(emp)

        # Add salary
        db.add(create_salary(emp.id))

        # Add skills
        for _ in range(3):
            db.add(create_skill(emp.id))

        # Add leave records
        for _ in range(2):
            db.add(create_leave(emp.id))

        # Add assets
        db.add(create_asset(emp.id))

        # Add goals
        db.add(create_goal(emp.id))

        db.commit()

        print(f"✅ Added Employee {emp.employee_code}")

    db.close()
    print("\n🎉 DATABASE SEEDING COMPLETED SUCCESSFULLY!")


if __name__ == "__main__":
    seed_database()
