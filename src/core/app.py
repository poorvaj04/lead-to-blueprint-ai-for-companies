import os
from fastapi import FastAPI, Request, File, UploadFile, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# Ensure we have the right paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

app = FastAPI(title="AI Project Analyst")

# Create static directory if it doesn't exist
os.makedirs(os.path.join(BASE_DIR, "static"), exist_ok=True)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"
    project_name: str = "Default Project"

# We will instantiate the WebInterviewController later
from src.controllers.web_interview_controller import WebInterviewController
controller = WebInterviewController()

from src.controllers.dashboard_controller import dashboard_router
from src.controllers.client_portal_controller import portal_router

app.include_router(dashboard_router)
app.include_router(portal_router)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return RedirectResponse(url="/portal/login", status_code=302)

@app.get("/portal/chat", response_class=HTMLResponse)
async def chat_ui(request: Request):
    from src.controllers.client_portal_controller import get_current_client
    try:
        get_current_client(request)
    except Exception:
        return RedirectResponse(url="/portal/login", status_code=302)
    return templates.TemplateResponse(request=request, name="index.html", context={"request": request})

@app.post("/api/chat")
async def chat(request: ChatRequest, req: Request, background_tasks: BackgroundTasks):
    from src.controllers.client_portal_controller import get_current_client
    from src.controllers.analysis_pipeline_controller import AnalysisPipelineController
    try:
        client_id = get_current_client(req)
    except Exception:
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})
        
    # Pass to the controller logic
    response = controller.process_message(request.message, request.session_id, client_id, request.project_name)
    
    # If the interview just completed, trigger the Phase 2 Pipeline
    if response.get("completed"):
        pipeline_controller = AnalysisPipelineController()
        background_tasks.add_task(pipeline_controller.run_pipeline, client_id, request.project_name)
        
    return JSONResponse(content=response)

@app.post("/api/voice")
async def voice(req: Request, background_tasks: BackgroundTasks, file: UploadFile = File(...), session_id: str = "default", project_name: str = "Default Project"):
    from src.controllers.client_portal_controller import get_current_client
    from src.controllers.analysis_pipeline_controller import AnalysisPipelineController
    try:
        client_id = get_current_client(req)
    except Exception:
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})
        
    # Save the file temporarily
    temp_path = f"temp_{session_id}.wav"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
        
    # Transcribe using speech-to-text service
    from src.services.speech_to_text_service import SpeechToTextService
    stt = SpeechToTextService()
    speech_result = stt.transcribe(temp_path)
    transcript = speech_result.transcript
    
    if os.path.exists(temp_path):
        os.remove(temp_path)
        
    # Process transcript
    response = controller.process_message(transcript, session_id, client_id, project_name)
    
    # If the interview just completed, trigger the Phase 2 Pipeline
    if response.get("completed"):
        pipeline_controller = AnalysisPipelineController()
        background_tasks.add_task(pipeline_controller.run_pipeline, client_id, project_name)
        
    # Include the transcript in the response so UI knows what was heard
    response["client_transcript"] = transcript
    return JSONResponse(content=response)

# To run: uvicorn src.core.app:app --reload
