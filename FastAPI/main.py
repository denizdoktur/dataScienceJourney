from fastapi import FastAPI
from app.routes import router as api_router

app = FastAPI(title="Image to Text")

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


# uvicorn main:app --reload
