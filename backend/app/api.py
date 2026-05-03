from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import os
import time
from pathlib import Path

# Only import these for local use
if os.environ.get("RENDER") is None:
    import webbrowser
    import threading

from .model_utils import preprocess, model

# -------------------------------------------------
# 1️⃣ Initialize FastAPI
# -------------------------------------------------
app = FastAPI(title="Mental-Health Predictor API")

# -------------------------------------------------
# 2️⃣ CORS (dynamic for local + production)
# -------------------------------------------------
if os.environ.get("RENDER"):
    origins = ["*"]  # allow all in production (can restrict later)
else:
    origins = [
        "http://localhost",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# 3️⃣ Prevent cache
# -------------------------------------------------
class NoCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response: Response = await call_next(request)
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

app.add_middleware(NoCacheMiddleware)

BUILD_VERSION = str(int(time.time()))

# -------------------------------------------------
# 4️⃣ Serve frontend ONLY in local (not needed on Render)
# -------------------------------------------------
frontend_dist = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"

if frontend_dist.exists() and os.environ.get("RENDER") is None:
    print(f"✅ Frontend build found at: {frontend_dist}")

    app.mount("/assets", StaticFiles(directory=frontend_dist / "assets"), name="assets")
    app.mount("/images", StaticFiles(directory=frontend_dist / "images"), name="images")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        response = FileResponse(frontend_dist / "index.html")
        response.headers["X-Build-Version"] = BUILD_VERSION
        return response
else:
    print("⚠️ Running in API-only mode (Render or no frontend build found)")

# -------------------------------------------------
# 5️⃣ Root endpoint (needed for Render health check)
# -------------------------------------------------
@app.get("/")
def home():
    return {"status": "MentalGlow API running"}

# -------------------------------------------------
# 6️⃣ Prediction API
# -------------------------------------------------
class InputData(BaseModel):
    age: int
    gender: str
    city: str 
    relationship_status: str

    sleep_hours: float
    exercise_frequency: int
    screen_time_hours: float
    diet_quality: int

    stress_level: int
    anxiety_level: int
    mood: str
    motivation_level: int
    concentration_level: int

    social_support: int
    social_interaction_frequency: int
    work_stress: int
    is_student: int
    is_employed: int

    household_responsibility: int

    open_to_therapy: int
    aware_of_mental_health: int

@app.post("/api/predict/")
def predict(data: InputData):
    try:
        df = preprocess(data.dict())
        pred = model.predict(df)[0]
        risk = "High risk" if pred == 1 else "Low risk"
        return {"prediction": risk}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------------------------------
# 7️⃣ Test route
# -------------------------------------------------
@app.get("/test")
def test_endpoint():
    return {"message": "Test endpoint is working!"}

# -------------------------------------------------
# 8️⃣ Auto-open browser (ONLY LOCAL)
# -------------------------------------------------
if os.environ.get("RENDER") is None:
    def launch_browser():
        webbrowser.open("http://127.0.0.1:8000/")
    threading.Timer(1.5, launch_browser).start()