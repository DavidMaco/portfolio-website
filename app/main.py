"""
FastAPI development server — serves the portfolio locally with live reload.
Run:  uvicorn app.main:app --reload --port 8000
"""
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.data import load_projects, get_project

ROOT = Path(__file__).resolve().parent.parent

app = FastAPI(title="David Igbonaju Portfolio")

# Static assets
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")

# Jinja2 templates
templates = Jinja2Templates(directory=ROOT / "app" / "templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    projects = load_projects()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "projects": projects, "base": "/"},
    )


@app.get("/projects/{project_id}", response_class=HTMLResponse)
async def project_detail(request: Request, project_id: str):
    project = get_project(project_id)
    if project is None:
        return HTMLResponse("<h1>404 — Project not found</h1>", status_code=404)
    return templates.TemplateResponse(
        "project.html",
        {"request": request, "project": project, "base": "/"},
    )
