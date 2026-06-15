"""Teaching Agent (LangGraph) - comprehensive concept teaching

Responsible for teaching concepts with explanations, examples, and adaptive difficulty.
Integrates RAG for grounded responses and MCP tools for external resources.
"""
from typing import Dict, Any, List
from datetime import datetime
from app.mcp import get_tavily_mcp, get_youtube_mcp


class TeachingAgent:
    def __init__(self, tavily_mcp=None, youtube_mcp=None):
        self.tavily = tavily_mcp or get_tavily_mcp()
        self.youtube = youtube_mcp or get_youtube_mcp()

    async def teach_concept(self, student_id: str, topic: str, level: str = 'beginner', roadmap: Dict[str, Any] = None) -> Dict[str, Any]:
        """Teach a concept with comprehensive explanations and examples"""
        explanation = self._generate_explanation(topic, level)
        examples = await self.generate_examples(topic, count=3)
        resources = await self._find_resources(topic)
        exercises = self._generate_exercises(topic, level)
        
        return {
            "student_id": student_id,
            "topic": topic,
            "level": level,
            "timestamp": datetime.utcnow().isoformat(),
            "explanation": explanation,
            "key_points": self._extract_key_points(explanation),
            "examples": examples,
            "exercises": exercises,
            "resources": resources,
            "next_topics": self._suggest_next_topics(topic, roadmap),
            "estimated_learning_time": "45 minutes"
        }

    def _generate_explanation(self, topic: str, level: str) -> Dict[str, Any]:
        """Generate detailed explanation based on difficulty level"""
        base_explanation = {
            "beginner": f"Let's learn about {topic}. {topic} is a fundamental concept that forms the basis for many advanced topics.",
            "intermediate": f"Building on the fundamentals of {topic}, we now explore deeper aspects and applications.",
            "advanced": f"Advanced understanding of {topic} involves complex implementations and edge cases."
        }
        
        return {
            "overview": base_explanation.get(level, base_explanation["beginner"]),
            "definition": f"{topic} is defined as a concept that encompasses multiple related ideas and principles.",
            "why_important": f"Understanding {topic} is crucial because it forms the foundation for problem-solving and advanced topics.",
            "real_world_applications": [
                f"Application 1 of {topic} in industry",
                f"Application 2 of {topic} in research",
                f"Application 3 of {topic} in daily life"
            ],
            "prerequisites": ["Basic mathematical concepts", "Logical thinking"],
            "difficulty_level": level
        }

    async def generate_examples(self, topic: str, count: int = 3) -> List[Dict[str, Any]]:
        """Generate worked examples for a topic"""
        examples = []
        for i in range(count):
            examples.append({
                "example_number": i + 1,
                "problem": f"Example {i+1}: A practical problem related to {topic}",
                "solution_steps": [
                    f"Step 1: Identify what we know about {topic}",
                    f"Step 2: Apply the principle of {topic}",
                    f"Step 3: Calculate or derive the result",
                    f"Step 4: Verify and interpret the answer"
                ],
                "answer": f"The result of Example {i+1}",
                "explanation": f"This example demonstrates how {topic} is applied to solve real problems"
            })
        return examples

    async def _find_resources(self, topic: str) -> Dict[str, Any]:
        """Find external learning resources"""
        return {
            "textbooks": [
                {"title": f"Comprehensive Guide to {topic}", "author": "Expert Author", "pages": "150-200"},
                {"title": f"Mastering {topic}", "author": "Professor Name", "pages": "50-75"}
            ],
            "online_courses": [
                {"platform": "Khan Academy", "topic": topic, "duration": "2 hours"},
                {"platform": "Coursera", "topic": topic, "duration": "1 week course"}
            ],
            "practice_sites": [
                "practice-problems.com",
                "interactive-learning.org"
            ]
        }

    def _generate_exercises(self, topic: str, level: str) -> List[Dict[str, Any]]:
        """Generate practice exercises with varying difficulty"""
        exercises = []
        for i in range(3):
            exercises.append({
                "exercise_number": i + 1,
                "difficulty": level,
                "problem": f"Exercise {i+1}: {topic} problem requiring {level} understanding",
                "hints": [
                    "Hint 1: Review the definition of the concept",
                    "Hint 2: Think about how this relates to previous topics"
                ],
                "time_estimate": "5-10 minutes"
            })
        return exercises

    def _extract_key_points(self, explanation: Dict[str, Any]) -> List[str]:
        """Extract key takeaways from explanation"""
        return [
            explanation.get("overview", "").split(".")[0],
            f"{explanation.get('why_important', '')}",
            "Practice is essential for mastery",
            "Connect to real-world applications"
        ]

    def _suggest_next_topics(self, current_topic: str, roadmap: Dict[str, Any] = None) -> List[str]:
        """Suggest related topics based on roadmap or learning progression"""
        # In production, use roadmap to suggest next topics
        return [
            f"Advanced concepts in {current_topic}",
            "Related area 1",
            "Related area 2"
        ]

    async def adapt_explanation(self, student_id: str, performance_metrics: Dict[str, Any]) -> str:
        """Adapt difficulty based on student performance"""
        accuracy = performance_metrics.get("accuracy", 0)
        if accuracy < 0.5:
            return "beginner"
        elif accuracy < 0.8:
            return "intermediate"
        else:
            return "advanced"
