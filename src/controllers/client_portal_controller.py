import os
from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import bcrypt
from sqlalchemy.exc import IntegrityError

from src.database.session import SessionLocal
from src.entities.client import Client
from src.entities.project_qualification import ProjectQualification

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

portal_router = APIRouter(prefix="/portal", tags=["Client Portal"])

# --- Security Helpers ---
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )

def get_password_hash(password):
    return bcrypt.hashpw(
        password.encode('utf-8'), 
        bcrypt.gensalt()
    ).decode('utf-8')

def get_current_client(request: Request):
    client_id = request.cookies.get("client_auth")
    if not client_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return int(client_id)

# --- Authentication Routes ---

@portal_router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="client_login.html", context={"request": request})

@portal_router.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    session = SessionLocal()
    try:
        client = session.query(Client).filter(Client.username == username).first()
        if not client or not verify_password(password, client.password_hash):
            return templates.TemplateResponse(request=request, name="client_login.html", context={
                "request": request,
                "error": "Invalid username or password"
            })
            
        response = RedirectResponse(url="/portal/dashboard", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="client_auth", value=str(client.client_id), httponly=True)
        return response
    finally:
        session.close()

@portal_router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse(request=request, name="client_signup.html", context={"request": request})

@portal_router.post("/signup")
async def signup(
    request: Request,
    client_name: str = Form(...),
    company_name: str = Form(...),
    contact_person: str = Form(...),
    email: str = Form(...),
    phone_number: str = Form(...),
    country_name: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
):
    if password != confirm_password:
        return templates.TemplateResponse(request=request, name="client_signup.html", context={
            "request": request,
            "error": "Passwords do not match."
        })
        
    session = SessionLocal()
    try:
        # Check duplicate username
        existing_user = session.query(Client).filter(Client.username == username).first()
        if existing_user:
            return templates.TemplateResponse(request=request, name="client_signup.html", context={
                "request": request,
                "error": "Username already exists. Please select another username."
            })
            
        # Check duplicate email
        existing_email = session.query(Client).filter(Client.email == email).first()
        if existing_email:
            return templates.TemplateResponse(request=request, name="client_signup.html", context={
                "request": request,
                "error": "Email is already registered."
            })
            
        hashed_password = get_password_hash(password)
        new_client = Client(
            company_name=company_name,
            contact_person=contact_person,
            email=email,
            phone_number=phone_number,
            country_name=country_name,
            username=username,
            password_hash=hashed_password
        )
        
        session.add(new_client)
        session.commit()
        session.refresh(new_client)
        
        # Log them in automatically after signup
        response = RedirectResponse(url="/portal/dashboard", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="client_auth", value=str(new_client.client_id), httponly=True)
        return response
        
    except Exception as e:
        session.rollback()
        return templates.TemplateResponse(request=request, name="client_signup.html", context={
            "request": request,
            "error": f"An error occurred: {str(e)}"
        })
    finally:
        session.close()

@portal_router.get("/logout")
async def logout():
    response = RedirectResponse(url="/portal/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("client_auth")
    return response

# --- Protected Dashboard Route ---

@portal_router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    try:
        client_id = get_current_client(request)
    except HTTPException:
        return RedirectResponse(url="/portal/login", status_code=status.HTTP_302_FOUND)
        
    session = SessionLocal()
    try:
        client = session.query(Client).filter(Client.client_id == client_id).first()
        
        # Fetch their projects
        qualifications = session.query(ProjectQualification).filter(
            ProjectQualification.client_id == client_id
        ).all()
        
        return templates.TemplateResponse(request=request, name="client_dashboard.html", context={
            "request": request,
            "client": client,
            "qualifications": qualifications
        })
    finally:
        session.close()
