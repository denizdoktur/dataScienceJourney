from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from .main import kickoff_with_input

app = FastAPI()

class ArticleInput(BaseModel):
    title: str
    topic: str
    goal: str

@app.post("/generate_article")
async def generate_article(article_input: ArticleInput):
    try:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            None,
            kickoff_with_input,
            article_input.title,
            article_input.topic,
            article_input.goal
        )
        return {"message": "Article generation initiated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
