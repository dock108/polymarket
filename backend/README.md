# Backend (FastAPI)

- App factory, services, and API routes live here.
- Python 3.11+, FastAPI, SQLAlchemy, Pydantic, httpx.

## Tests & Lint

```bash
# from backend/
source .venv/bin/activate
pip install -r requirements.txt
pytest -q

# optional: black/flake8
python -m black .
python -m flake8
```
