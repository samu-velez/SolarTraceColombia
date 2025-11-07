# SolarTraceColombia

Aplicativo web para analizar la transición energética renovable (1965–2022).  
Backend construido en **FastAPI** — Frontend en **Bootstrap + Chart.js**.

---

## 🚀 Backend (FastAPI)

### Correr local

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate   # En Windows: .venv\Scripts\activate
python3 -m pip install -r ../requirements.txt
cd ..
python3 -m uvicorn backend.main:app --reload --port 8000
```
