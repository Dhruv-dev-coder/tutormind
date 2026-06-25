"""Teaching Agent (LangGraph) - comprehensive concept teaching

Responsible for teaching concepts with explanations, examples, and adaptive difficulty.
Integrates RAG for grounded responses and MCP tools for external resources.
"""
from typing import Dict, Any, List
from datetime import datetime
from app.mcp import get_tavily_mcp, get_youtube_mcp
from app.agents.learning_intelligence import (
    build_lesson_path,
    dedupe_keep_order,
    infer_learning_objectives,
    normalize_level,
    roadmap_topics,
    topic_title,
)


class TeachingAgent:
    def __init__(self, tavily_mcp=None, youtube_mcp=None):
        self.tavily = tavily_mcp or get_tavily_mcp()
        self.youtube = youtube_mcp or get_youtube_mcp()

    async def teach_concept(self, student_id: str, topic: str, level: str = 'beginner', roadmap: Dict[str, Any] = None) -> Dict[str, Any]:
        """Teach a concept with comprehensive explanations and examples"""
        level = normalize_level(level)
        explanation = self._generate_explanation(topic, level)
        examples = await self.generate_examples(topic, count=3)
        resources = await self._find_resources(topic)
        exercises = self._generate_exercises(topic, level)
        lesson_path = build_lesson_path(topic, level)
        
        return {
            "student_id": student_id,
            "topic": topic,
            "level": level,
            "timestamp": datetime.utcnow().isoformat(),
            "explanation": explanation,
            "learning_objectives": infer_learning_objectives(topic, level),
            "lesson_path": lesson_path,
            "key_points": self._extract_key_points(explanation),
            "examples": examples,
            "exercises": exercises,
            "resources": resources,
            "next_topics": self._suggest_next_topics(topic, roadmap),
            "estimated_learning_time": f"{sum(step['minutes'] for step in lesson_path)} minutes"
        }

    def _generate_explanation(self, topic: str, level: str) -> Dict[str, Any]:
        """Generate detailed explanation based on difficulty level"""
        title = topic_title(topic)
        base_explanation = {
            "beginner": f"Start with the big idea: {title} is easier when you connect the definition to one simple example before memorizing rules.",
            "intermediate": f"Now connect {title} to problem patterns, exceptions, and method selection.",
            "advanced": f"Advanced work on {title} focuses on multi-step reasoning, edge cases, and exam-time tradeoffs."
        }
        
        return {
            "overview": base_explanation.get(level, base_explanation["beginner"]),
            "definition": f"{title} is the set of rules, relationships, and reasoning patterns used to solve this class of problems.",
            "why_important": f"Understanding {title} helps you identify the right method quickly instead of trying unrelated formulas or facts.",
            "real_world_applications": [
                f"Using {title} to model real situations",
                f"Using {title} to compare possible solutions",
                f"Using {title} to explain why an answer is reasonable"
            ],
            "prerequisites": ["Core vocabulary", "Prior chapter fundamentals", "Step-by-step reasoning"],
            "difficulty_level": level
        }

    async def generate_examples(self, topic: str, count: int = 3) -> List[Dict[str, Any]]:
        """Generate worked examples for a topic"""
        title = topic_title(topic)
        examples = []
        for i in range(count):
            examples.append({
                "example_number": i + 1,
                "problem": f"Example {i+1}: Solve a practical {title} question with one clear constraint.",
                "solution_steps": [
                    f"Step 1: Identify the given information and what {title} asks for",
                    f"Step 2: Choose the rule or relationship that fits {title}",
                    "Step 3: Work through the calculation or reasoning carefully",
                    "Step 4: Check units, assumptions, and whether the answer makes sense"
                ],
                "answer": f"A complete answer for Example {i+1}",
                "explanation": f"This example shows the thinking pattern behind {title}, not just the final result."
            })
        return examples

    async def _find_resources(self, topic: str) -> Dict[str, Any]:
        """Find external learning resources"""
        academic_resources = await self.tavily.search_academic_resources(topic, limit=5)
        tutorials = await self.youtube.find_tutorials(topic, max_results=3)
        revision_videos = await self.youtube.find_revision_videos(topic, max_results=2)

        return {
            "academic": academic_resources,
            "videos": dedupe_keep_order([video.get("url", "") for video in tutorials + revision_videos]),
            "video_details": tutorials + revision_videos,
            "source": "mcp"
        }

    def _generate_exercises(self, topic: str, level: str) -> List[Dict[str, Any]]:
        """Generate practice exercises with varying difficulty"""
        title = topic_title(topic)
        exercises = []
        prompts = {
            "beginner": ["identify", "define", "solve a direct"],
            "intermediate": ["compare", "apply", "explain an error in a"],
            "advanced": ["prove or justify", "combine with another concept in a", "optimize a"],
        }
        for i, verb in enumerate(prompts.get(level, prompts["beginner"])):
            exercises.append({
                "exercise_number": i + 1,
                "difficulty": level,
                "problem": f"Exercise {i+1}: {verb} {title} problem.",
                "hints": [
                    "Hint 1: Write down the definition or rule before solving",
                    "Hint 2: Point to the exact clue that tells you which method to use"
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
        topics = roadmap_topics(roadmap)
        current_key = current_topic.strip().lower()
        if topics:
            for index, topic in enumerate(topics):
                if topic.lower() == current_key:
                    return topics[index + 1:index + 4] or [f"Advanced {topic_title(current_topic)}"]
            return topics[:3]
        return [f"Advanced {topic_title(current_topic)}", f"Practice problems for {topic_title(current_topic)}", "Mixed revision"]

    async def adapt_explanation(self, student_id: str, performance_metrics: Dict[str, Any]) -> str:
        """Adapt difficulty based on student performance"""
        accuracy = performance_metrics.get("accuracy", 0)
        if accuracy < 0.5:
            return "beginner"
        elif accuracy < 0.8:
            return "intermediate"
        else:
            return "advanced"
