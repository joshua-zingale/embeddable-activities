import json
import secrets
from typing import Annotated, Type, TypeVar
from dotenv import load_dotenv
import os


from fastapi import FastAPI, Response, Cookie, Request
from pydantic import BaseModel, Field
from cryptography.fernet import Fernet

load_dotenv()

app = FastAPI()

master_key = os.environ["SECRET_KEY"].encode('utf-8')


class EncryptedPayload(BaseModel):
    """Fernet Encrypted Data"""

    encrypted_data: bytes

    @staticmethod
    def from_plaintext(text: str):
        return EncryptedPayload(
            encrypted_data=Fernet(master_key).encrypt(text.encode("utf-8"))
        )

    _T = TypeVar("_T", bound=BaseModel)

    def decrypt_as(self, model_type: Type[_T]) -> _T:
        return model_type(
            **json.loads(
                Fernet(master_key).decrypt(self.encrypted_data).decode("utf-8")
            )
        )


class Activity(BaseModel):
    # Identifier should be a valid cookie name
    identifier: str = Field(pattern=r"^[\w\d\-_]+$")
    answers: list[str]
    hints: dict[str, str] | None = None
    activity_metadata: dict | None = None


class ActivitySubmission(EncryptedPayload):
    answer: str


class SubmissionResponse(BaseModel):
    correct: bool
    hint: str | None


def get_session_id(
    response: Response, session_id: Annotated[str | None, Cookie()] = None
) -> str:
    if session_id is None:
        session_id = secrets.token_urlsafe(16)
        response.set_cookie(key="session_id", value=session_id)
    return session_id


@app.post("/api/v1/activity/encrypt")
def encrypt_activity(activity: Activity) -> EncryptedPayload:
    """Encrypt an activity for embedding in a client."""
    activity_json = activity.model_dump_json()
    return EncryptedPayload.from_plaintext(activity_json)


@app.get("/api/v1/activity/completion-status")
def activity_completion_status(request: Request, identifier: str) -> bool:
    value = request.cookies.get(get_activity_cookie_name(identifier))
    if value is None:
        return False
    return value.lower() == "true"


@app.post("/api/v1/submission/grade")
def grade_activity_submission(
    response: Response, submission: ActivitySubmission
) -> SubmissionResponse:
    activity = submission.decrypt_as(Activity)

    is_correct = submission.answer in activity.answers

    if activity.hints:
        hint_text = activity.hints.get(submission.answer)
    else:
        hint_text = None

    if is_correct:
        response.set_cookie(get_activity_cookie_name(activity.identifier), "true")

    return SubmissionResponse(correct=is_correct, hint=hint_text)


def get_activity_cookie_name(identifier: str):
    return f"activity-{identifier}"