from fastapi import FastAPI
from pydantic import BaseModel
from eSbot import run_eSbot, get_collection_count

api = FastAPI()

class eSbot_request(BaseModel):
    query: str

@api.post("/query")
def eSbot_query(request: eSbot_request):
    answer = run_eSbot(request.query)
    return {"response": answer}

@api.get("/ping")
def eSbot_ping():
    return {"status": "200 : eSbot Connected"}

@api.get("/check")
def check():
    return {"document_count": get_collection_count()}