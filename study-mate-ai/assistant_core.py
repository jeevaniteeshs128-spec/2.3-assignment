"""Gemini-powered conversational assistant core."""

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_google_genai import ChatGoogleGenerativeAI

from tools import TOOLS


SYSTEM_PROMPT = """You are StudyMate AI, a friendly and practical college study planner.
Help students organize revision, manage exam preparation, and divide study time.
Use the provided custom tools whenever date calculations or study-hour calculations are needed.
Remember previous conversation messages and refer to previously mentioned subjects, exam dates, and study hours.
Give concise, structured answers and never invent tool results.
Admit when a tool fails. Politely refuse unrelated questions outside study planning.
Never pretend to access calendars, files, or external websites.
Never give medical, legal, or financial advice."""


class StudyMateAssistant:
    """Manage Gemini chat history and custom tool calls."""

    MAX_STEPS = 6
    MAX_HISTORY = 20

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.history = []
        self.tools_used = []
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.3,
        ).bind_tools(TOOLS)
        self.tool_by_name = {tool.name: tool for tool in TOOLS}

    def clear(self) -> None:
        """Clear all remembered conversation messages."""
        self.history = []
        self.tools_used = []

    def respond(self, user_message: str) -> str:
        """Get a final response and execute at most MAX_STEPS tool calls."""
        self.tools_used = []
        messages = [SystemMessage(content=SYSTEM_PROMPT), *self.history,
                    HumanMessage(content=user_message)]

        for _ in range(self.MAX_STEPS):
            response = self.model.invoke(messages)
            tool_calls = getattr(response, "tool_calls", None) or []

            if not tool_calls:
                text = response.content if isinstance(response.content, str) else ""
                if not text and isinstance(response.content, list):
                    text = "".join(
                        part.get("text", "")
                        for part in response.content
                        if isinstance(part, dict)
                    )
                final_text = text.strip() or "I could not produce a text answer."
                self.history.append(HumanMessage(content=user_message))
                self.history.append(AIMessage(content=final_text))
                if len(self.history) > self.MAX_HISTORY:
                    self.history = self.history[-self.MAX_HISTORY:]
                return final_text

            messages.append(response)
            for tool_call in tool_calls:
                name = tool_call.get("name", "")
                args = tool_call.get("args", {}) or {}
                tool_call_id = tool_call.get("id", name)
                tool_instance = self.tool_by_name.get(name)

                if tool_instance is None:
                    result = f"Tool '{name}' is not available."
                else:
                    self.tools_used.append(name)
                    try:
                        result = tool_instance.invoke(args)
                    except Exception as exc:
                        if name == "create_study_schedule":
                            result = (
                                "Please enter a valid positive number of study "
                                "hours and at least one subject."
                            )
                        elif name == "days_until_exam":
                            result = (
                                "Please provide a valid exam date in "
                                "YYYY-MM-DD format."
                            )
                        else:
                            result = f"The {name} tool failed: {exc}"

                messages.append(
                    ToolMessage(content=str(result), tool_call_id=tool_call_id)
                )

        return "I reached the tool-use limit before completing that request."
