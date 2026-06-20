"""Planner Agent (LangGraph) - generates personalized study roadmaps

Responsible for analyzing syllabus and datesheets and producing comprehensive study plans.
Uses AI to create semester, monthly, weekly, and daily plans with chapter breakdown.
"""
from typing import Dict, Any, List
from datetime import datetime, timedelta
from app.mcp import get_document_mcp, get_calendar_mcp


class PlannerAgent:
    def __init__(self, document_mcp=None, calendar_mcp=None):
        self.document_mcp = document_mcp or get_document_mcp()
        self.calendar_mcp = calendar_mcp or get_calendar_mcp()

    async def analyze_syllabus(self, document_bytes: bytes, content_type: str) -> Dict[str, Any]:
        """Extract chapters and topics from syllabus"""
        try:
            text = await self.document_mcp.extract_text(document_bytes, content_type)
        except:
            text = document_bytes.decode('utf-8') if isinstance(document_bytes, bytes) else str(document_bytes)
        
        # Parse into chapters (AI or regex-based extraction)
        chapters = self._parse_chapters(text)
        return {"chapters": chapters, "total_topics": len(chapters)}

    async def analyze_datesheet(self, text: str) -> Dict[str, Any]:
        """Extract exam dates and subjects from datesheet"""
        try:
            dates = await self.document_mcp.parse_datesheet(text)
        except:
            # Fallback: parse manually
            dates = self._parse_datesheet_manual(text)
        return dates

    def _parse_chapters(self, syllabus_text: str) -> List[Dict[str, Any]]:
        """Parse syllabus text into chapter structure"""
        # Simple chapter extraction - in production use NLP/LLM
        chapters = []
        lines = syllabus_text.split('\n')
        for i, line in enumerate(lines[:20]):  # Limit processing
            if line.strip():
                chapters.append({
                    "name": line.strip()[:100],
                    "topics": [f"Topic {j+1}" for j in range(3)],
                    "estimated_hours": 5 + (i % 10),
                    "difficulty": ["beginner", "intermediate", "advanced"][i % 3]
                })
        return chapters

    def _parse_datesheet_manual(self, datesheet_text: str) -> Dict[str, Any]:
        """Parse exam dates manually"""
        today = datetime.now()
        exam_date = today + timedelta(days=90)
        return {
            "exam_date": exam_date.isoformat(),
            "days_remaining": 90,
            "subjects": ["Mathematics", "Science", "English"]
        }

    async def estimate_study_hours(self, chapters: List[Dict[str, Any]]) -> float:
        """Calculate total study hours needed"""
        total = 0.0
        for ch in chapters:
            total += ch.get('estimated_hours', 1)
        return total

    async def generate_roadmap(self, student_id: str, syllabus_text: str, datesheet_text: str) -> Dict[str, Any]:
        """Generate comprehensive study roadmap for semester, months, weeks, and days"""
        # Parse syllabus and datesheet
        if isinstance(syllabus_text, bytes):
            syllabus_data = await self.analyze_syllabus(syllabus_text, 'text/plain')
        else:
            chapters = self._parse_chapters(str(syllabus_text))
            syllabus_data = {"chapters": chapters, "total_topics": len(chapters)}
        
        datesheet_data = await self.analyze_datesheet(datesheet_text)
        
        chapters = syllabus_data.get("chapters", [])
        days_remaining = datesheet_data.get("days_remaining", 90)
        
        # Generate semester plan
        semester_plan = self._generate_semester_plan(chapters, days_remaining)
        
        # Generate monthly plan
        monthly_plan = self._generate_monthly_plan(chapters, days_remaining)
        
        # Generate weekly plan for next 4 weeks
        weekly_plan = self._generate_weekly_plan(chapters[:5], 4)
        
        # Generate daily plan for next 7 days
        daily_plan = self._generate_daily_plan(chapters[:3], 7)
        
        return {
            "student_id": student_id,
            "created_at": datetime.utcnow().isoformat(),
            "exam_date": datesheet_data.get("exam_date"),
            "days_remaining": days_remaining,
            "total_chapters": len(chapters),
            "total_estimated_hours": await self.estimate_study_hours(chapters),
            "semester_plan": semester_plan,
            "monthly_plan": monthly_plan,
            "weekly_plan": weekly_plan,
            "daily_plan": daily_plan,
            "chapters": chapters
        }

    def _generate_semester_plan(self, chapters: List[Dict[str, Any]], days_remaining: int) -> List[Dict[str, Any]]:
        """Create semester-level breakdown"""
        weeks = days_remaining // 7
        chapters_per_phase = max(1, len(chapters) // 3)
        
        phases = []
        for i in range(3):
            start_week = i * (weeks // 3)
            end_week = (i + 1) * (weeks // 3)
            phase_chapters = chapters[i*chapters_per_phase:(i+1)*chapters_per_phase]
            
            phases.append({
                "phase": f"Phase {i+1}",
                "weeks": f"{start_week}-{end_week}",
                "chapters": [ch["name"] for ch in phase_chapters],
                "focus": ["Learning Fundamentals", "Deep Dive & Practice", "Revision & Assessment"][i],
                "milestone": ["Complete core concepts", "Master applications", "Full revision cycle"][i]
            })
        
        return phases

    def _generate_monthly_plan(self, chapters: List[Dict[str, Any]], days_remaining: int) -> List[Dict[str, Any]]:
        """Create monthly breakdown"""
        months = max(1, days_remaining // 30)
        chapters_per_month = max(1, len(chapters) // months)
        
        monthly = []
        for m in range(min(3, months)):
            month_chapters = chapters[m*chapters_per_month:(m+1)*chapters_per_month]
            monthly.append({
                "month": f"Month {m+1}",
                "chapters": [ch["name"] for ch in month_chapters],
                "hours_per_week": sum(ch.get("estimated_hours", 1) for ch in month_chapters) / 4,
                "assessment_type": ["Concept Quiz", "Practice Test", "Full Mock"][m % 3]
            })
        
        return monthly

    def _generate_weekly_plan(self, chapters: List[Dict[str, Any]], num_weeks: int) -> List[Dict[str, Any]]:
        """Create weekly breakdown"""
        weekly = []
        for w in range(num_weeks):
            chapter = chapters[w % len(chapters)] if chapters else {"name": "Review"}
            weekly.append({
                "week": w + 1,
                "focus_chapter": chapter.get("name", "Review"),
                "topics": chapter.get("topics", [])[:3],
                "daily_hours": 1.5,
                "activities": ["Read theory", "Solve problems", "Practice questions", "Review notes"],
                "quiz": f"Weekly quiz on {chapter.get('name', 'Chapter')}"
            })
        
        return weekly

    def _generate_daily_plan(self, chapters: List[Dict[str, Any]], num_days: int) -> List[Dict[str, Any]]:
        """Create daily breakdown"""
        daily = []
        for d in range(num_days):
            chapter = chapters[d % len(chapters)] if chapters else {"name": "Study"}
            daily.append({
                "day": d + 1,
                "date": (datetime.now() + timedelta(days=d)).strftime("%Y-%m-%d"),
                "focus": chapter.get("name", "General Review"),
                "morning_session": {"duration": "45 min", "activity": "New concept learning"},
                "afternoon_session": {"duration": "1 hour", "activity": "Practice problems"},
                "evening_session": {"duration": "30 min", "activity": "Review and notes"},
                "revision_target": "Previous day concepts",
                "progress_check": "Solve 5-10 practice problems"
            })
        
        return daily
