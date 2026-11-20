# StudyMate AI

StudyMate AI is a simple, beginner-friendly AI study planning assistant for college students. It uses Google's Gemini API and LangChain tool calling to calculate exam countdowns and divide available study time across subjects.

## Problem Statement

Students often need to combine exam deadlines, limited available time, and multiple subjects into a practical revision plan. StudyMate AI provides a chat interface that helps organize that information quickly.

## Features

- Natural-language study planning
- Exam countdown calculations
- Equal subject-wise study-hour schedules
- Multi-turn conversation memory
- Gemini tool calling
- A clear list of tools used for each answer
- Visitor-provided API keys
- Clear Chat control

## Technology Stack

- Python
- Streamlit
- Google Gemini API
- LangChain
- Python `datetime`

## Project Structure

```text
study-mate-ai/
├── app.py
├── assistant_core.py
├── tools.py
├── requirements.txt
├── .gitignore
├── README.md
└── tests.md
```

## Custom Tools

### `days_until_exam(exam_date: str)`

Accepts a date in `YYYY-MM-DD` format and calculates the number of calendar days remaining. It handles invalid dates and past dates.

### `create_study_schedule(total_hours: float, subjects: str)`

Accepts a positive number of hours and comma-separated subject names, then divides the hours equally and produces a subject-wise schedule.

## Conversation Memory

The assistant keeps recent `HumanMessage` and `AIMessage` entries in Streamlit session state. It sends that history back to Gemini with each new prompt and limits retained messages with `MAX_HISTORY`. Changing the API key or using Clear Chat resets the conversation.

## Gemini Tool Calling

The two functions in `tools.py` are registered in `TOOLS`. `assistant_core.py` binds the list to a Gemini chat model. When Gemini requests a tool, the assistant executes it locally and sends a `ToolMessage` containing the result back to Gemini. A `MAX_STEPS` loop prevents excessive tool calls.

## Installation

Python 3.10 or newer is recommended.

```powershell
cd "study-mate-ai"
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Obtain a Gemini API Key

1. Open [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Sign in with a Google account.
3. Create an API key.
4. Keep the key private and do not place it in source code.

## Run Locally

```powershell
streamlit run app.py
```

Enter your own Gemini API key in the sidebar. The key is used only for current-session API requests.

## Deploy with Streamlit Community Cloud

1. Push this project to a public or private GitHub repository.
2. Open [Streamlit Community Cloud](https://share.streamlit.io).
3. Sign in and select **Create app**.
4. Choose the GitHub repository, branch, and `app.py`.
5. Deploy the app.

Do not add a real API key to Streamlit Secrets or repository files. Visitors enter their own key in the app sidebar.

## Security Considerations

- Never commit API keys or personal credentials.
- Never put API keys in screenshots, logs, or source code.
- Use the sidebar password field rather than a hardcoded key.
- This app does not use a database or intentionally store visitor keys.

## Reflection Questions

1. What did you learn while building this assistant?
2. What would you improve in the next version?
