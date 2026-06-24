from src.database.session import SessionLocal

from src.entities.department import Department
from src.entities.employee import Employee
from src.entities.skill import Skill
from src.entities.employee_skill import EmployeeSkill
from src.entities.employee_availability import EmployeeAvailability
from src.entities.technology import Technology
from src.entities.infrastructure import Infrastructure
from src.entities.completed_project import CompletedProject

from data.seeds.departments import DEPARTMENTS
from data.seeds.employees import EMPLOYEES
from data.seeds.skills import SKILLS
from data.seeds.employee_skills import EMPLOYEE_SKILLS
from data.seeds.availability import AVAILABILITY
from data.seeds.technologies import TECHNOLOGIES
from data.seeds.infrastructure import INFRASTRUCTURE
from data.seeds.completed_projects import COMPLETED_PROJECTS


session = SessionLocal()


# ----------------------------
# Departments
# ----------------------------

department_count = 0

for data in DEPARTMENTS:

    department = session.query(Department).filter_by(
        department_name=data["department_name"]
    ).first()

    if department is None:

        session.add(Department(**data))
        department_count += 1

session.commit()


# ----------------------------
# Employees
# ----------------------------

employee_count = 0

for data in EMPLOYEES:

    employee = session.query(Employee).filter_by(
        email=data["email"]
    ).first()

    if employee is None:

        department = session.query(Department).filter_by(
            department_name=data["department"]
        ).first()

        session.add(

            Employee(
                department_id=department.department_id,
                employee_name=data["employee_name"],
                designation=data["designation"],
                years_of_experience=data["years_of_experience"],
                email=data["email"],
                employment_type=data["employment_type"]
            )

        )

        employee_count += 1

session.commit()


# ----------------------------
# Skills
# ----------------------------

skill_count = 0

for data in SKILLS:

    skill = session.query(Skill).filter_by(
        skill_name=data["skill_name"]
    ).first()

    if skill is None:

        session.add(Skill(**data))
        skill_count += 1

session.commit()


# ----------------------------
# Employee Skills
# ----------------------------

employee_skill_count = 0

for data in EMPLOYEE_SKILLS:

    employee = session.query(Employee).filter_by(
        email=data["employee"]
    ).first()

    skill = session.query(Skill).filter_by(
        skill_name=data["skill"]
    ).first()

    exists = session.query(EmployeeSkill).filter_by(
        employee_id=employee.employee_id,
        skill_id=skill.skill_id
    ).first()

    if exists is None:

        session.add(

            EmployeeSkill(
                employee_id=employee.employee_id,
                skill_id=skill.skill_id,
                proficiency_level=data["proficiency_level"]
            )

        )

        employee_skill_count += 1

session.commit()


# ----------------------------
# Availability
# ----------------------------

availability_count = 0

for data in AVAILABILITY:

    employee = session.query(Employee).filter_by(
        email=data["employee"]
    ).first()

    exists = session.query(EmployeeAvailability).filter_by(
        employee_id=employee.employee_id
    ).first()

    if exists is None:

        session.add(

            EmployeeAvailability(
                employee_id=employee.employee_id,
                availability_status=data["availability_status"],
                available_hours_per_week=data["available_hours_per_week"],
                current_project=data["current_project"]
            )

        )

        availability_count += 1

session.commit()


# ----------------------------
# Technologies
# ----------------------------

technology_count = 0

for data in TECHNOLOGIES:

    exists = session.query(Technology).filter_by(
        technology_name=data["technology_name"]
    ).first()

    if exists is None:

        session.add(Technology(**data))
        technology_count += 1

session.commit()


# ----------------------------
# Infrastructure
# ----------------------------

infrastructure_count = 0

for data in INFRASTRUCTURE:

    exists = session.query(Infrastructure).filter_by(
        resource_name=data["resource_name"]
    ).first()

    if exists is None:

        session.add(Infrastructure(**data))
        infrastructure_count += 1

session.commit()


# ----------------------------
# Completed Projects
# ----------------------------

project_count = 0

for data in COMPLETED_PROJECTS:

    exists = session.query(CompletedProject).filter_by(
        project_name=data["project_name"]
    ).first()

    if exists is None:

        session.add(CompletedProject(**data))
        project_count += 1

session.commit()


print("\n==============================")
print("Company Knowledge Base Ready")
print("==============================")

print(f"Departments Added       : {department_count}")
print(f"Employees Added         : {employee_count}")
print(f"Skills Added            : {skill_count}")
print(f"Employee Skills Added   : {employee_skill_count}")
print(f"Availability Added      : {availability_count}")
print(f"Technologies Added      : {technology_count}")
print(f"Infrastructure Added    : {infrastructure_count}")
print(f"Completed Projects Added: {project_count}")

session.close()