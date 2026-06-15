Prompts Directory
=================

This folder contains system-level prompts, agent prompts, and safety policies
used by LangGraph agents. Agents should load these files at startup or the
orchestrator should embed the text into the LangGraph node definitions.

Files:
- `system_prompt.md` — global system instructions and constraints.
- `agent_prompts.md` — per-agent prompt templates and expected JSON outputs.
- `safety_policy.md` — rules for refusing harmful or cheating-related requests.
