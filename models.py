from sqlalchemy import (
    Column, Integer, String, Date, Text, Float, ForeignKey, Boolean, JSON
)
from sqlalchemy.orm import relationship
from database import Base, engine

# ============================================================
#  EMPLOYEE MASTER TABLE — Primary Profile
# ============================================================
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50), unique=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, index=True)
    phone = Column(String(20))
    gender = Column(String(10))
    date_of_birth = Column(Date)

    role = Column(String(100), nullable=False)
    department = Column(String(100))
    job_level = Column(String(50))
    location = Column(String(100))
    join_date = Column(Date)
    employment_type = Column(String(50))  # Full-time, Contract, Intern

    manager_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    manager = relationship("Employee", remote_side=[id])

    emergency_contact = Column(String(100))
    address = Column(Text)

    # Relationships
    salary = relationship("EmployeeSalary", back_populates="employee", uselist=False)
    leaves = relationship("LeaveRecord", back_populates="employee")
    skills = relationship("SkillRecord", back_populates="employee")
    assets = relationship("AssetRecord", back_populates="employee")
    goals = relationship("GoalRecord", back_populates="employee")

# ============================================================
#  SALARY / PAYROLL TABLE
# ============================================================
class EmployeeSalary(Base):
    __tablename__ = "employee_salary"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    ctc = Column(Float)
    basic_pay = Column(Float)
    hra = Column(Float)
    pf = Column(Float)
    esi = Column(Float)
    tax_deduction = Column(Float)
    last_updated = Column(Date)

    employee = relationship("Employee", back_populates="salary")

# ============================================================
#  LEAVE RECORDS TABLE
# ============================================================
class LeaveRecord(Base):
    __tablename__ = "leave_records"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    leave_type = Column(String(50))  # Sick, Casual, Earned
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String(20))  # Approved, Pending, Rejected

    employee = relationship("Employee", back_populates="leaves")

# ============================================================
#  SKILLS & CERTIFICATIONS TABLE
# ============================================================
class SkillRecord(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    skill_name = Column(String(100))
    experience_years = Column(Float)
    certification = Column(String(150), nullable=True)

    employee = relationship("Employee", back_populates="skills")

# ============================================================
#  ASSETS ASSIGNED TABLE (Laptop, ID Card, etc)
# ============================================================
class AssetRecord(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    asset_type = Column(String(100))
    serial_number = Column(String(100))
    issue_date = Column(Date)
    return_date = Column(Date, nullable=True)
    status = Column(String(50))  # Active / Returned / Lost

    employee = relationship("Employee", back_populates="assets")

# ============================================================
#  PERFORMANCE GOALS TABLE
# ============================================================
class GoalRecord(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    goal_title = Column(String(200))
    description = Column(Text)
    due_date = Column(Date)
    status = Column(String(50))  # In progress / Completed / Pending Review

    employee = relationship("Employee", back_populates="goals")


# ============================================================
#  CREATE ALL TABLES
# ============================================================
def create_tables():
    print("⏳ Creating corporate-grade HRMS tables in Supabase…")
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully!")


if __name__ == "__main__":
    create_tables()
