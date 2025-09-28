# Local Development Runbook

## Backend
1. Create venv & install deps
```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```
2. Configure environment
```bash
cp ../.env.example ../.env
# edit values as needed (ODDS_API_KEY required for sportsbook join)
```
3. Run API
```bash
./dev.sh
# http://localhost:8000/health
# http://localhost:8000/api/opportunities
# http://localhost:8000/api/opportunities/meta
# http://localhost:8000/api/odds/{sport}
# http://localhost:8000/api/debug/opportunity/{id}
```

## iOS App
1. Generate project (first time)
```bash
cd frontend
xcodegen generate
open PolymarketEdge.xcodeproj
```
2. Run in Simulator (iOS 17)
- Ensure backend is running at `http://localhost:8000`
- Build and run

## Tests
```bash
cd backend
source .venv/bin/activate
pytest --cov=app --cov-report=term-missing -q
```
