from fastapi import APIRouter, HTTPException
from fastapi import Depends
from app.schemas.auth import TokenVerifyRequest, TokenVerifyResponse
from app.services.firebase import verify_id_token, initialize_firebase
from app.database import db
from datetime import datetime

router = APIRouter()


@router.on_event("startup")
async def init_firebase():
    try:
        initialize_firebase()
    except Exception:
        # log initialization failure; continue so server stays up for development
        pass


@router.get('/status')
def status():
    return {"auth": "ready"}


@router.post('/verify', response_model=TokenVerifyResponse)
async def verify_token(payload: TokenVerifyRequest):
    decoded = verify_id_token(payload.id_token)
    if not decoded:
        raise HTTPException(status_code=401, detail='Invalid or missing Firebase token')

    uid = decoded.get('uid')
    email = decoded.get('email')
    name = decoded.get('name') or decoded.get('displayName')

    # Map or create a student record in MongoDB
    students = db['students']
    existing = await students.find_one({"firebase_uid": uid})
    
    is_first_time = False
    if not existing:
        # Create a minimal student mapping
        is_first_time = True
        doc = {
            "firebase_uid": uid,
            "email": email,
            "name": name,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "onboarded": False
        }
        res = await students.insert_one(doc)
        student_id = str(res.inserted_id)
    else:
        student_id = str(existing.get('_id'))
        is_first_time = not existing.get("onboarded", False)

    return TokenVerifyResponse(
    uid=uid,
    email=email,
    name=name,
    firebase_claims=decoded,
    is_first_time=is_first_time,
    student_id=student_id,
    onboarded=(existing.get("onboarded", False) if existing else False)
)
