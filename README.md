Embeddable Activities is a light-weight web server that facilitates embedding activities directly into static HTML pages,
all while avoiding leaking solutions to activities in the HTML source.


## How Does It Work?
The web server does not store any of the activities itself.
Instead, activities are placed directly into the HTML of a webpage and the webserver only grades submissions made for the activity,
responding with a boolean indicating the correctness of the submission and, optionally, a hint message corresponding to the submission.
For this to work, each submission must contain the submission along with the activity data, i.e. the answer.

One problem with embedding activities directly into HTML is that users could inspect the source to dirive the correct answer for the activity.
To close this security hole, the web server accepts encrypted activity data.
Therefore, inspecting the HTML source would only reveal an uninterpretable encrypted string.


## Usage

The module is executable with

```bash
python3 -m embeddable_activities
```

The script has multiple commands.


### Key Generation

To generate a key, pass in the argument "generate-key".
For example, you could use
```bash
python3 -m embeddable_activities generate-key
```
This key may be used to set the SECRET_KEY environment variable for the web server.
If thus used, do not share the key with anyone.

You may also use `store-key` to append a new key to an existent .env file or to create a new one if it doesn't exist.
The web server will automatically load the key from this file.

```bash
python3 -m embeddable_activities store-key
```

### Activity Encryption

To encrypt an activity, pass in the argument `encrypt` as the first argument.
The activity to be encrypted should be entered via the standard input as a JSON object.
The encrypted activity will be printed to the standard output and can be embedded directly
into a website.
For example, you could use
```bash
echo '{"identifier":"activity-1", "answers":["George Washington"], "hints": {"Donald Trump": "Wrong!"}}' | python3 -m embeddable_activities encrypt
```
This will print the encrypted activity to the standard output.


### Serving

To serve the web server, run the following command:
```bash
python3 -m embeddable_activities serve [host:port]
```
This will start the web server and load the secret key from the .env file.

## Examples

In the `static/` directory is a multiple-choice question that uses the system.
Included are an html page alongside a javascript file and a JSON file containing the question information.
To run the example, you need to generate a key as with

```bash
python3 -m embeddable_activities store-key
```

Then, you must encrypt the JSON, which can be done with

```bash
cat example_activities/multiple-choice.json | python3 -m embeddable_activities encrypt
```

Next, copy and paste the encryped question string into both of the `activity=` attributes in `example_activities/multiple-choice.html`.

Finally, you can serve the web server with

```bash
python3 -m embeddable_activities serve
```

static files are hosted at `host:port/`.

For more serious use, you would of course want to automate the pipeline of encrypting questions: this is only an example to demonstrate the web-server's functionality.