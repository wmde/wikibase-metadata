# Development

## Running Locally:

### Requirements

- Python version 3.12
- Docker
- npm

### Backend

Inside the `backend` directory:

1. Start a postgres instance with docker using:
```bash
$ docker run -d \
  --name postgres \
  -e POSTGRES_PASSWORD=app \
  -p 5432:5432 \
  postgres:16
```

2. Create a python virtual environment:
```bash
$ python3.12 -m venv .venv
$ source .venv/bin/activate
```

3. Install the requirements:
```bash
$ pip install -r requirements.txt && pip install -r requirements-dev.txt 
```

4. Run migrations:
```bash
$ alembic upgrade head
```

5. Start the server:
```bash
$ PYTHONPATH=. fastapi dev app.py
```


### Frontend

Inside the `frontend` directory:

1. Install dependencies:
```bash
$ npm ci
```

2. Start the app:
```bash
$ npm run dev
```

The UI should now be running on http://localhost:1573


## Testing Locally:

### Non-Data Tests

To run all non-data tests, run the following command:

```bash
$ PYTHONPATH=. SETTINGS_FILE=test-settings.ini pytest -m "not data"
```

You can run just a specific test using: 

```bash
$ PYTHONPATH=. SETTINGS_FILE=test-settings.ini pytest tests/test_query/<FILE_NAME>::<TEST_NAME>
```

To check test coverage when running tests:

```bash
$ PYTHONPATH=. SETTINGS_FILE=test-settings.ini pytest -m "not data" --cov=. --cov-report html:cov_html --order-dependencies
```

Here's a breakdown:

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
