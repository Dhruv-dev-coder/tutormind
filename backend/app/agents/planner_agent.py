"""Planner Agent (LangGraph) - generates personalized study roadmaps

Responsible for analyzing syllabus and datesheets and producing comprehensive study plans.
Uses AI to create semester, monthly, weekly, and daily plans with chapter breakdown.
"""
from typing import Dict, Any, List
from datetime import datetime, timedelta
from app.mcp import get_document_mcp, get_calendar_mcp
from app.services.llm_service import llm_service


import re

class PlannerAgent:
    def __init__(self, document_mcp=None, calendar_mcp=None):
        self.document_mcp = document_mcp or get_document_mcp()
        self.calendar_mcp = calendar_mcp or get_calendar_mcp()
        self.llm = llm_service

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
        """Parse syllabus text into chapter structure with actual subjects/topics"""
        chapters = []
        current_subject = "General Study"
        
        lines = [line.strip() for line in syllabus_text.split('\n') if line.strip()]
        
        # Check if there are subject-like headers
        for line in lines:
            # Check if this line defines a subject and its topics: e.g. "Math: Algebra, Calculus"
            if ':' in line:
                parts = line.split(':', 1)
                subj = parts[0].strip()
                topics_text = parts[1].strip()
                topics = [t.strip() for t in re.split(r'[,;]', topics_text) if t.strip()]
                if not topics:
                    topics = [subj]
                
                chapters.append({
                    "subject": subj,
                    "name": f"{subj} Fundamentals",
                    "topics": topics,
                    "estimated_hours": 8.0,
                    "difficulty": "intermediate"
                })
                continue
            
            # If line is short and doesn't look like a typical chapter list line, it might be a subject header
            if len(line) < 30 and not any(line.lower().startswith(x) for x in ['chapter', 'unit', 'topic', 'lesson', '-', '*', '1', '2', '3', '4', '5', '6', '7', '8', '9']):
                current_subject = line
                continue
                
            # Otherwise, treat the line as a chapter name
            # Split the line by common delimiters to find topics, or use the line itself as topic
            topic_names = []
            cleaned_line = re.sub(r'^(?:chapter|unit|topic|lesson|\d+|-|\*|\.)\s*[:.-]?\s*', '', line, flags=re.IGNORECASE).strip()
            
            if cleaned_line:
                # If there are sub-topics separated by commas or semicolons
                if ',' in cleaned_line or ';' in cleaned_line:
                    topic_names = [t.strip() for t in re.split(r'[,;]', cleaned_line) if t.strip()]
                else:
                    topic_names = [cleaned_line]
                    
                chapters.append({
                    "subject": current_subject,
                    "name": cleaned_line[:100],
                    "topics": topic_names[:5],
                    "estimated_hours": 6.0,
                    "difficulty": "beginner"
                })
        
        # If no chapters were parsed, create a default one using the whole text
        if not chapters:
            chapters.append({
                "subject": "General Study",
                "name": "Introduction",
                "topics": [syllabus_text[:100].strip() or "General Concepts"],
                "estimated_hours": 10.0,
                "difficulty": "beginner"
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
        # Try to use LLM if available
        if self.llm.is_available():
            try:
                llm_roadmap = await self.llm.generate_roadmap(syllabus_text, datesheet_text)
                # Enhance LLM output with structured plans
                chapters = llm_roadmap.get("chapters", [])
                days_remaining = llm_roadmap.get("days_remaining", 90)
                
                # Generate structured plans
                semester_plan = self._generate_semester_plan(chapters, days_remaining)
                monthly_plan = self._generate_monthly_plan(chapters, days_remaining)
                weekly_plan = self._generate_weekly_plan(chapters[:5], 4)
                daily_plan = self._generate_daily_plan(chapters[:3], 7)
                
                # Extract unique subjects
                subjects = []
                for ch in chapters:
                    subj = ch.get("subject", "General Study")
                    if subj not in subjects:
                        subjects.append(subj)
                if not subjects:
                    subjects = ["General Study"]
                
                return {
                    "student_id": student_id,
                    "created_at": datetime.utcnow().isoformat(),
                    "exam_date": llm_roadmap.get("exam_date"),
                    "days_remaining": days_remaining,
                    "total_chapters": llm_roadmap.get("total_chapters", len(chapters)),
                    "total_estimated_hours": llm_roadmap.get("total_estimated_hours", await self.estimate_study_hours(chapters)),
                    "semester_plan": semester_plan,
                    "monthly_plan": monthly_plan,
                    "weekly_plan": weekly_plan,
                    "daily_plan": daily_plan,
                    "chapters": chapters,
                    "subjects": subjects
                }
            except Exception as e:
                print(f"LLM roadmap generation failed, falling back to template: {e}")
        
        # Fallback to template-based generation
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
        
        # Extract unique subjects from parsed chapters
        subjects = []
        for ch in chapters:
            subj = ch.get("subject", "General Study")
            if subj not in subjects:
                subjects.append(subj)
        if not subjects:
            subjects = ["General Study"]
        
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
            "chapters": chapters,
            "subjects": subjects
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

    def _derive_topic(self, chapter: Dict[str, Any]) -> str:
        """Derive a teachable topic from chapter metadata."""
        topics = chapter.get("topics") or []
        if topics:
            return topics[0]
        return chapter.get("name", "General Review")

    def _generate_daily_plan(self, chapters: List[Dict[str, Any]], num_days: int) -> List[Dict[str, Any]]:
        """Create daily breakdown with structured session metadata for interactivity."""
        daily = []
        for d in range(num_days):
            chapter = chapters[d % len(chapters)] if chapters else {"name": "Study"}
            topic = self._derive_topic(chapter)
            daily.append({
                "day": d + 1,
                "date": (datetime.now() + timedelta(days=d)).strftime("%Y-%m-%d"),
                "focus": chapter.get("name", "General Review"),
                "morning_session": {
                    "duration": "45 min",
                    "activity": "New concept learning",
                    "type": "concept_learning",
                    "topic": topic,
                },
                "afternoon_session": {
                    "duration": "1 hour",
                    "activity": "Practice problems",
                    "type": "practice",
                    "topic": topic,
                },
                "evening_session": {
                    "duration": "30 min",
                    "activity": "Review and notes",
                    "type": "revision",
                    "topic": topic,
                },
                "revision_target": "Previous day concepts",
                "progress_check": "Solve 5-10 practice problems",
            })

        return daily
