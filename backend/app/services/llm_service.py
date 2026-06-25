"""LLM Service for AI content generation.

Supports OpenAI and Google AI (Gemini) for generating educational content.
"""
import os
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()


class LLMService:
    """Service for LLM-based content generation."""
    
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.model = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash-lite')
        
    def is_available(self) -> bool:
        """Check if any LLM service is available."""
        return bool(self.google_api_key or self.openai_api_key)
    
    async def generate_text(self, prompt: str, system_prompt: str = None, max_tokens: int = 1000) -> str:
        """Generate text using available LLM."""
        # Prefer Google AI (Gemini) since user has that configured
        if self.google_api_key:
            return await self._generate_with_google(prompt, system_prompt, max_tokens)
        elif self.openai_api_key:
            return await self._generate_with_openai(prompt, system_prompt, max_tokens)
        else:
            raise Exception("No LLM API key configured")
    
    async def _generate_with_openai(self, prompt: str, system_prompt: str = None, max_tokens: int = 1000) -> str:
        """Generate text using OpenAI API."""
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=self.openai_api_key)
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = await client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI generation failed: {e}")
            raise
    
    async def _generate_with_google(self, prompt: str, system_prompt: str = None, max_tokens: int = 1000) -> str:
        """Generate text using Google AI (Gemini) API."""
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.google_api_key)
            
            model = genai.GenerativeModel(self.model)
            
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            response = model.generate_content(full_prompt)
            
            return response.text
        except Exception as e:
            print(f"Google AI generation failed: {e}")
            raise
    
    async def generate_roadmap(self, syllabus: str, datesheet: str) -> Dict[str, Any]:
        """Generate a study roadmap using LLM."""
        system_prompt = """You are an expert educational planner. Generate a comprehensive study roadmap based on the syllabus and exam dates.
Return a JSON object with the following structure:
{
    "chapters": [{"name": "Chapter Name", "topics": ["topic1", "topic2"], "estimated_hours": 5, "difficulty": "beginner"}],
    "exam_date": "YYYY-MM-DD",
    "days_remaining": 90,
    "total_chapters": 10,
    "total_estimated_hours": 50
}"""
        
        prompt = f"""Syllabus:\n{syllabus}\n\nExam Dates:\n{datesheet}\n\nGenerate a structured study roadmap."""
        
        response = await self.generate_text(prompt, system_prompt, max_tokens=2000)
        
        # Parse JSON response (in production, add proper error handling)
        import json
        try:
            return json.loads(response)
        except:
            # Fallback if JSON parsing fails
            return {
                "chapters": [{"name": "General Study", "topics": ["Topic 1"], "estimated_hours": 5, "difficulty": "beginner"}],
                "exam_date": "2024-12-31",
                "days_remaining": 90,
                "total_chapters": 1,
                "total_estimated_hours": 5
            }
    
    async def generate_explanation(self, topic: str, level: str = "beginner") -> Dict[str, Any]:
        """Generate a detailed explanation for a topic."""
        system_prompt = f"""You are an expert teacher. Generate a comprehensive explanation for the topic at {level} level.
Return a JSON object with: overview, definition, why_important, real_world_applications, prerequisites."""
        
        prompt = f"Generate a detailed explanation for: {topic}"
        
        response = await self.generate_text(prompt, system_prompt, max_tokens=1500)
        
        import json
        try:
            return json.loads(response)
        except:
            return {
                "overview": f"Introduction to {topic}",
                "definition": f"{topic} is a fundamental concept",
                "why_important": f"Understanding {topic} is essential for mastery",
                "real_world_applications": ["Practical application 1", "Practical application 2"],
                "prerequisites": ["Basic concepts"]
            }
    
    async def generate_examples(self, topic: str, count: int = 3) -> List[Dict[str, Any]]:
        """Generate worked examples for a topic."""
        system_prompt = f"""Generate {count} worked examples for the topic. Each example should have: problem, solution_steps, answer, explanation."""
        
        prompt = f"Generate {count} worked examples for: {topic}"
        
        response = await self.generate_text(prompt, system_prompt, max_tokens=1500)
        
        import json
        try:
            return json.loads(response)
        except:
            return [
                {
                    "example_number": 1,
                    "problem": f"Example problem for {topic}",
                    "solution_steps": ["Step 1", "Step 2", "Step 3"],
                    "answer": "Solution",
                    "explanation": "Explanation"
                }
            ]
    
    async def generate_quiz(self, subject: str, difficulty: str = "medium", num_questions: int = 5) -> Dict[str, Any]:
        """Generate a quiz for a subject."""
        system_prompt = f"""Generate a quiz with {num_questions} questions for {subject} at {difficulty} level.
Return a JSON object with: quiz_id, questions (each with question_text, options, correct_answer, explanation)."""
        
        prompt = f"Generate a quiz for: {subject}"
        
        response = await self.generate_text(prompt, system_prompt, max_tokens=2000)
        
        import json
        try:
            return json.loads(response)
        except:
            return {
                "quiz_id": "quiz_1",
                "questions": [
                    {
                        "question_text": f"Question about {subject}",
                        "options": ["A", "B", "C", "D"],
                        "correct_answer": "A",
                        "explanation": "Explanation"
                    }
                ]
            }


# Global LLM service instance
llm_service = LLMService()
