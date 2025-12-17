from fastapi import APIRouter, Depends, Form, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

templates = Jinja2Templates(directory="app/templates")


# ---------- API: CREATE USER ----------
@router.post("/api")
def create_user_api(
    name: str,
    fingerprint_id: int,
    access_level: int = 1,
    db: Session = Depends(get_db)
):
    existing = db.query(User).filter(
        User.fingerprint_id == fingerprint_id
    ).first()

    if existing:
        return {
            "status": "error",
            "message": "Fingerprint ID already exists"
        }

    user = User(
        name=name,
        fingerprint_id=fingerprint_id,
        access_level=access_level
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "status": "success",
        "user_id": user.id
    }


# ---------- ADMIN PAGE ----------
@router.get("/admin", name="admin_users")
def admin_users(
    request: Request,
    db: Session = Depends(get_db)
):
    users = db.query(User).order_by(User.id).all()

    return templates.TemplateResponse(
        "admin_users.html",
        {
            "request": request,
            "users": users
        }
    )


@router.post("/admin", name="admin_users_create")
def admin_users_create(
    request: Request,
    name: str = Form(...),
    fingerprint_id: int = Form(...),
    access_level: int = Form(1),
    db: Session = Depends(get_db)
):
    existing = db.query(User).filter(
        User.fingerprint_id == fingerprint_id
    ).first()

    if existing:
        users = db.query(User).all()
        return templates.TemplateResponse(
            "admin_users.html",
            {
                "request": request,
                "users": users,
                "error": "Fingerprint ID findes allerede"
            }
        )

    user = User(
        name=name,
        fingerprint_id=fingerprint_id,
        access_level=access_level
    )

    db.add(user)
    db.commit()

    users = db.query(User).all()
    return templates.TemplateResponse(
        "admin_users.html",
        {
            "request": request,
            "users": users,
            "success": "Bruger oprettet"
        }
    )
