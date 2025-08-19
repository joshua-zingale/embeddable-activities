Embeddable Activities is a light-weight web server that facilitates embedding activities directly into static HTML pages,
all while avoiding leaking solutions to activities in the HTML source.


## How Does It Work?
The web server does not store any of the activities itself.
Instead, activities are placed directly into the HTML of a webpage and the webserver only grades submissions made for the activity,
responding with a boolean indicating the correctness of the submission and, optionally, a hint message corresponding to the submission.
For this to work, each submission must contain the submission along with the activity data, i.e. the answer.

One problem with embedding activities directly into HTML is that user's could inspect the source to dirive the correct answer for the activity.
To close this security hole, the web server accepts encrypted activity data.
Therefore, inspecting the HTML source would only reveal an uninterpretable encrypted string.