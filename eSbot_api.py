from fastapi import FastAPI
from pydantic import BaseModel
from eSbot import run_eSbot  

api = FastAPI()

# structure of the JSON else error
class eSbot_request(BaseModel):
    question: str

@api.post("/eSbot")
def eSbot_query(query: eSbot_request):
    rag_query = query.question
    answer = run_eSbot(rag_query)
    return {"response": answer} 
