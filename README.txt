ProjectCine - pacote gerado automaticamente for deployment on Render or local run.

Structure:
- backend/: Flask app (app.py), SQLite DB (cinema.db), requirements.txt, Procfile
- frontend/: React app source (run `npm install` then `npm run build` to create build/)

Quick local run (backend):
1. cd backend
2. python -m venv venv
3. venv\Scripts\activate
4. pip install -r requirements.txt
5. python app.py
Open http://127.0.0.1:10000

Quick local run (frontend development):
1. cd frontend
2. npm install
3. npm start
Open http://localhost:3000 and set REACT_APP_API_URL to http://localhost:10000

Deploy on Render (single service unified):
- Push repo to GitHub
- Create a Web Service on Render with root directory at repository root
- Build command: cd backend && pip install -r requirements.txt && cd ../frontend && npm install && npm run build
- Start command: cd backend && gunicorn -w 4 -b 0.0.0.0:10000 app:app
- Set environment variable OPENAI_API_KEY on Render dashboard if you want IA

Notes:
- Place your OpenAI API key in backend/.env or in Render environment variables as OPENAI_API_KEY
- SQLite is file-based; for production prefer a managed DB (Postgres) for persistence.
