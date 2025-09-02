import datetime
from typing import Annotated
import secrets
import os

from fastapi import FastAPI, Response, Cookie, Depends
from fastapi.staticfiles import StaticFiles

from .models import Activity, ActivitySubmission, SubmissionResponse, Submission
from .db import write_submission

app = FastAPI(docs_url=None)

STATIC_DIRECTORY = os.getenv("STATIC_DIRECTORY", "static/")


def get_session_id(
    response: Response, session_id: Annotated[str | None, Cookie()] = None
) -> str:
    if session_id is None:
        session_id = secrets.token_urlsafe(16)
        response.set_cookie(key="session_id", value=session_id)
    return session_id


@app.post("/api/submissions")
def grade_activity_submission(
    submission: ActivitySubmission, session_id: Annotated[str, Depends(get_session_id)]
) -> SubmissionResponse:
    activity = submission.decrypt_as(Activity)

    is_correct = submission.answer in activity.answers

    if activity.hints:
        hint_text = activity.hints.get(submission.answer)
    else:
        hint_text = None

    submission_data = Submission(
        activity_id=activity.identifier,
        session_id=session_id,
        answer=submission.answer,
        timestamp=datetime.datetime.now(datetime.UTC),
    )

    write_submission(submission_data)

    return SubmissionResponse(correct=is_correct, hint=hint_text)


app.mount("/", StaticFiles(directory=STATIC_DIRECTORY, html=True), name="static")
