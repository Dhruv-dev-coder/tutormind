from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, student
from app.api import planner, teaching, quiz, rag
from app.api import classroom, notes, roadmap
from app.api import notifications, analytics, mcp, onboarding

app = FastAPI(title="TutorMind API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Basic security headers middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    # Minimal CSP - adapt in production
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['Strict-Transport-Security'] = 'max-age=63072000; includeSubDomains; preload'
    return response

# NOTE: Add a rate-limiting middleware or a gateway-based WAF in production.

app.include_router(auth.router, prefix="/api/auth")
app.include_router(student.router, prefix="/api/students")
app.include_router(planner.router, prefix="/api/planner")
app.include_router(teaching.router, prefix="/api/teaching")
app.include_router(classroom.router, prefix="/api/classroom")
app.include_router(quiz.router, prefix="/api/quiz")
app.include_router(notes.router, prefix="/api/notes")
app.include_router(roadmap.router, prefix="/api/roadmap")
app.include_router(rag.router, prefix="/api/rag")
app.include_router(notifications.router, prefix="/api/notifications")
app.include_router(analytics.router, prefix="/api/analytics")
app.include_router(onboarding.router, prefix="/api/onboarding")
app.include_router(mcp.router, prefix="/api")

@app.get("/api/health")
def health():
    return {"status":"ok"}
