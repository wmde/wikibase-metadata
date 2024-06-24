### Running Locally:

This definitely works on 3.10.12; other versions not guaranteed. Recommend using a python virtual environment.

Run the following:

`bash 
$ pip install -r requirements.txt
$ PYTHONPATH=. fastapi dev app.py
`

The immediate output should include a reference to `http://127.0.0.1:8000`, which is localhost, port 8000. Navigating there in a browser should result in the simple JSON `{Hello: "World"}`.

Navigate to `http://127.0.0.1:8000/graphql`. This should include a simple interactive GraphiQL UI for querying and mutating data.
