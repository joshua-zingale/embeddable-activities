import json
from typing import Type, TypeVar
from dotenv import load_dotenv
import os

from pydantic import BaseModel, Field
from cryptography.fernet import Fernet

from dotenv import load_dotenv
import os

load_dotenv()
master_key = os.environ["SECRET_KEY"].encode("utf-8")


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
