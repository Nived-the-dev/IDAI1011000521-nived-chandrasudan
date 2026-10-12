"""ParentConnect AI | Streamlit front end for the prebuilt Dialogflow ES agent.

This application does not contain hard-coded intent responses, a shadow
chatbot, or any real student records. Every chat request reaches Dialogflow ES.
"""

from __future__ import annotations

import hmac
import uuid

import streamlit as st

from dialogflow_client import ask_dialogflow, helpful_error

st.set_page_config(
    page_title="ParentConnect AI | School communication",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

CSS = """
<style>
:root { --pc-primary:#4634bb; --pc-ink:#152039; --pc-muted:#67728b; }
#MainMenu, footer {visibility:hidden;}
.block-container {max-width:1120px; padding-top:1.55rem; padding-bottom:4rem;}
[data-testid="stAppViewContainer"] {background:#f6f8fc;}
[data-testid="stSidebar"] {background:#eef1f8; border-right:1px solid #dde3ee;}
[data-testid="stSidebar"] .stMarkdown p {line-height:1.55;}
.pc-top {background:#ffffff; border:1px solid #e0e6f0; border-radius:21px;
    padding:24px 28px 21px; margin-bottom:18px; box-shadow:0 8px 24px rgba(21,33,69,.035);}
.pc-kicker {letter-spacing:.16em;text-transform:uppercase;color:#6654c7;font-size:.69rem;font-weight:800;}
.pc-brand {font-weight:850; color:#172039; font-size:2.05rem; margin:.25rem 0 .5rem; line-height:1.2;}
.pc-sub {color:#5b6680;font-size:.98rem;line-height:1.6;max-width:760px;}
.pc-status {margin:18px 0 4px; display:inline-block; font-size:.78rem; color:#305c48;
  background:#e5f5ed; border-radius:999px; padding:5px 12px; font-weight:750;}
.pc-status.off {color:#805415;background:#fff2d9;}
.pc-label {font-size:.75rem;color:#7a849a;font-weight:800;letter-spacing:.09em;text-transform:uppercase;margin:10px 0 5px;}
.pc-note {background:#fff;border:1px solid #e0e6f0;padding:12px 16px;border-radius:12px;color:#576278;font-size:.88rem;}
.pc-foot {font-size:.78rem;color:#7d8799;line-height:1.6;margin-top:20px;}
[data-testid="stChatMessage"] {background:white;border:1px solid #e6eaf2;border-radius:18px;margin:8px 0;padding:8px 13px;}
[data-testid="stButton"] button {border-radius:999px;border-color:#d8d1fb;background:#fff;color:#4934b8;font-weight:650;}
[data-testid="stButton"] button:hover {border-color:#5541cc;background:#f2efff;color:#31238f;}
[data-testid="stChatInput"] {border-radius:14px;}
@media(max-width:640px){.block-container{padding-top:.75rem}.pc-top{padding:18px}
.pc-brand{font-size:1.65rem}.pc-sub{font-size:.9rem}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def read_secret(name: str) -> str:
    try:
        return str(st.secrets.get(name, "")).strip()
    except (FileNotFoundError, KeyError):
        return ""


project_id = read_secret("dialogflow_project_id")
service_json = read_secret("service_account_json")
viewer_password = read_secret("viewer_password")
configured = bool(project_id and service_json)

if "session_id" not in st.session_state:
    st.session_state.session_id = uuid.uuid4().hex
if "messages" not in st.session_state:
    st.session_state.messages = []
if "access_granted" not in st.session_state:
    st.session_state.access_granted = not bool(viewer_password)

with st.sidebar:
    st.markdown("### 🎓 ParentConnect AI")
    st.caption("Viraj International School · Student prototype")
    st.divider()
    st.markdown("**About this project**")
    st.write("A conversational school-help assistant powered by **Google Dialogflow ES**.")
    st.markdown("**What it can help with**")
    st.markdown("Attendance · Exam schedules · Fees · School updates · Transport · Contacts")
    st.divider()
    if st.button("↻ New conversation", use_container_width=True):
        st.session_state.session_id = uuid.uuid4().hex
        st.session_state.messages = []
        st.rerun()
    show_intents = st.toggle("Show matched intents", value=False, help="Useful for assessment screenshots")
    st.divider()
    st.caption("Created by Nived Chandrasudan · Registration 1000521")
    st.caption("Demonstration only. Not an official source of school records.")

if not st.session_state.access_granted:
    st.markdown('<div class="pc-top"><div class="pc-kicker">ParentConnect / secure demo</div>'
                '<div class="pc-brand">Welcome to ParentConnect AI</div>'
                '<div class="pc-sub">Please enter the viewing password provided by the project owner.</div></div>',
                unsafe_allow_html=True)
    with st.form("access_form"):
        entry = st.text_input("Viewing password", type="password")
        submitted = st.form_submit_button("Open chatbot", use_container_width=True)
    if submitted:
        if hmac.compare_digest(entry, viewer_password):
            st.session_state.access_granted = True
            st.rerun()
        else:
            st.error("Incorrect password. Please try again.")
    st.stop()

st.markdown(
    '<div class="pc-top">'
    '<div class="pc-kicker">AI-POWERED SCHOOL SUPPORT · STUDENT PROJECT</div>'
    '<div class="pc-brand">Your school questions, answered simply.</div>'
    '<div class="pc-sub">Ask about attendance, examinations, fee guidance, transport, notices and school services. '
    'The chatbot understands everyday language and can ask follow-up questions to clarify your request.</div>'
    f'<div class="pc-status{"" if configured else " off"}">'
    f'{"● Dialogflow configured — test connection" if configured else "● Setup needed — Dialogflow not yet connected"}'
    '</div></div>', unsafe_allow_html=True,
)

if not configured:
    st.warning(
        "This is a website preview. To activate live Dialogflow responses, configure "
        "`dialogflow_project_id` and `service_account_json` in Streamlit secrets. "
        "See `docs/SETUP_STEP_BY_STEP.md` in the project ZIP."
    )

st.markdown('<div class="pc-label">Start with a topic</div>', unsafe_allow_html=True)
quick_replies = [
    ("📋 Attendance", "Show my child's attendance for grade 8"),
    ("📝 Exam schedule", "When are the final exams for grade 8"),
    ("💳 School fees", "What is the tuition fee for grade 8"),
    ("📣 Announcements", "What are the latest school announcements"),
    ("🚌 Transport", "Tell me about bus route 1"),
    ("🕒 School timings", "What are the school timings?"),
]
selection = None
for row in (quick_replies[:3], quick_replies[3:]):
    cols = st.columns(3)
    for col, (label, utterance) in zip(cols, row):
        with col:
            if st.button(label, key=f"quick_{label}", use_container_width=True, disabled=not configured):
                selection = utterance

st.markdown('<div class="pc-label">Conversation</div>', unsafe_allow_html=True)
if not st.session_state.messages:
    with st.chat_message("assistant", avatar="🎓"):
        st.write("Hello! I'm ParentConnect AI. Select a topic above or type a question to get started.")
        st.caption("For this demo, please use fictional examples, not real student information.")

for item in st.session_state.messages:
    with st.chat_message(item["role"], avatar="🎓" if item["role"] == "assistant" else "🧑"):
        st.write(item["content"])
        if item["role"] == "assistant" and show_intents and item.get("intent"):
            details = f'Intent: {item["intent"]} · Confidence: {item.get("confidence", 0):.0%}'
            if item.get("awaiting"):
                details += " · Waiting for details"
            st.caption(details)

incoming = st.chat_input("Ask ParentConnect anything about school…", max_chars=500, disabled=not configured)
new_text = selection or incoming
if new_text:
    st.session_state.messages.append({"role": "user", "content": new_text})
    with st.spinner("ParentConnect is thinking…"):
        try:
            result = ask_dialogflow(project_id, st.session_state.session_id, new_text, service_json)
            item = {"role": "assistant", "content": result.message,
                    "intent": result.intent, "confidence": result.confidence,
                    "awaiting": result.awaiting_input}
        except Exception as exc:
            item = {"role": "assistant", "content": helpful_error(exc), "intent": "Connection error"}
    st.session_state.messages.append(item)
    st.rerun()

st.markdown(
    '<div class="pc-foot">🔒 Privacy notice: This educational prototype does not access real school records. '
    'Never share names, roll numbers, passwords, payment information or other private details. '
    'Questions are processed by Google Dialogflow; this app does not save chat transcripts to a database.'
    '</div>', unsafe_allow_html=True,
)
