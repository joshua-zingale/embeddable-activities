"""Either generates a secret key or encrypts an Activity with the secrety key stored in the SECRET_KEY environment variable.
If the first argument is "generate-key", generates a Fernet Key and prints a utf-8 string of it to the standard output.


KEY GENERATION
==============

To generate a key, pass in the argument "generate-key".
For example, you could use
```
python3 -m embeddable_activities generate-key
```
This key may be used to set the SECRET_KEY environment variable for the web server.
If thus used, do not share the key with anyone.


ACTIVITY ENCRYPTING
===================

To encrypt an activity, pass in the argument "encrypt" as the first argument.
The activity to be encrypted should be entered via the standard input as a JSON object.
The encrypted activity will be printed to the standard output and can be embedded directly
into a website.
For example, you could use
```
echo '{"identifier":"activity-1", "answers":["George Washington"], "hints": {"Donald Trump": "Wrong!"}}' | python3 -m embeddable_activities encrypt
```
This will print the encrypted activity to the standard output.

"""

import sys
from sys import argv
from cryptography.fernet import Fernet
from .models import Activity, EncryptedPayload
import pydantic
import json


def main():
    if len(argv) != 2:
        print(__doc__)
        exit(0)
    match argv[1]:
        case "generate-key":
            print(Fernet.generate_key().decode("utf-8"))
        case "encrypt":
            raw_activity = sys.stdin.read()

            try:
                encrypted_payload = EncryptedPayload.from_plaintext(
                    Activity(**json.loads(raw_activity)).model_dump_json()
                )
            except json.JSONDecodeError as e:
                print(
                    "Encountered an error when parsing the input as JSON:",
                    e,
                    file=sys.stderr,
                )
                exit(1)
            except TypeError as e:
                print(
                    "The input JSON is not a valid Activity: JSON must be a dictionary."
                )
                exit(1)
            except pydantic.ValidationError as e:
                print("The input JSON is not a valid Activity:", e)
                exit(1)

            print(encrypted_payload.encrypted_data.decode("utf-8"), end="")


if __name__ == "__main__":
    main()
