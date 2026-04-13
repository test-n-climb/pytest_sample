# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Start the mock service (required before running tests locally)
python -m mock_service.main

# Run tests
pytest -m "task_api" --env mock          # directly
poe test_task_api                        # via poe shortcut

# Run a single test
pytest tests/test_task_api.py::TestCreateTask::test_create_task --env mock

# Allure report
poe report

# Linting / formatting
poe lint
poe format
poe sort
```

## Architecture

**Two independent layers:** a Flask mock service (`mock_service/`) and the pytest test framework (`src/`, `tests/`).

### Test framework

- **`Config`** (`config/config.py`) — singleton initialized once per session in `conftest.pytest_sessionstart`. Reads env vars from `.env.<env>` for `mock`/`local` envs, or from `config/<env>.ini` + AWS Secrets Manager for remote envs. Always pass `--env <name>` when running pytest.

- **`BaseApiClient`** (`src/clients/api_clients/`) — abstract HTTP client. All HTTP methods are decorated by `ApiCallInterceptor.process_request`, which handles request/response logging and retry logic. The `is_response_expected` callable controls the retry condition; by default retries until `response.ok`, but stops early on 4xx.

- **`BaseTestDataFactory`** (`src/test_data_factories/`) — Faker-based factory pattern. Subclasses implement `get_defaults()` and optionally `get_optional_fields()`. Call `factory.build(overrides)` for required-fields-only payloads, or `factory.build_with_optional_fields(overrides)` to include optional fields. Both accept a partial dict that deep-merges over defaults.

- **Test structure** — Tests are class-based, marked with `@pytest.mark.task_api` and `@allure.feature/story`. Fixtures are session-scoped where possible (`task_api_client`). `pytest.ini` configures 5-worker xdist parallelism and Allure output by default.

### Mock service

Flask app using SQLAlchemy with a per-request DB session (`get_db()` via Flask `g`). Business logic lives in resolver classes under `mock_service/resolvers/` — add a resolver there and register the route in `mock_service/main.py`. Response shape is always `ResponseContent(success, data|errors)` from `mock_service/schemas/response.py`.
