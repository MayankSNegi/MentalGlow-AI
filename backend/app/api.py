from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import webbrowser, threading, time
from pathlib import Path

from .model_utils import preprocess, model

# -------------------------------------------------
# 1️⃣ Initialize FastAPI
# -------------------------------------------------
app = FastAPI(title="Mental-Health Predictor API")

# -------------------------------------------------
# 2️⃣ CORS for frontend
# -------------------------------------------------
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
# 3️⃣ Prevent cache - Always serve fresh frontend build
# -------------------------------------------------
class NoCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response: Response = await call_next(request)
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

app.add_middleware(NoCacheMiddleware)

# Dynamic version based on startup time
BUILD_VERSION = str(int(time.time()))

# -------------------------------------------------
# 4️⃣ Detect and serve frontend build dynamically
# -------------------------------------------------
frontend_dist = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"

if frontend_dist.exists():
    print(f"✅ Frontend build found at: {frontend_dist}")
    app.mount("/assets", StaticFiles(directory=frontend_dist / "assets"), name="assets")
    app.mount("/images", StaticFiles(directory=frontend_dist / "images"), name="images")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        response = FileResponse(frontend_dist / "index.html")
        response.headers["X-Build-Version"] = BUILD_VERSION
        return response
else:
    print(f"⚠️  Frontend build not found at: {frontend_dist}. Only API will run.")

# -------------------------------------------------
# 5️⃣ Prediction API
# -------------------------------------------------
class InputData(BaseModel):
    # Basic Demographics
    age: int
    gender: str
    city: str 
    relationship_status: str

    # Lifestyle
    sleep_hours: float
    exercise_frequency: int
    screen_time_hours: float
    diet_quality: int

    # Emotional & Mental Health
    stress_level: int
    anxiety_level: int
    mood: str
    motivation_level: int
    concentration_level: int

    # Social & Work/Study
    social_support: int
    social_interaction_frequency: int
    work_stress: int
    is_student: int
    is_employed: int

    # Household
    household_responsibility: int

    # Awareness
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
# 6️⃣ Health check route
# -------------------------------------------------
@app.get("/test")
def test_endpoint():
    return {"message": "Test endpoint is working!"}

# -------------------------------------------------
# 7️⃣ Auto-open browser
# -------------------------------------------------
def launch_browser():
    webbrowser.open("http://127.0.0.1:8000/")
threading.Timer(1.5, launch_browser).start()
