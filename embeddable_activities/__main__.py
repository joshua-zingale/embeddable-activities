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

You may also use `store-key` to append a new key to an existent .env file or to create a new one if it doesn't exist.
The web server will automatically load the key from this file.

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


SERVING THE WEB SERVER
======================

To serve the web server, run the following command:
```
python3 -m embeddable_activities serve [host:port]
```
This will start the web server and load the secret key from the .env file.
"""

import sys
import os
from cryptography.fernet import Fernet
import pydantic
import json


def main():
    if len(sys.argv) < 2 and not (len(sys.argv) == 3 and sys.argv[1] == "serve"):
        print(__doc__)
        print(sys.argv)
        exit(0)
    match sys.argv[1]:
        case "generate-key":
            print(Fernet.generate_key().decode("utf-8"))
        case "store-key":
            with open(".env", "+a") as f:
                f.write(f"SECRET_KEY={Fernet.generate_key().decode('utf-8')}\n")
        case "encrypt":
            from .models import Activity, EncryptedPayload

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
        case "serve":
            if len(sys.argv) == 3:
                host, port = sys.argv[2].split(":")
            else:
                host, port = "0.0.0.0", "8000"
            os.execvp(
                "uvicorn",
                [
                    "uvicorn",
                    "embeddable_activities.app:app",
                    "--host",
                    host,
                    "--port",
                    port,
                ],
            )


if __name__ == "__main__":
    main()
