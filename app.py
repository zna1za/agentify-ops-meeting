import os
import uuid

import streamlit as st
from dotenv import load_dotenv

from meetingops.extractor import ExtractionError, build_extractor, validate_transcript
from meetingops.models import Task
from meetingops.repository import Repository

load_dotenv()
st.set_page_config(page_title="MeetingOps", page_icon="", layout="wide")

repo = Repository(os.getenv("MEETINGOPS_DB", "meetingops.db"))

st.title("MeetingOps")
st.caption("Human-in-the-loop meeting transcript to Kanban workflow assistant")

mode = st.sidebar.radio("Extraction mode", ["mock", "live"], help="Mock mode is deterministic and does not call an API.")
tab_analyze, tab_board = st.tabs(["Analyze meeting", "Kanban board"])

with tab_analyze:
    uploaded = st.file_uploader("Upload a transcript", type=["txt", "md"])
    default_text = uploaded.read().decode("utf-8") if uploaded else ""
    transcript = st.text_area("Transcript", value=default_text, height=280, placeholder="Paste a meeting transcript here...")
    if st.button("Analyze transcript", type="primary"):
        try:
            clean = validate_transcript(transcript)
            result = build_extractor(mode).extract(clean)
            meeting_id = str(uuid.uuid4())[:8]
            st.session_state["pending_result"] = result
            st.session_state["pending_meeting_id"] = meeting_id
            repo.save_meeting(meeting_id, clean, result)
            st.success(f"Analysis complete. Meeting ID: {meeting_id}")
        except (ValueError, ExtractionError) as exc:
            st.error(str(exc))

    result = st.session_state.get("pending_result")
    meeting_id = st.session_state.get("pending_meeting_id")
    if result and meeting_id:
        st.subheader("Review proposed results")
        st.write(result.summary)
        if result.decisions:
            st.markdown("**Decisions**")
            for decision in result.decisions:
                st.write(f"- {decision}")
        if result.risks:
            st.markdown("**Risks**")
            for risk in result.risks:
                st.write(f"- {risk}")
        st.markdown("**Action items**")
        for item in result.action_items:
            with st.expander(f"{item.title} — {item.owner} ({item.priority})", expanded=True):
                st.caption(f"Evidence: {item.evidence}")
                st.write(f"Due: {item.due_date or 'Not specified'}")
        if result.action_items and st.button("Approve action items and add to board"):
            repo.add_tasks([Task(meeting_id=meeting_id, **item.model_dump()) for item in result.action_items])
            st.success("Approved tasks added to the Kanban board.")

with tab_board:
    st.subheader("Project workflow")
    columns = {"backlog": "Backlog", "in_progress": "In progress", "blocked": "Blocked", "done": "Done"}
    tasks = repo.list_tasks()
    board = st.columns(len(columns))
    for column, (status, label) in zip(board, columns.items()):
        with column:
            st.markdown(f"### {label}")
            for task in [task for task in tasks if task.status == status]:
                with st.container(border=True):
                    st.write(f"**{task.title}**")
                    st.caption(f"Owner: {task.owner} · Priority: {task.priority} · Meeting: {task.meeting_id}")
                    st.caption(f"Evidence: {task.evidence}")
                    choices = list(columns)
                    selected = st.selectbox("Move task", choices, index=choices.index(task.status), key=f"status_{task.id}", format_func=lambda value: columns[value])
                    if selected != task.status:
                        repo.update_task_status(task.id, selected)
                        st.rerun()
