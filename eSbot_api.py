from fastapi import FastAPI, HTTPException
from eSbot import run_eSbot, get_collection_count, groq_client
from schema import ESbotRequest, LLMAnalysisPayload
from fastapi.middleware.cors import CORSMiddleware
from context import format_llm_prompt

api = FastAPI(    
    title="eSBot: eSkolar LLM Engine",
    description="RAG and Generative Reasoning backend for eSkolar.",
    version="1.0.0"
)

api.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # This is for Frontend, change if you have deployed URL or to your localhost
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@api.post("/query")
def eSbot_query(request: ESbotRequest):
    """ Execute semantic query matching against scholarship specification documents using RAG. """
    answer = run_eSbot(request.query)
    return {
        "response": answer
    }

@api.get("/ping")
def eSbot_ping():
    return {
        "status": "healthy",
        "message": "eSbot active."
    }

@api.get("/check")
def check():
    """ Pull global vector record count loaded in memory spaces. """
    return {
        "document_count": get_collection_count()
    }

@api.post("/explain")
def explain(payload: LLMAnalysisPayload):
    """
        Accept raw JSON student data structures and scholarship rules, 
        compile an isolation prompt template, and return an explicit alignment breakdown.
    """
    try:
        student = payload.student 
        scholarship = payload.scholarship
        breakdown = payload.breakdown 

        instructions = format_llm_prompt(student, scholarship, breakdown)
        chat_completion = groq_client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": instructions
            }],
            model="llama-3.3-70b-versatile",
        )

        analysis = chat_completion.choices[0].message.content 
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"eSBot Explanation Engine error: {str(e)}")