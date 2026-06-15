"""Assessment Agent (LangGraph) - comprehensive quiz & assignment generation

Generates quizzes and assignments based on student roadmap and performance.
Provides detailed feedback and evaluates understanding.
"""
from typing import Dict, Any, List
from datetime import datetime
import json


class AssessmentAgent:
    def __init__(self):
        self.question_types = ["multiple_choice", "short_answer", "true_false", "essay"]

    async def generate_quiz(self, student_id: str, subject_id: str, difficulty: str = "medium", roadmap: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate a comprehensive quiz based on subject and difficulty"""
        questions = self._generate_questions(subject_id, difficulty, count=10)
        
        return {
            "quiz_id": f"quiz_{datetime.utcnow().timestamp()}",
            "student_id": student_id,
            "subject": subject_id,
            "difficulty": difficulty,
            "created_at": datetime.utcnow().isoformat(),
            "title": f"{subject_id} Assessment - {difficulty.capitalize()} Level",
            "description": f"This quiz tests your understanding of {subject_id} at {difficulty} level",
            "total_questions": len(questions),
            "total_marks": len(questions) * 10,
            "time_limit_minutes": 30,
            "passing_score": 60,
            "questions": questions,
            "instructions": [
                "Read each question carefully",
                "Attempt all questions",
                "Review your answers before submitting",
                "Do not navigate away during the quiz"
            ]
        }

    def _generate_questions(self, subject: str, difficulty: str, count: int = 10) -> List[Dict[str, Any]]:
        """Generate quiz questions with answers"""
        difficulty_params = {
            "easy": {"marks": 5, "detail": "basic"},
            "medium": {"marks": 10, "detail": "moderate"},
            "hard": {"marks": 15, "detail": "advanced"}
        }
        
        params = difficulty_params.get(difficulty, difficulty_params["medium"])
        questions = []
        
        for i in range(count):
            q_type = self.question_types[i % len(self.question_types)]
            
            if q_type == "multiple_choice":
                questions.append({
                    "id": f"q_{i+1}",
                    "type": "multiple_choice",
                    "question": f"Question {i+1}: What is the {difficulty} concept of {subject}?",
                    "marks": params["marks"],
                    "options": [
                        f"Option A - Basic answer about {subject}",
                        f"Option B - Correct answer about {subject}",
                        f"Option C - Incorrect but plausible answer",
                        f"Option D - Completely wrong answer"
                    ],
                    "correct_answer": 1,
                    "explanation": f"The correct answer is B because it accurately describes the {difficulty} concept of {subject}"
                })
            elif q_type == "true_false":
                questions.append({
                    "id": f"q_{i+1}",
                    "type": "true_false",
                    "question": f"Question {i+1}: True or False? {subject} statement is correct.",
                    "marks": params["marks"],
                    "correct_answer": True,
                    "explanation": "This statement is true because..."
                })
            elif q_type == "short_answer":
                questions.append({
                    "id": f"q_{i+1}",
                    "type": "short_answer",
                    "question": f"Question {i+1}: Briefly explain the concept of {subject}.",
                    "marks": params["marks"],
                    "expected_keywords": ["definition", "key point 1", "key point 2"],
                    "sample_answer": f"A comprehensive explanation of {subject} including definition and examples"
                })
            else:  # essay
                questions.append({
                    "id": f"q_{i+1}",
                    "type": "essay",
                    "question": f"Question {i+1}: Discuss the importance and applications of {subject}.",
                    "marks": params["marks"],
                    "expected_length": "200-300 words",
                    "rubric": {
                        "understanding": 5,
                        "examples": 3,
                        "clarity": 2
                    }
                })
        
        return questions

    async def evaluate_answers(self, quiz_id: str, answers: List[Dict[str, Any]], questions: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Evaluate quiz answers and provide detailed feedback"""
        if not questions:
            questions = []
        
        score = 0
        total_marks = 0
        feedback_details = []
        
        for answer in answers:
            q_id = answer.get("question_id")
            student_answer = answer.get("answer")
            
            # Find corresponding question
            question = next((q for q in questions if q.get("id") == q_id), None)
            if not question:
                continue
            
            marks = question.get("marks", 10)
            total_marks += marks
            
            # Check answer correctness
            is_correct = self._check_answer(question, student_answer)
            if is_correct:
                score += marks
            
            feedback_details.append({
                "question_id": q_id,
                "is_correct": is_correct,
                "marks_obtained": marks if is_correct else 0,
                "total_marks": marks,
                "student_answer": student_answer,
                "correct_answer": question.get("correct_answer", ""),
                "explanation": question.get("explanation", ""),
                "feedback": self._generate_feedback(question, is_correct)
            })
        
        percentage = (score / total_marks * 100) if total_marks > 0 else 0
        
        return {
            "quiz_id": quiz_id,
            "total_score": score,
            "total_marks": total_marks,
            "percentage": round(percentage, 2),
            "passed": percentage >= 60,
            "timestamp": datetime.utcnow().isoformat(),
            "details": feedback_details,
            "analysis": self._generate_quiz_analysis(feedback_details),
            "recommendations": self._generate_recommendations(feedback_details)
        }

    def _check_answer(self, question: Dict[str, Any], student_answer: Any) -> bool:
        """Check if student answer is correct"""
        q_type = question.get("type")
        
        if q_type == "multiple_choice":
            return student_answer == question.get("correct_answer")
        elif q_type == "true_false":
            return student_answer == question.get("correct_answer")
        else:
            # For short answer and essay, basic keyword matching
            keywords = question.get("expected_keywords", [])
            if isinstance(student_answer, str):
                return any(kw.lower() in student_answer.lower() for kw in keywords)
        
        return False

    def _generate_feedback(self, question: Dict[str, Any], is_correct: bool) -> str:
        """Generate feedback for an answer"""
        if is_correct:
            return "✓ Correct! " + question.get("explanation", "")
        else:
            return "✗ Incorrect. " + question.get("explanation", "")

    def _generate_quiz_analysis(self, details: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze quiz performance"""
        total_questions = len(details)
        correct_answers = sum(1 for d in details if d["is_correct"])
        
        return {
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "incorrect_answers": total_questions - correct_answers,
            "accuracy": round((correct_answers / total_questions * 100) if total_questions > 0 else 0, 2),
            "performance_level": self._get_performance_level(correct_answers, total_questions)
        }

    def _get_performance_level(self, correct: int, total: int) -> str:
        """Determine performance level"""
        if total == 0:
            return "Not attempted"
        percentage = correct / total * 100
        if percentage >= 90:
            return "Excellent"
        elif percentage >= 75:
            return "Good"
        elif percentage >= 60:
            return "Satisfactory"
        else:
            return "Needs Improvement"

    def _generate_recommendations(self, details: List[Dict[str, Any]]) -> List[str]:
        """Generate study recommendations based on performance"""
        incorrect = [d for d in details if not d["is_correct"]]
        
        if not incorrect:
            return ["Great job! You've mastered this topic. Try harder questions."]
        
        return [
            f"Review the concepts covered in {len(incorrect)} questions you missed",
            "Focus on understanding the underlying principles",
            "Practice more problems of this type",
            "Discuss your answers with a mentor or tutor"
        ]

    async def generate_assignment(self, student_id: str, subject_id: str, instructions: str, roadmap: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate assignment based on subject and roadmap"""
        return {
            "assignment_id": f"assign_{datetime.utcnow().timestamp()}",
            "student_id": student_id,
            "subject": subject_id,
            "instructions": instructions,
            "tasks": self._generate_assignment_tasks(subject_id),
            "due_date": (datetime.utcnow().timestamp() + 86400 * 7),  # 7 days from now
            "created_at": datetime.utcnow().isoformat(),
            "status": "created"
        }

    def _generate_assignment_tasks(self, subject: str) -> List[Dict[str, Any]]:
        """Generate individual assignment tasks"""
        return [
            {
                "task_id": "t1",
                "description": f"Complete problems 1-10 on {subject}",
                "marks": 10,
                "resources": ["Chapter 2", "Example 3"]
            },
            {
                "task_id": "t2",
                "description": f"Write a 500-word essay on applications of {subject}",
                "marks": 10,
                "resources": ["Research papers", "Online articles"]
            },
            {
                "task_id": "t3",
                "description": f"Create a presentation comparing concepts in {subject}",
                "marks": 10,
                "resources": ["Video tutorials", "Slide templates"]
            }
        ]
