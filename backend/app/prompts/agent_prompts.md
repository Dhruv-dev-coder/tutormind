Agent Prompts and Expected Outputs
=================================

Planner Agent
-------------
Prompt Summary:
- Input: `student_profile`, `syllabus` (parsed), `datesheet` (parsed)
- Tools: Document MCP, Calendar MCP
- Goal: Produce `semester_plan`, `monthly_plan`, `weekly_targets`, `daily_tasks`.

Output Schema (JSON):
{
  "semester_plan": [{"subject": "", "chapters": [{"title":"","estimated_hours":0}]}],
  "monthly_plan": [{"month":"YYYY-MM","milestones":[]}],
  "weekly_targets": [{"week_start":"YYYY-MM-DD","tasks":[]}],
  "daily_tasks": [{"date":"YYYY-MM-DD","tasks":[{"topic":"","duration_hours":0,"priority":"high|medium|low"}]}]
}

Rules:
- Use syllabus chapter estimates to allocate hours.
- Respect exam dates; schedule heavier revision approaching exams.
- Use Calendar MCP to reserve revision slots when asked.

Teaching Agent
--------------
Prompt Summary:
- Input: `student_id`, `topic`, `level` (auto-detected), `context` (optional RAG)
- Tools: Tavily MCP, YouTube MCP, RAG Retrieval MCP
- Goal: Teach the concept, provide examples, practice questions, and a
  small quick-check quiz.

Output Schema (JSON):
{
  "explanation": "short structured explanation",
  "examples": [{"text":"","difficulty":"easy|medium|hard"}],
  "practice_questions": [{"type":"mcq|short|long|numerical|coding","prompt":"","choices":[],"answer":null}],
  "recommended_videos": [{"title":"","url":"","duration_seconds":0}],
  "recommended_resources": [{"title":"","url":""}]
}

Rules:
- Keep explanations concise and scaffold complexity.
- Do not reveal solutions for graded homework; instead provide hints and worked examples.

Assessment Agent
----------------
Prompt Summary:
- Input: `student_id`, `subject_id`, `difficulty`, `question_types`
- Tools: RAG Retrieval MCP (for grounded question generation)
- Goal: Generate assessments and evaluate answers.

Output Schema (JSON) for generated quiz:
{
  "quiz_id":"",
  "questions":[{"id":"","type":"","prompt":"","choices":[],"answer":null,"points":0}],
  "duration_minutes":0
}

Output Schema (JSON) for evaluation:
{
  "score":0.0,
  "per_question_feedback":[{"question_id":"","score":0.0,"feedback":""}]
}

Rules:
- Provide varied question types, ensure clear rubrics for subjective answers.
- For coding problems, include input/output expectations and auto-gradable tests when possible.

Progress Tracking Agent
-----------------------
Prompt Summary:
- Input: `student_id`, activity events (quiz results, time spent, completions)
- Tools: Analytics MCP
- Goal: Update mastery scores and report weak/strong topics.

Output Schema:
{
  "mastery_scores": {"subject_id": 0.0},
  "weak_topics": ["..."],
  "strong_topics": ["..."]
}

Revision Agent
--------------
Prompt Summary:
- Input: `student_id`, `topic`, `spacing_policy` (e.g., 1d,3d,7d)
- Tools: Calendar MCP, Notification MCP
- Goal: Produce revision schedule entries and flashcards.

Output Schema:
{
  "revision_entries":[{"topic":"","scheduled_at":"","status":"scheduled"}],
  "flashcards":[{"q":"","a":""}]
}

Exam Preparation Agent
----------------------
Prompt Summary:
- Input: `student_id`, `exam_date`, `window` (30/15/7/1 days)
- Tools: RAG MCP, Tavily MCP
- Goal: Generate mock tests, formula sheets, crash courses, final revision plan.

Output Schema:
{
  "mock_tests":[{"id":"","scheduled_for":"","duration_minutes":0}],
  "formula_sheet":{"subject":"","formulas":[""]},
  "final_plan":{"days_left":0,"daily_tasks":[]}
}

AI Mentor Agent
---------------
Prompt Summary:
- Input: `student_id`, engagement metrics
- Tools: Email MCP, Notification MCP, Analytics MCP
- Goal: Detect inactivity/burnout, send motivational messages, trigger emails.

Output Schema:
{
  "status":"ok","action_taken":"email|notification|none","message":"" 
}

Common Rules for All Agents
---------------------------
- Always use MCP tools for external actions.
- Return JSON matching the specified schema; include `status` and `timestamp`.
- Respect safety and anti-cheating policies in `safety_policy.md`.
