import os
from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from src.config.settings import settings
from src.database.session import SessionLocal

# Import models for CRUD
from src.entities.employee import Employee
from src.entities.skill import Skill
from src.entities.technology import Technology
from src.entities.infrastructure import Infrastructure
from src.schemas.infrastructure_status import InfrastructureStatus
from src.entities.department import Department
from src.entities.project_qualification import ProjectQualification
from src.entities.manager_notification import ManagerNotification
from src.entities.employee_skill import EmployeeSkill
from src.entities.employee_availability import EmployeeAvailability
from src.schemas.availability_status import AvailabilityStatus
from src.controllers.analysis_pipeline_controller import AnalysisPipelineController
from fastapi import BackgroundTasks

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

dashboard_router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

# --- Authentication Dependency ---
def verify_manager(request: Request):
    auth_cookie = request.cookies.get("manager_auth")
    if auth_cookie != "true":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return True

# --- Login Routes ---
@dashboard_router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={"request": request})

@dashboard_router.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == settings.MANAGER_USERNAME and password == settings.MANAGER_PASSWORD:
        response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="manager_auth", value="true", httponly=True)
        return response
    
    return templates.TemplateResponse(request=request, name="login.html", context={
        "request": request, 
        "error": "Invalid manager credentials"
    })

@dashboard_router.get("/logout")
async def logout():
    response = RedirectResponse(url="/dashboard/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("manager_auth")
    return response

# --- Dashboard Home (Protected) ---
@dashboard_router.get("/", response_class=HTMLResponse)
async def dashboard_home(request: Request):
    try:
        verify_manager(request)
    except HTTPException:
        return RedirectResponse(url="/dashboard/login", status_code=status.HTTP_302_FOUND)
        
    session = SessionLocal()
    try:
        # Fetch stats for the dashboard
        stats = {
            "employees": session.query(Employee).count(),
            "technologies": session.query(Technology).count(),
            "active_qualifications": session.query(ProjectQualification).count(),
            "skills": session.query(Skill).count()
        }
        
        # Fetch actual data lists for the CRUD tables
        employees = session.query(Employee).all()
        technologies = session.query(Technology).all()
        infrastructures = session.query(Infrastructure).all()
        
        # We need the most recent qualifications
        qualifications = session.query(ProjectQualification).order_by(ProjectQualification.created_at.desc()).all()
        
        return templates.TemplateResponse(request=request, name="dashboard.html", context={
            "request": request,
            "stats": stats,
            "employees": employees,
            "technologies": technologies,
            "infrastructures": infrastructures,
            "qualifications": qualifications,
        })
    finally:
        session.close()

# --- Example Basic CRUD Endpoints (Protected API) ---
@dashboard_router.post("/api/employees/delete/{employee_id}")
async def delete_employee(request: Request, employee_id: int):
    verify_manager(request)
    session = SessionLocal()
    try:
        emp = session.query(Employee).filter_by(employee_id=employee_id).first()
        if emp:
            session.delete(emp)
            session.commit()
    finally:
        session.close()
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)

@dashboard_router.post("/api/technologies/delete/{tech_id}")
async def delete_technology(request: Request, tech_id: int):
    verify_manager(request)
    session = SessionLocal()
    try:
        tech = session.query(Technology).filter_by(technology_id=tech_id).first()
        if tech:
            session.delete(tech)
            session.commit()
    except Exception as e:
        session.rollback()
    finally:
        session.close()
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)

@dashboard_router.post("/api/infrastructure/delete/{infra_id}")
async def delete_infrastructure(request: Request, infra_id: int):
    verify_manager(request)
    session = SessionLocal()
    try:
        infra = session.query(Infrastructure).filter_by(infrastructure_id=infra_id).first()
        if infra:
            session.delete(infra)
            session.commit()
    except Exception as e:
        session.rollback()
    finally:
        session.close()
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)

@dashboard_router.post("/api/employees/edit/{employee_id}")
async def edit_employee(request: Request, employee_id: int, name: str = Form(...), email: str = Form(...), designation: str = Form(...)):
    verify_manager(request)
    session = SessionLocal()
    try:
        emp = session.query(Employee).filter_by(employee_id=employee_id).first()
        if emp:
            emp.employee_name = name
            emp.email = email
            emp.designation = designation
            session.commit()
    except Exception as e:
        session.rollback()
    finally:
        session.close()
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)

@dashboard_router.post("/api/technologies/edit/{tech_id}")
async def edit_technology(request: Request, tech_id: int, name: str = Form(...), category: str = Form(...), version: str = Form(...)):
    verify_manager(request)
    session = SessionLocal()
    try:
        tech = session.query(Technology).filter_by(technology_id=tech_id).first()
        if tech:
            tech.technology_name = name
            tech.technology_category = category
            tech.version = version
            session.commit()
    except Exception as e:
        session.rollback()
    finally:
        session.close()
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)

# --- CRM Report Endpoints ---
@dashboard_router.get("/api/crm_report/{qualification_id}")
async def get_crm_report(request: Request, qualification_id: int):
    verify_manager(request)
    session = SessionLocal()
    try:
        notification = session.query(ManagerNotification).filter_by(qualification_id=qualification_id).first()
        if not notification:
            raise HTTPException(status_code=404, detail="CRM Report not found")
            
        # Update status to READ
        if notification.status == "UNREAD":
            notification.status = "READ"
            session.commit()
            
        return notification.crm_report
    finally:
        session.close()

@dashboard_router.post("/api/override/{qualification_id}")
async def override_decision(request: Request, qualification_id: int, decision: str = Form(...)):
    verify_manager(request)
    session = SessionLocal()
    try:
        qual = session.query(ProjectQualification).filter_by(qualification_id=qualification_id).first()
        if not qual:
            raise HTTPException(status_code=404, detail="Qualification not found")
            
        qual.final_decision = decision
        session.commit()
    finally:
        session.close()
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)

# --- Add Endpoints ---
@dashboard_router.post("/api/technologies/add")
async def add_technology(request: Request, name: str = Form(...), category: str = Form(...), version: str = Form(...)):
    verify_manager(request)
    session = SessionLocal()
    try:
        new_tech = Technology(
            technology_name=name,
            technology_category=category,
            version=version
        )
        session.add(new_tech)
        session.commit()
    except Exception as e:
        session.rollback()
    finally:
        session.close()
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)

@dashboard_router.post("/api/infrastructure/add")
async def add_infrastructure(request: Request, name: str = Form(...), category: str = Form(...), type: str = Form(...), quantity: int = Form(...)):
    verify_manager(request)
    session = SessionLocal()
    try:
        new_infra = Infrastructure(
            resource_name=name,
            infrastructure_category=category,
            resource_type=type,
            quantity=quantity,
            availability_status=InfrastructureStatus.AVAILABLE
        )
        session.add(new_infra)
        session.commit()
    except Exception as e:
        session.rollback()
    finally:
        session.close()
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)

@dashboard_router.post("/api/infrastructure/edit/{infra_id}")
async def edit_infrastructure(request: Request, infra_id: int, name: str = Form(...), category: str = Form(...), type: str = Form(...), quantity: int = Form(...)):
    verify_manager(request)
    session = SessionLocal()
    try:
        infra = session.query(Infrastructure).filter_by(infrastructure_id=infra_id).first()
        if infra:
            infra.resource_name = name
            infra.infrastructure_category = category
            infra.resource_type = type
            infra.quantity = quantity
            session.commit()
    except Exception as e:
        session.rollback()
    finally:
        session.close()
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)

@dashboard_router.post("/api/employees/add")
async def add_employee(request: Request, name: str = Form(...), designation: str = Form(...), email: str = Form(...), skill_name: str = Form(...)):
    verify_manager(request)
    session = SessionLocal()
    try:
        # 1. Add Employee
        new_emp = Employee(
            department_id=1, # Default department
            employee_name=name,
            designation=designation,
            email=email,
            years_of_experience=3,
            employment_type="Full-Time"
        )
        session.add(new_emp)
        session.commit()
        session.refresh(new_emp)

        # 2. Check/Add Skills
        skill_names = [s.strip() for s in skill_name.split(",") if s.strip()]
        for s_name in skill_names:
            skill = session.query(Skill).filter_by(skill_name=s_name).first()
            if not skill:
                skill = Skill(skill_name=s_name, skill_category="Engineering")
                session.add(skill)
                session.commit()
                session.refresh(skill)

            # 3. Add EmployeeSkill
            emp_skill = EmployeeSkill(
                employee_id=new_emp.employee_id,
                skill_id=skill.skill_id,
                proficiency_level=85
            )
            session.add(emp_skill)
        
        session.commit()

        # 4. Add EmployeeAvailability
        emp_avail = EmployeeAvailability(
            employee_id=new_emp.employee_id,
            availability_status=AvailabilityStatus.AVAILABLE,
            available_hours_per_week=40,
            current_project=None
        )
        session.add(emp_avail)
        session.commit()

    except Exception as e:
        print(f"ERROR ADDING EMPLOYEE: {e}")
        session.rollback()
    finally:
        session.close()
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)

@dashboard_router.post("/api/pipeline/rerun/{qualification_id}")
async def rerun_pipeline(request: Request, qualification_id: int, background_tasks: BackgroundTasks):
    verify_manager(request)
    session = SessionLocal()
    try:
        qual = session.query(ProjectQualification).filter_by(qualification_id=qualification_id).first()
        if not qual:
            raise HTTPException(status_code=404, detail="Qualification not found")
        
        # We need client_id and project_name to run pipeline
        client_id = qual.client_id
        project_name = qual.project_name
        
        # Reset decision
        qual.final_decision = "Re-evaluating..."
        session.commit()
        
        pipeline_controller = AnalysisPipelineController()
        background_tasks.add_task(pipeline_controller.run_pipeline, client_id, project_name)
    finally:
        session.close()
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
