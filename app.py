import streamlit as st

api_key = st.secrets["GOOGLE_API_KEY"]

from ai_engine import generate_response
from prompts import explanation_prompt, summary_prompt, quiz_prompt, pdf_explanation_prompt
from pdf_utils import extract_text_from_pdf


# PAGE CONFIG

st.set_page_config(page_title="AI Study Buddy", page_icon="🤖", layout="wide")


# SESSION STATE INIT

defaults = {
    "messages": [],
    "last_topic": None,
    "last_pdf_text": None,
    "last_pdf_name": None,
    "generating": False,
    "pending_prompt": None,
    "uploader_version": 0,
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val


# SIDEBAR

with st.sidebar:
    st.markdown("## ⚙️ Settings")

    mode = st.selectbox("Mode", ["Explain", "Summarize", "Quiz"])
    level = st.selectbox("Explanation Level", ["Beginner", "Intermediate", "Exam-Ready"])

    st.markdown("---")
    st.markdown("### 📄 Upload PDF Notes")

    uploaded_pdf = st.file_uploader("Drop a PDF here", type=["pdf"], label_visibility="collapsed", key=f"pdf_uploader_{st.session_state.uploader_version}")

    if uploaded_pdf is not None:
        if uploaded_pdf.name != st.session_state.last_pdf_name:
            with st.spinner("Reading PDF…"):
                pdf_text = extract_text_from_pdf(uploaded_pdf)
            if pdf_text:
                st.session_state.last_pdf_text = pdf_text
                st.session_state.last_pdf_name = uploaded_pdf.name
                st.session_state.last_topic = None
                st.success(f"✅ {uploaded_pdf.name} loaded!")
            else:
                st.error("❌ Could not extract text from this PDF.")

    
    else:
    
        if st.session_state.last_pdf_text is not None:
            st.session_state.last_pdf_text = None
            st.session_state.last_pdf_name = None

    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_topic = None
        st.session_state.last_pdf_text = None
        st.session_state.last_pdf_name = None
        st.session_state.pending_prompt = None
        st.session_state.generating = False
        st.session_state.uploader_version += 1
        st.rerun()


# HEADER

st.title("🤖 AI Study Buddy")
st.caption("Your personal AI-powered learning assistant")
st.divider()


# INPUT

input_col, btn_col = st.columns([5, 1], vertical_alignment="bottom")
with input_col:
    topic = st.text_input("Enter a topic", placeholder="e.g., binary search, neural networks…", label_visibility="collapsed")
with btn_col:
    generate_clicked = st.button("Generate ✨", type="primary", use_container_width=True, disabled=st.session_state.generating)


# CHAT HISTORY DISPLAY

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# HELPERS


def detect_mode_override(text: str, default: str) -> str:
    t = text.lower()
    if "quiz" in t:
        return "Quiz"
    if any(w in t for w in ("summarize", "summary", "summarise")):
        return "Summarize"
    if "explain" in t:
        return "Explain"
    return default


def build_prompt(user_text: str, active_mode: str, active_level: str):
    if st.session_state.last_pdf_text:
        final_mode = detect_mode_override(user_text, active_mode)
        return pdf_explanation_prompt(st.session_state.last_pdf_text[:12000], final_mode)

    if st.session_state.last_topic:
        final_mode = detect_mode_override(user_text, active_mode)
        if final_mode == "Explain":
            return explanation_prompt(st.session_state.last_topic, active_level)
        if final_mode == "Summarize":
            return summary_prompt(st.session_state.last_topic)
        return quiz_prompt(st.session_state.last_topic)

    return None


def call_ai(core_prompt: str) -> str:
    recent = st.session_state.messages[-10:]
    history_text = "\n".join(f"{m['role'].upper()}: {m['content']}" for m in recent)
    full_prompt = f"Previous conversation:\n{history_text if history_text else '(none yet)'}\n---\n{core_prompt}"
    return generate_response(full_prompt)


def render_ai_response(response: str):
    if response == "__SERVER_BUSY__":
        st.warning("⚠️ AI is busy right now. Try again shortly.")
        return False
    if response == "__API_ERROR__":
        st.error("❌ AI service error. Please retry.")
        return False
    if response == "__UNKNOWN_ERROR__":
        st.error("❌ Unexpected error occurred.")
        return False

    st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    return True


# FREEZE REQUEST WHEN BUTTON CLICKED

if generate_clicked and not st.session_state.generating:
    if not topic.strip() and not st.session_state.last_pdf_text:
        st.warning("⚠️ Please enter a topic or upload a PDF first.")
        st.stop()

    frozen_topic = topic.strip()

    if frozen_topic:
        st.session_state.last_topic = frozen_topic
        st.session_state.last_pdf_text = None
        st.session_state.last_pdf_name = None

    user_display = frozen_topic if frozen_topic else f"[PDF: {st.session_state.last_pdf_name}] — {mode}"
    st.session_state.pending_prompt = (user_display, mode, level)
    st.session_state.generating = True
    st.rerun()


# PROCESS PENDING REQUEST SAFELY

if st.session_state.generating and st.session_state.pending_prompt:
    user_display, mode, level = st.session_state.pending_prompt

    
    st.session_state.messages.append({"role": "user", "content": user_display})
    user_index = len(st.session_state.messages) - 1

    core_prompt = build_prompt(user_display, mode, level)

    success = False

    try:
        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                response = call_ai(core_prompt)
                success = render_ai_response(response)

    
        if not success:
            st.session_state.messages.pop(user_index)

    finally:
        st.session_state.generating = False
        st.session_state.pending_prompt = None

        if success:
            st.rerun()


# FOLLOW-UP CHAT INPUT (ONLY QUEUES REQUEST)

user_followup = st.chat_input(
    "Ask a follow-up question…",
    disabled=st.session_state.generating
)

if user_followup:
    # If nothing to reference yet
    if not st.session_state.last_topic and not st.session_state.last_pdf_text and not st.session_state.messages:
        st.warning("Start by generating a topic or uploading a PDF first.")
        st.stop()

    # Queue request — DO NOT write message here
    st.session_state.pending_prompt = (user_followup, mode, level)
    st.session_state.generating = True
    st.rerun()