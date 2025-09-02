import json
from pathlib import Path
import os

import portalocker

from .models import Submission

DB_PATH = Path(os.getenv("DB_PATH", "db/submissions.jsonl"))
os.makedirs(DB_PATH.parent, exist_ok=True)


def write_submission(data: Submission):
    with portalocker.Lock(DB_PATH, "a", timeout=10) as log_file:
        log_file.write(data.model_dump_json() + "\n")
