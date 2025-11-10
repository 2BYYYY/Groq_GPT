from fastapi import FastAPI
from pydantic import BaseModel
from eSbot import run_eSbot  

api = FastAPI()

# structure of the JSON else error
class eSbot_request(BaseModel):
    query: str

@api.post("/query")
def eSbot_query(query: eSbot_request):
    rag_query = query.query
    answer = run_eSbot(rag_query)
    return {"response": answer} 

@api.get("/ping")
def eSbot_ping():
    return {"status" : "eSbot Connected"}
