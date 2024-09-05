from fastapi import FastAPI, BackgroundTasks, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

import schemas
import crud
from database import get_db

from fastapi.templating import Jinja2Templates

app = FastAPI()

#set up for jinja templates
templates = Jinja2Templates(directory="templates")

@app.get('/index', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request":request })



#enable CORS

@app.post('/translate', response_model=schemas.TaskResponse)
def translate(request: schemas.TranslationRequest):
    #create a new translation task

    task = crud.create_translation_task(db, request.text, request.languages)

    background_tasks.add_task(perform_translation, task.id, request.text, request.languages, get_db.db)
    return {"task_id": {task.id}}