"""Streamlit user interface for StudyMate AI."""

import streamlit as st

from assistant_core import StudyMateAssistant


st.set_page_config(
    page_title="StudyMate AI",
    page_icon="📚",
    layout="wide",
)

st.title("StudyMate AI – Your Personal Study Planner")
st.write(
    "Plan revision, divide study hours, and track exam dates with a friendly "
    "AI study assistant."
)

with st.sidebar:
    st.header("Gemini API")
    api_key = st.text_input(
        "Gemini API key",
        type="password",
        help="Your key is used only for requests during this browser session.",
    )
    st.markdown(
        "Get your own free API key from "
        "[Google AI Studio](https://aistudio.google.com/app/apikey)."
    )
    clear_chat = st.button("Clear Chat", use_container_width=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "assistant" not in st.session_state:
    st.session_state.assistant = None
if "assistant_key" not in st.session_state:
    st.session_state.assistant_key = None

if clear_chat:
    st.session_state.messages = []
    if st.session_state.assistant is not None:
        st.session_state.assistant.clear()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            tools_used = message.get("tools_used", [])
            with st.expander("Tools Used", expanded=False):
                if tools_used:
                    for tool_name in dict.fromkeys(tools_used):
                        st.write(f"- `{tool_name}`")
                else:
                    st.write("No custom tools used.")

if api_key:
    if (
        st.session_state.assistant is None
        or st.session_state.assistant_key != api_key
    ):
        try:
            st.session_state.assistant = StudyMateAssistant(api_key)
            st.session_state.assistant_key = api_key
            if len(st.session_state.messages) > 0:
                st.session_state.messages = []
        except Exception:
            st.error(
                "Could not initialize Gemini. Please check that the API key is valid."
            )
else:
    st.session_state.assistant = None
    st.session_state.assistant_key = None

user_input = st.chat_input("Ask StudyMate AI...")

if user_input:
    if not api_key:
        st.error("Please enter your Gemini API key in the sidebar first.")
    elif st.session_state.assistant is None:
        st.error("Gemini is unavailable. Please check your API key.")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        try:
            with st.chat_message("assistant"):
                with st.spinner("StudyMate AI is planning..."):
                    answer = st.session_state.assistant.respond(user_input)
                st.markdown(answer)
                tools_used = st.session_state.assistant.tools_used
                with st.expander("Tools Used", expanded=False):
                    if tools_used:
                        for tool_name in dict.fromkeys(tools_used):
                            st.write(f"- `{tool_name}`")
                    else:
                        st.write("No custom tools used.")

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "tools_used": tools_used,
                }
            )
        except Exception as exc:
            message = str(exc)
            friendly = (
                "The Gemini request failed. Please verify your API key, internet "
                "connection, or Gemini service availability."
            )
            if "API_KEY" in message.upper() or "401" in message or "403" in message:
                friendly = "Your Gemini API key appears invalid or unauthorized."
            st.error(friendly)
