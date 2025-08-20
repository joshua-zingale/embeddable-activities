from typing import Annotated
import secrets
from fastapi import FastAPI, Response, Cookie

from .models import Activity, ActivitySubmission, SubmissionResponse


app = FastAPI()


def get_session_id(
    response: Response, session_id: Annotated[str | None, Cookie()] = None
) -> str:
    if session_id is None:
        session_id = secrets.token_urlsafe(16)
        response.set_cookie(key="session_id", value=session_id)
    return session_id


@app.post("/")
def grade_activity_submission(submission: ActivitySubmission) -> SubmissionResponse:
    activity = submission.decrypt_as(Activity)

    is_correct = submission.answer in activity.answers

    if activity.hints:
        hint_text = activity.hints.get(submission.answer)
    else:
        hint_text = None

    return SubmissionResponse(correct=is_correct, hint=hint_text)
