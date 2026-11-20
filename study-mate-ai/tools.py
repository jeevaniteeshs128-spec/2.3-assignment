"""Custom tools used by the StudyMate AI assistant."""

from datetime import date, datetime
from langchain_core.tools import tool


@tool
def days_until_exam(exam_date: str) -> str:
    """Calculate the number of calendar days remaining until an exam date."""
    if not isinstance(exam_date, str) or not exam_date.strip():
        return "Please provide an exam date in YYYY-MM-DD format."

    try:
        exam = datetime.strptime(exam_date.strip(), "%Y-%m-%d").date()
    except ValueError:
        return "Invalid date. Please use YYYY-MM-DD, for example 2026-12-15."

    today = date.today()
    difference = (exam - today).days
    if difference < 0:
        return f"The exam date {exam.isoformat()} has already passed."
    if difference == 0:
        return "Your exam is today."
    if difference == 1:
        return "1 day remains until your exam."
    return f"{difference} days remain until your exam."


@tool
def create_study_schedule(total_hours: float, subjects: str) -> str:
    """Divide available study hours equally across a comma-separated subject list."""
    try:
        hours = float(total_hours)
    except (TypeError, ValueError):
        return "Please enter a valid positive number of study hours."

    if hours <= 0:
        return "Study hours must be positive."

    if not isinstance(subjects, str) or not subjects.strip():
        return "Please provide at least one subject."

    subject_names = [name.strip() for name in subjects.split(",") if name.strip()]
    if not subject_names:
        return "Please provide at least one non-empty subject name."

    per_subject = hours / len(subject_names)
    lines = [
        f"Study schedule ({hours:g} hours total)",
        f"Each subject gets {per_subject:g} hours:",
    ]
    lines.extend(
        f"- {subject_name}: {per_subject:g} hours"
        for subject_name in subject_names
    )
    return "\n".join(lines)


TOOLS = [days_until_exam, create_study_schedule]
