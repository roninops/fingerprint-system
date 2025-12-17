from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, AccessLog

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/fingerprint")
def fingerprint_login(fingerprint_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(
        User.fingerprint_id == fingerprint_id
    ).first()

    if not user:
        log = AccessLog(
            user_id=None,
            fingerprint_id=fingerprint_id,
            granted=0
        )
        db.add(log)
        db.commit()

        raise HTTPException(status_code=401, detail="Fingerprint not recognized")

    log = AccessLog(
        user_id=user.id,
        fingerprint_id=fingerprint_id,
        granted=1
    )
    db.add(log)
    db.commit()

    return {
        "login": "success",
        "user_id": user.id,
        "name": user.name,
        "access_level": user.access_level
    }
