from fastapi import FastAPI, BackgroundTasks, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

import schemas
from sqlalchemy.orm import Session 
import crud
import models
from database import get_db, engine, SessionLocal
from utily import perform_translation
from typing import List
import uuid
from fastapi.staticfiles import StaticFiles

from fastapi.templating import Jinja2Templates

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


#set up for jinja templates
templates = Jinja2Templates(directory="templates")


@app.get('/', response_class=HTMLResponse)
@app.get('/index', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request":request })




@app.post('/translate', response_model=schemas.TaskResponse)
def translate(request: schemas.TranslationRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    #create a new translation task

    task = crud.create_translation_task(db, request.text, request.languages)

    background_tasks.add_task(perform_translation, task.id, request.text, request.languages, db)
    return {"task_id": task.id}


@app.get("/translate/{task_id}", response_model=schemas.TranslationStatus)
def get_translation(task_id: int, db: Session = Depends(get_db)):
    

    task = crud.get_translation_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"task_id": task.id, "status": task.status, "translations": task.translations}


@app.get("/translate/content/{task_id}")
def get_translate_content(task_id: int, db: Session = Depends(get_db)):
    

    task = crud.get_translation_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    
    return task