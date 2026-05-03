import uvicorn
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))

    uvicorn.run(
        "app.api:app",
        host="0.0.0.0",
        port=port,
        reload=os.environ.get("RENDER") is None  # reload only locally
    )