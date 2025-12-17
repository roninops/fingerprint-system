from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Journal

router = APIRouter(
    prefix="/journal",
    tags=["Journal"]
)

templates = Jinja2Templates(directory="app/templates")


# ---------- VIEW JOURNAL ----------
@router.get("/{user_id}", name="journal_view")
def view_journal(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    journal = db.query(Journal).filter(Journal.user_id == user_id).first()

    if not user:
        return {"error": "User not found"}

    return templates.TemplateResponse(
        "journal.html",
        {
            "request": request,
            "user": user,
            "journal": journal
        }
    )


# ---------- SAVE / UPDATE JOURNAL ----------
@router.post("/{user_id}", name="journal_save")
def save_journal(
    user_id: int,
    birthday: str = Form(""),
    blood_type: str = Form(""),
    allergies: str = Form(""),
    medications: str = Form(""),
    conditions: str = Form(""),
    db: Session = Depends(get_db)
):
    journal = db.query(Journal).filter(
        Journal.user_id == user_id
    ).first()

    if journal:
        journal.birthday = birthday or None
        journal.blood_type = blood_type
        journal.allergies = allergies
        journal.medications = medications
        journal.conditions = conditions
    else:
        journal = Journal(
            user_id=user_id,
            birthday=birthday or None,
            blood_type=blood_type,
            allergies=allergies,
            medications=medications,
            conditions=conditions
        )
        db.add(journal)

    db.commit()

    return RedirectResponse(
        url=f"/journal/{user_id}",
        status_code=302
    )
