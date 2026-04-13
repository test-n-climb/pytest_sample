# pytest_sample

Sample API tests using pytest against a mock Flask service.

## Description

Demonstrates an API test framework built with pytest, targeting a locally-run mock Task API. The mock service exposes endpoints to create and retrieve tasks, backed by a database. Tests run in parallel via `pytest-xdist` and produce Allure reports.

## How to Run

### 1. Start the mock service

```bash
python -m mock_service.main
```

The mock runs at `http://127.0.0.1:5000` by default.

### 2. Run the tests

```bash
# Run all task API tests
pytest -m "task_api" --env mock

# Or use the poe shortcut
poe test_task_api
```

### 3. View the Allure report

```bash
poe report
```

## Project Structure

```
pytest_sample/
├── config/                         # Environment and app configuration
│   ├── config.py                   # Config singleton
│   ├── environment.py              # Environment name enum
│   └── secret_manager.py           # Secrets/env var loading
│
├── mock_service/                   # Flask mock API
│   ├── main.py                     # App entry point (routes)
│   ├── db/                         # SQLAlchemy DB layer
│   └── resolvers/                  # Request handler logic
│
├── src/
│   ├── clients/api_clients/        # HTTP client wrappers
│   │   ├── base_api_client.py      # Base client
│   │   ├── task_api_client.py      # Task API client
│   │   └── api_call_interceptor.py # Request/response interceptor (logging, retries)
│   ├── schemas/                    # Pydantic response schemas
│   ├── test_data_factories/        # Faker-based input factories
│   └── utils/                      # Helpers, decorators, wait utils
│
├── tests/
│   ├── conftest.py                 # Fixtures and session setup
│   └── test_task_api.py            # Task API test cases
│
├── .env.mock                       # Env vars for local mock run
├── pytest.ini                      # pytest config (markers, xdist, Allure)
└── pyproject.toml                  # Dependencies and poe tasks
```
