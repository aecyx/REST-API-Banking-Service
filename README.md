# Project 4: RESTful Banking Service API

## Overview

Build a RESTful API that simulates core banking operations — account management, transfers, and transaction history. This project focuses on API design, input validation, concurrency safety, and testing — all critical skills for backend Python development at JP Morgan.

## Requirements

### Phase 1: API Design and Account Management
- Build a REST API using **FastAPI** (or Flask if you prefer) with the following endpoints:
  - `POST /accounts` — Create a new account (name, account type, initial balance)
  - `GET /accounts/{account_id}` — Get account details
  - `GET /accounts` — List all accounts with pagination (limit/offset query params)
  - `PUT /accounts/{account_id}` — Update account details (name, status)
  - `DELETE /accounts/{account_id}` — Soft-delete an account (mark inactive, don't remove data)
- Use Pydantic models (if FastAPI) or dataclasses for request/response validation:
  - Validate account names (non-empty, max length)
  - Validate balances (non-negative for creation)
  - Validate account types (checking, savings, investment)
  - Return clear, structured error responses for validation failures
- Store data in SQLite with a clean schema

### Phase 2: Transactions and Transfers
- Add transaction endpoints:
  - `POST /accounts/{account_id}/deposit` — Deposit funds
  - `POST /accounts/{account_id}/withdraw` — Withdraw funds (must check sufficient balance)
  - `POST /transfers` — Transfer between two accounts (atomic operation)
  - `GET /accounts/{account_id}/transactions` — Get transaction history with filters (date range, type, min/max amount)
- Every transaction must:
  - Be recorded with a unique transaction ID, timestamp, type, amount, and resulting balance
  - Be atomic — a failed transfer must not partially execute (both accounts update or neither does)
  - Validate that accounts are active before allowing operations
- Implement proper HTTP status codes: 200, 201, 400, 404, 409, 422, 500

### Phase 3: Authentication and Rate Limiting
- Implement basic API key authentication:
  - Require an `X-API-Key` header on all requests
  - Store valid API keys in the database
  - Return 401 for missing keys and 403 for invalid keys
- Implement rate limiting:
  - Track requests per API key using an in-memory counter (or SQLite)
  - Limit to N requests per minute (configurable)
  - Return 429 Too Many Requests when limit is exceeded
  - Include `Retry-After` header in 429 responses

### Phase 4: Logging, Error Handling, and Documentation
- Implement structured logging for all API requests:
  - Log method, path, status code, response time, API key (masked)
  - Use Python's `logging` module with a JSON formatter
- Create a global exception handler that:
  - Catches unhandled exceptions and returns a generic 500 response
  - Logs the full traceback without exposing it to the client
  - Handles known exceptions (validation errors, not found, etc.) with appropriate status codes
- Generate API documentation:
  - If using FastAPI: the auto-generated OpenAPI docs at `/docs` count
  - If using Flask: write a clear API reference in a separate DOCS.md file

### Phase 5: Testing
- Write integration tests for every endpoint using `pytest` and the framework's test client
- Test happy paths and error cases:
  - Creating accounts with valid and invalid data
  - Transfers with sufficient and insufficient funds
  - Concurrent transfer safety (simulate two transfers from the same account)
  - Authentication with valid, invalid, and missing API keys
  - Rate limiting behavior
- Use fixtures for test database setup and teardown

## Acceptance Criteria
- [ ] All CRUD endpoints work correctly with proper HTTP status codes
- [ ] Transfers are atomic — no partial execution on failure
- [ ] Input validation returns clear error messages
- [ ] API key authentication works correctly
- [ ] Rate limiting is enforced per API key
- [ ] Structured logging captures all request/response metadata
- [ ] Integration tests cover happy paths and edge cases
- [ ] API documentation is available and accurate

## Technical Constraints
- Allowed libraries: `fastapi`, `uvicorn`, `pydantic`, `sqlite3` (built-in), `pytest`, `httpx` (for async test client) — OR `flask`, `pytest`, `requests`
- Do NOT use an ORM (SQLAlchemy, etc.) — write SQL directly to demonstrate database skills
- Do NOT use external authentication services — implement key-based auth yourself

## Suggested Project Structure
```
rest-api-banking-service/
    src/
        __init__.py
        app.py
        models/
            __init__.py
            schemas.py
        routes/
            __init__.py
            accounts.py
            transactions.py
            transfers.py
        middleware/
            __init__.py
            auth.py
            rate_limiter.py
            logging_middleware.py
        database/
            __init__.py
            connection.py
            queries.py
            migrations.py
        exceptions.py
    tests/
        __init__.py
        conftest.py
        test_accounts.py
        test_transactions.py
        test_transfers.py
        test_auth.py
        test_rate_limiting.py
    config.yaml
    main.py
    requirements.txt
    README.md
```

## Resources

### FastAPI
- FastAPI Official Tutorial — https://fastapi.tiangolo.com/tutorial/
- FastAPI Path Parameters — https://fastapi.tiangolo.com/tutorial/path-params/
- FastAPI Request Validation — https://fastapi.tiangolo.com/tutorial/body/
- Pydantic Documentation — https://docs.pydantic.dev/latest/

### Flask (Alternative)
- Flask Official Tutorial — https://flask.palletsprojects.com/en/stable/tutorial/
- Flask RESTful API — https://flask.palletsprojects.com/en/stable/views/

### API Design
- REST API Best Practices — https://restfulapi.net/
- HTTP Status Codes Reference — https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
- Real Python: API Design — https://realpython.com/api-integration-in-python/

### Database and SQL
- SQLite3 Python docs — https://docs.python.org/3/library/sqlite3.html
- Real Python: SQLite in Python — https://realpython.com/python-sqlite-sqlalchemy/#working-with-sqlite-in-python
- SQL Transactions and Atomicity — https://www.sqlite.org/lang_transaction.html

### Testing APIs
- Real Python: Testing FastAPI — https://realpython.com/courses/testing-fastapi-applications/
- FastAPI Testing docs — https://fastapi.tiangolo.com/tutorial/testing/
- pytest fixtures — https://docs.pytest.org/en/stable/how-to/fixtures.html

## Why This Matters for JP Morgan
Backend API development is core to JP Morgan's technology stack. They build internal and client-facing APIs that handle enormous transaction volumes. This project demonstrates you can design clean APIs, handle financial data safely (atomic transactions), implement security basics, and write thorough tests — all expectations for Python developers at the firm.
