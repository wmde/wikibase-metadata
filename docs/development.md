# Development

## Running Locally:

### Bare metal

This definitely works on 3.10.12; other versions not guaranteed. Recommend using a python virtual environment.

Run the following in a bash terminal:

```bash
$ pip install -r requirements.txt
$ PYTHONPATH=. fastapi dev app.py
```

### Using docker

Install `docker` and `docker-compose-v2`.

```bash
docker compose up --build
```

The immediate output should include a reference to `http://127.0.0.1:8000`, which is localhost, port 8000. Navigating there in a browser should result in the simple JSON `{Hello: "World"}`.

Navigate to `http://127.0.0.1:8000/graphql`. This should include a simple interactive GraphiQL UI for querying and mutating data.

## Testing Locally:

### Non-Data Tests

To run all non-data tests, run the following command:

```bash
$ git restore data/wikibase-test-data.db && PYTHONPATH=. SETTINGS_FILE=test-settings.ini pytest -m "not data" --cov=. --cov-report html:cov_html --order-dependencies
```

Here's a breakdown:

- `git restore data/wikidata-test-data.db` -- The tests do not currently clean up after themselves, and as such data will be left in `data/wikibase-test-data.db` that must be reverted before the tests can be run.
- `PYTHONPATH=.` -- The gods alone know why, but this is necessary for fastapi
- `SETTINGS_FILE=test-settings.ini` -- directs the program to use test settings, which for the moment simply point it to the test database
- `pytest` -- the base command at the root of all of this: run the tests
- `-m "not data"` -- selects all tests that are not marked with `data`. There are many other markers for the tests; see [pytest.ini](../pytest.ini) for a complete list.
- `--cov=.` -- enable coverage checking; the coverage configuration can be found at [.coveragerc](../.coveragerc)
- `--cov-report html:cov_html` -- generates a report of coverage in HTML, which can be accessed in [the generated cov_html directory](../cov_html/index.html). Link will not work if you have not run the tests at least once.
- `--order-dependencies` -- test dependency will be taken into account when determining running order for tests. In our case, we use the data from testing observation creation to test our query structures and aggregation math.

### Data Tests

To run the data tests, run the following command:

```bash
$ pytest -m data
```
