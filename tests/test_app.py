
from fastapi.testclient import TestClient
from embeddable_activities.models import EncryptedPayload
import json
def test_encrypt_and_grade_and_session(client: TestClient):
    activity_json = {
        "identifier": "activity-1",
        "answers": ["correct 1", "correct 2"],
        "hints": {"correct 1": "Hint for correct1"},
        "activity_metadata": {"question": "Quess the answer"}
        }
    



    ecrypted_activity = EncryptedPayload.from_plaintext(json.dumps(activity_json)).encrypted_data.decode("utf-8")

    assert client.cookies.get('activity-activity-1') is None


    response = client.post("/", json = {
        "answer": "incorrect",
        "encrypted_data": ecrypted_activity,
        })
    
    submission_response = response.json()

    assert not submission_response['correct']
    assert submission_response['hint'] is None
    assert client.cookies.get('activity-activity-1') is None

    response = client.post("/", json = {
        "answer": "correct 1",
        "encrypted_data": ecrypted_activity,
        })
    
    submission_response = response.json()

    assert submission_response['correct']
    assert submission_response['hint'] == "Hint for correct1"
    assert client.cookies.get('activity-activity-1') == 'true'


    response = client.post("/", json = {
        "answer": "correct 2",
        "encrypted_data": ecrypted_activity,
        })
    
    submission_response = response.json()

    assert submission_response['correct']
    assert submission_response['hint'] is None
    assert client.cookies.get('activity-activity-1') == 'true'