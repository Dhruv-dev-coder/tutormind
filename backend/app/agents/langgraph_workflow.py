"""LangGraph workflow orchestrator

This module orchestrates the agents for generating personalized learning plans.
"""
from app.agents.planner_agent import PlannerAgent
from app.agents.teaching_agent import TeachingAgent
from app.agents.assessment_agent import AssessmentAgent
from app.agents.progress_agent import ProgressAgent
from app.agents.revision_agent import RevisionAgent
from app.agents.exam_agent import ExamAgent
from app.agents.mentor_agent import MentorAgent


class LangGraphWorkflow:
    def __init__(self):
        self.planner = PlannerAgent()
        self.teaching = TeachingAgent()
        self.assessment = AssessmentAgent()
        self.progress = ProgressAgent()
        self.revision = RevisionAgent()
        self.exam = ExamAgent()
        self.mentor = MentorAgent()

    async def run_planner_flow(self, student_id: str, syllabus_data, content_type: str, datesheet_text: str):
        """Generate study roadmap from syllabus and datesheet"""
        # Handle both bytes and string input
        if isinstance(syllabus_data, bytes):
            syllabus_text = syllabus_data.decode('utf-8')
        else:
            syllabus_text = str(syllabus_data)
        
        roadmap = await self.planner.generate_roadmap(student_id, syllabus_text, datesheet_text)
        return roadmap
    
    async def run_teaching_flow(self, student_id: str, topic: str, level: str = 'beginner', roadmap = None):
        """Generate teaching content for a topic"""
        lesson = await self.teaching.teach_concept(student_id, topic, level, roadmap)
        return lesson
    
    async def run_assessment_flow(self, student_id: str, subject: str, difficulty: str = 'medium', roadmap = None):
        """Generate quiz for assessment"""
        quiz = await self.assessment.generate_quiz(student_id, subject, difficulty, roadmap)
        return quiz

    async def run_progress_flow(self, student_id: str, event):
        """Update progress from a learning event"""
        return await self.progress.update_progress(student_id, event)

    async def run_revision_flow(self, student_id: str, topic: str, start_date: str = None):
        """Create spaced revision schedule for a topic"""
        return await self.revision.create_spaced_revision_plan(student_id, topic, start_date)

    async def run_exam_flow(self, student_id: str, subject: str, mode: str = "30_days"):
        """Generate a mock test plan for exam preparation"""
        return await self.exam.generate_mock_test(student_id, subject, mode)

    async def run_mentor_flow(self, student_id: str, activity = None):
        """Monitor activity and trigger mentor interventions"""
        return await self.mentor.monitor_activity(student_id, activity)
