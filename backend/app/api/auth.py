from fastapi import APIRouter, HTTPException
from fastapi import Depends
from app.schemas.auth import TokenVerifyRequest, TokenVerifyResponse
from app.services.firebase import verify_id_token, initialize_firebase
from app.database import db
from datetime import datetime

router = APIRouter()


@router.get('/status')
def status():
    return {"auth": "ready"}


@router.post('/verify', response_model=TokenVerifyResponse)
async def verify_token(payload: TokenVerifyRequest):
    print(f"Received verify request with token length: {len(payload.id_token) if payload.id_token else 0}")
    
    try:
        decoded = verify_id_token(payload.id_token)
    except Exception as e:
        print(f"Token verification error: {e}")
        raise HTTPException(status_code=401, detail=f'Token verification failed: {str(e)}')
    
    if not decoded:
        print("Token verification returned None")
        raise HTTPException(status_code=401, detail='Invalid or missing Firebase token')

    uid = decoded.get('uid')
    email = decoded.get('email')
    name = decoded.get('name') or decoded.get('displayName')
    
    print(f"Decoded token - uid: {uid}, email: {email}")

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
        print(f"Created new student with id: {student_id}")
    else:
        student_id = str(existing.get('_id'))
        is_first_time = not existing.get("onboarded", False)
        print(f"Found existing student with id: {student_id}, onboarded: {existing.get('onboarded', False)}")

    return TokenVerifyResponse(
    uid=uid,
    email=email,
    name=name,
    firebase_claims=decoded,
    is_first_time=is_first_time,
    student_id=student_id,
    onboarded=(existing.get("onboarded", False) if existing else False)
)
