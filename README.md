# agentify-ops-meeting
# Agentify Ops

Agentify Ops is a human-in-the-loop assistant that turns meeting transcripts into structured decisions, risks, and proposed Kanban tasks. Users review the extracted work before it changes the local project board.

# Why this project

Meeting outcomes are often scattered across long conversations. Agentify Ops demonstrates a practical LLM workflow: validate input, extract structured data, preserve source evidence, require human approval, and persist approved work items.

# Features

•
Paste or upload a .txt/.md transcript.

•
Deterministic offline mock mode for demos and tests.

•
Optional OpenAI-compatible live LLM mode.

•
Pydantic validation for model output.

•
Evidence text attached to every extracted action item.

•
Human approval before tasks enter the Kanban board.

•
Local SQLite persistence.

•
Streamlit UI and GitHub Actions tests.

Architecture

<img width="236" height="694" alt="image" src="https://github.com/user-attachments/assets/add03c81-6aa7-4a47-8a0d-4019cca9c49f" />






The MVP intentionally uses transcript upload/paste rather than Zoom or Google Meet APIs. Those integrations require OAuth, provider permissions, recording retrieval, and webhook handling, so they are future adapters rather than hidden claims of the current version.

# Setup

Bash


python3 -m venv .venv
source .venv/bin/activate        # Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
cp .env.example .env             # Windows: copy .env.example .env
export PYTHONPATH=src             # Windows PowerShell: $env:PYTHONPATH = "src"



Run offline demo mode:

Bash


streamlit run app.py



Choose mock mode in the sidebar and upload sample_data/demo_transcript.txt. Mock mode is not an LLM response; it is a deterministic test/demo implementation.

Live mode

Copy .env.example to .env and set LLM_API_KEY, LLM_BASE_URL, and LLM_MODEL for an OpenAI-compatible provider. Never commit .env or API keys. Live mode validates the returned JSON but cannot guarantee that the model extracted every task correctly.

# Tests and evaluation

Bash


PYTHONPATH=src pytest -q



The tests cover short-input rejection, deterministic extraction, evidence mapping, schema validation, and an integration-style SQLite round trip without paid API calls.

The included sample transcript is a reproducible smoke-test set. The current evaluation checks structural properties—valid output and evidence strings that occur in the input—not semantic completeness or model accuracy. It does not prove that all decisions, owners, dates, or risks are correct. A stronger evaluation would use a larger, manually labeled transcript set and report precision/recall for each field.

# Security and privacy

Transcripts may contain confidential information. This MVP stores transcript text and results in a local SQLite database and sends text to the configured LLM provider in live mode. Obtain consent, minimize sensitive data, review provider retention settings, and do not use production confidential transcripts without an appropriate privacy review.

# Limitations and next steps

•
No direct Zoom or Google Meet ingestion.

•
No authentication or multi-user permissions.

•
Local SQLite is not designed for concurrent production use.

•
Evidence is requested and validated as a substring, not independently verified for semantic accuracy.

•
Due-date parsing in mock mode is intentionally minimal.

# Ultimate Objective
Create a continuous, AI-assisted workflow that connects meetings to execution. Every important discussion can become an actionable task, every task has a clear owner, and progress is tracked between meetings.

Potential improvements include provider adapters for Zoom/Google Meet, background job processing, stronger evidence span offsets, user authentication, PostgreSQL, notifications, and automated chasing.

AI-Powered Meeting Management and Project Execution Workflow
1. Team Meeting
Team members discuss project progress, current challenges, key decisions, and next steps. The goal is to capture important information and turn meeting discussions into actionable work.

2. Otter.ai Captures the Meeting
Otter.ai records the meeting and generates a transcript, identifies speakers, and captures meeting notes for later analysis.

3. Google Sheets Stores Meeting Data
The transcript and related meeting information are saved to Google Sheets, creating a centralized, structured record of discussions, decisions, and potential action items.

4. AI Analyzes the Transcript
An LLM reviews the transcript and identifies key discussion points, meeting summaries, decisions, risks, unresolved questions, action items, assigned owners, and proposed deadlines.

5. Meeting Summary Is Distributed
The AI generates a concise meeting summary, including decisions made, action items, and outstanding issues. The summary is shared with all meeting participants so everyone has a consistent understanding of the outcomes.

6. CEO Reviews and Approves Changes
The CEO reviews the summary and proposed action items, corrects inaccuracies, resolves ambiguities, and approves the changes before they are implemented in the project management system.

7. Kanban Project Management Board Is Updated
Once approved, the system updates the Kanban board with the appropriate tasks, owners, deadlines, priorities, and statuses. This turns meeting decisions into trackable work.

8. AI Monitors Open Tasks Between Meetings
The AI monitors outstanding commitments by tracking task owners, deadlines, progress, dependencies, and overdue items. It identifies potential delays and tasks that may require attention.

9. AI Follows Up With Task Owners
The AI contacts task owners to request progress updates, confirm deadlines, and identify blockers. This helps maintain accountability without requiring constant manual follow-up from leadership.

10. AI Processes Updates and Flags Risks
Responses from task owners are analyzed and summarized. The AI identifies progress, changes in timelines, emerging risks, and proposed updates to the project management board.

11. Updates Are Applied or Escalated
Routine updates are applied according to predefined permissions and approval rules. Significant changes, missed commitments, and unresolved blockers are escalated to the CEO or the appropriate decision-maker for review.

12. The Next Meeting Starts With Verified Progress
Before the next team meeting, the AI prepares an updated overview of completed tasks, outstanding commitments, overdue items, responsible owners, and unresolved blockers.

The team can then focus on progress, accountability, and decisions that require discussion rather than spending valuable meeting time reconstructing what happened previously.

The CEO retains oversight and approval authority, while AI handles the repetitive work of summarizing discussions, organizing tasks, monitoring commitments, and preparing the team for its next meeting.
