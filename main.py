from fastapi import FastAPI, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.database import engine, get_db
from app import models
from app.routers import access, journal

# ---------- DATABASE ----------
models.Base.metadata.create_all(bind=engine)

# ---------- APP ----------
app = FastAPI(title="Fingerprint Access System")

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ---------- ROUTERS ----------
app.include_router(access.router)
app.include_router(journal.router)

# ---------- HOME ----------
@app.get("/", name="home")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

# ---------- LOGIN ----------
@app.get("/login", name="login")
def login_page(request: Request):
    return templates.TemplateResponse(
        "Login.html",
        {"request": request}
    )

@app.post("/login", name="login_post")
def login_post(
    request: Request,
    fingerprint_id: int = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(
        models.User.fingerprint_id == fingerprint_id
    ).first()

    if not user:
        return templates.TemplateResponse(
            "Login.html",
            {
                "request": request,
                "error": "Ugyldigt fingeraftryk"
            }
        )

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": user
        }
    )

from fastapi import Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

@app.get("/dashboard", name="dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )
