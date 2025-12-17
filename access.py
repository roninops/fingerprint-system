from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, AccessLog

router = APIRouter(
    prefix="/access",
    tags=["Access"]
)


LAST_AUTH_USER_ID = None



@router.get("/{fingerprint_id}")
def check_access(
    fingerprint_id: int,
    db: Session = Depends(get_db)
):
    global LAST_AUTH_USER_ID

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

        return {
            "access": "denied"
        }

 
    log = AccessLog(
        user_id=user.id,
        fingerprint_id=fingerprint_id,
        granted=1
    )
    db.add(log)
    db.commit()


    LAST_AUTH_USER_ID = user.id

    return {
        "access": "granted",
        "user_id": user.id,
        "user_name": user.name,
        "access_level": user.access_level
    }



@router.get("/auth/status")
def auth_status(db: Session = Depends(get_db)):
    if LAST_AUTH_USER_ID is None:
        return {
            "authenticated": False
        }

    user = db.query(User).filter(
        User.id == LAST_AUTH_USER_ID
    ).first()

    if not user:
        return {
            "authenticated": False
        }

    return {
        "authenticated": True,
        "user_id": user.id,
        "user_name": user.name
    }



@router.post("/auth/reset")
def auth_reset():
    global LAST_AUTH_USER_ID
    LAST_AUTH_USER_ID = None
    return {"status": "reset"}
