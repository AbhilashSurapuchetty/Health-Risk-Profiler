from fastapi import FastAPI
from app.routes.analyze import router as analyze_router
from dotenv import load_dotenv

app = FastAPI(title="Health Risk Profiler", version="0.1.0")
app.include_router(analyze_router, prefix="/api")

load_dotenv()

@app.get("/")
def root():
    return {"status": "ok", "service": "Health Risk Profiler"}
