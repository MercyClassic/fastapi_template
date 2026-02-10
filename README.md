# FastAPI Project Template

A template repository for quickly starting **FastAPI** projects with a modern Python stack and strict code quality settings.

## 🚀 Tech Stack

- Python 3.11+
- FastAPI
- Pydantic v2
- SQLAlchemy 2.0
- Alembic
- PostgreSQL (psycopg3)
- Uvicorn / Gunicorn
- Dishka

## 🧹 Code Quality

- Ruff — linter and formatter (auto-fix enabled)
- Mypy — strict static type checking
- Pytest + pytest-asyncio — testing
- Pre-commit — automated checks before commits

## 📁 Project Structure

Application code is located in the `src/` directory.
Tests are located in the `tests/` directory.

## ⚙️ Installation

```bash
poetry install
```

## ▶️ Running the App

```bash
uvicorn src.main:app --reload
```

## 🧪 Running Tests

```bash
pytests -s -v tests/
```
