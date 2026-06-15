# TutorMind – Autonomous AI Learning Platform

An intelligent learning platform that generates personalized study roadmaps and provides AI-powered teaching, assessments, and progress tracking.

## 🎯 Features

### AI-Powered Features
- **Personalized Roadmaps**: AI analyzes your syllabus and exam dates to generate optimized study plans (daily, weekly, monthly, semester)
- **AI Teaching Assistant**: Comprehensive lesson generation with explanations, examples, and adaptive difficulty levels
- **Smart Quizzes**: AI-generated assessments with multiple question types and detailed feedback
- **RAG Knowledge Base**: Ask questions about your study topics and get grounded, contextual answers
- **Progress Tracking**: Real-time monitoring of your learning progress with insights and recommendations

### Onboarding Flow
1. Sign up or log in
2. Provide your syllabus (copy-paste text)
3. Provide your exam schedule/datesheet
4. AI automatically generates your personalized roadmap
5. Start learning with AI guidance

## 🚀 Quick Start

### Prerequisites
- Node.js 16+
- Python 3.9+
- MongoDB (local or Atlas)
- Firebase project (for auth)

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create Python venv
python -m venv .venv

# Activate venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with:
FIREBASE_CREDENTIALS_PATH=path/to/serviceAccountKey.json
GOOGLE_API_KEY=your_gemini_api_key
DATABASE_URL=mongodb://localhost:27017/tutormind

# Run server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create .env file with:
VITE_FIREBASE_API_KEY=your_firebase_api_key
VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your_project_id
VITE_API_BASE_URL=http://localhost:8000/api

# Start dev server (runs on localhost:5173 or 5174)
npm run dev
```

## 📱 Pages & AI Integration

### Dashboard
- **AI Feature**: RAG-powered Q&A about study topics
- **Display**: Today's study plan from roadmap
- **Metrics**: Total chapters, study hours, days remaining, daily target hours

### Study Planner
- **AI Feature**: Auto-generated roadmaps with 4 view modes
- **Modes**: 
  - Semester: 3 phases with focus and milestones
  - Monthly: Detailed monthly breakdown
  - Weekly: 4-week preview with daily hours and quizzes
  - Daily: Hour-by-hour schedule with sessions
- **Action**: Regenerate roadmap with updated syllabus

### AI Classroom
- **AI Feature**: Concept teaching engine
- **Content**: 
  - Comprehensive explanations at multiple difficulty levels
  - Worked examples (3 per topic)
  - Key learning points
  - External resources (textbooks, courses, practice sites)
  - Practice exercises with hints

### Quiz Center
- **AI Feature**: Adaptive quiz generation
- **Types**: Multiple choice, True/False, Short answer, Essay
- **Feedback**: Detailed explanations, accuracy analysis, recommendations
- **Submission**: Submit answers and get evaluation with performance analysis

## 🤖 AI Agent Architecture

### Agents Implemented

1. **PlannerAgent** - Generates multi-level study roadmaps
   - Parses syllabus and datesheets
   - Calculates optimal study hours distribution
   - Creates semester/monthly/weekly/daily plans

2. **TeachingAgent** - Comprehensive concept instruction
   - Multi-level explanations (beginner/intermediate/advanced)
   - Generates worked examples
   - Finds external resources via MCP
   - Adaptive difficulty based on performance

3. **AssessmentAgent** - Quiz and assignment generation
   - Multiple question type support
   - Auto-grading and feedback
   - Performance analysis and recommendations

4. **ProgressAgent** (Skeleton) - Progress tracking
5. **RevisionAgent** (Skeleton) - Revision planning
6. **ExamAgent** (Skeleton) - Exam preparation
7. **MentorAgent** (Skeleton) - Personalized mentoring

### Backend API Endpoints

#### Auth
- `POST /api/auth/verify` - Firebase token verification with onboarding status

#### Onboarding
- `POST /api/onboarding/initialize` - Capture syllabus/datesheet and generate roadmap
- `GET /api/onboarding/status/{student_id}` - Check onboarding status
- `GET /api/onboarding/roadmap/{student_id}` - Retrieve student roadmap

#### AI Endpoints
- `POST /api/planner/generate_roadmap` - Generate personalized roadmap
- `POST /api/teaching/teach` - Get concept teaching content
- `POST /api/quiz/generate` - Generate quiz
- `POST /api/quiz/submit` - Submit answers and get evaluation
- `POST /api/rag/query` - Query knowledge base

#### MCP
- `GET /api/mcp/health/email` - Email MCP health check
- `POST /api/mcp/test/email` - Test email sending
- `POST /api/mcp/test/reminder_email` - Test reminder email

## 🗄️ Database Schema

### Students Collection
```javascript
{
  firebase_uid: String,
  email: String,
  name: String,
  onboarded: Boolean,
  onboarded_at: DateTime,
  roadmap: {
    total_chapters: Number,
    exam_date: String,
    days_remaining: Number,
    semester_plan: [...],
    monthly_plan: [...],
    weekly_plan: [...],
    daily_plan: [...]
  },
  created_at: DateTime,
  updated_at: DateTime
}
```

## 🔧 Tech Stack

### Frontend
- React 18
- Vite
- Tailwind CSS
- Firebase Auth
- React Router
- Axios

### Backend
- FastAPI (Python)
- Motor (async MongoDB)
- Firebase Admin SDK
- LangChain & LangGraph (AI orchestration)
- Google Generative AI (Gemini embeddings)
- Pydantic (validation)

### Infrastructure
- MongoDB Atlas (vector search ready)
- Docker & Docker Compose
- Firebase (authentication)

## 📊 Roadmap Example

When a student provides:
- **Syllabus**: "Chapter 1: Algebra Basics, Chapter 2: Equations, Chapter 3: Polynomials..."
- **Datesheet**: "Math exam on June 15 (90 days away)"

The AI generates:
```
Semester Plan:
  Phase 1 (Days 1-30): Learning Fundamentals
    - Algebra Basics, Equations
    - 5 hours/week
  Phase 2 (Days 31-60): Deep Dive & Practice
    - Polynomials, Advanced Topics
    - 6 hours/week
  Phase 3 (Days 61-90): Revision & Assessment
    - Full revision cycle
    - Mock tests

Daily Plan:
  Morning (45 min): New concept learning
  Afternoon (1 hour): Practice problems
  Evening (30 min): Review and notes
  
Quiz: Weekly assessment on learned topics
```

## 🔐 Security

- Firebase Authentication for user management
- JWT token verification on all protected routes
- CORS enabled for localhost development
- Security headers (HSTS, CSP, X-Frame-Options)
- MCP-first architecture for external integrations

## 📝 Environment Variables

### Backend (.env)
```
FIREBASE_CREDENTIALS_PATH=path/to/serviceAccountKey.json
GOOGLE_API_KEY=your_gemini_api_key
DATABASE_URL=mongodb://localhost:27017/tutormind
```

### Frontend (.env)
```
VITE_FIREBASE_API_KEY=
VITE_FIREBASE_AUTH_DOMAIN=
VITE_FIREBASE_PROJECT_ID=
VITE_API_BASE_URL=http://localhost:8000/api
```

## 🚢 Deployment

See `DEPLOYMENT.md` for production deployment instructions including:
- Docker containerization
- Docker Compose orchestration
- Environment configuration
- Monitoring and logging setup

## 📚 API Response Examples

### Generate Roadmap
```json
{
  "status": "ok",
  "roadmap": {
    "student_id": "user123",
    "total_chapters": 5,
    "days_remaining": 90,
    "semester_plan": [...],
    "daily_plan": [...]
  }
}
```

### Teach Concept
```json
{
  "status": "ok",
  "result": {
    "topic": "Newton's Laws",
    "level": "beginner",
    "explanation": {...},
    "examples": [...],
    "exercises": [...]
  }
}
```

### Generate Quiz
```json
{
  "status": "ok",
  "quiz": {
    "quiz_id": "quiz_123",
    "total_questions": 10,
    "questions": [...],
    "time_limit_minutes": 30
  }
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [LangChain Documentation](https://python.langchain.com/)
- [Firebase Documentation](https://firebase.google.com/docs)

---

**TutorMind** - Making personalized AI-powered education accessible to everyone

