import os
from fastapi import FastAPI
from pydantic import BaseModel
import chromadb
# from dotenv import load_dotenv
from groq import Groq

# local use (load_dotenv()) 
GROQ_API = os.environ.get("GROQ_API")


api = FastAPI()

# railway volume path (local: ./chroma_db)
chroma_client = chromadb.PersistentClient(path="/usls_scholarships")
collection = chroma_client.get_or_create_collection(name="USLS_SCHOLARSHIPS")
print(f"ChromaDB initialized with {collection.count()} entries.")

groq_client = Groq(api_key=GROQ_API)

class QueryRequest(BaseModel):
    query: str


@api.post("/query")
def query_chromadb(req: QueryRequest):
    user_query = req.query

    # Query ChromaDB
    try:
        chroma_results = collection.query(query_texts=[user_query], n_results=5)
        context_text = chroma_results["documents"][0]
    except Exception as e:
        print(f"error: {e}")

    # Compose prompt for Groq
    institution_resources = "https://www.usls.edu.ph/overviews/Scholarships"
    prompt = f"""
                You are an AI assistant for eSkolar that must answer questions based on the provided context.

                CONTEXT:
                {context_text}

                INSTRUCTIONS:
                    1. Only use information explicitly stated in the context to answer the question.
                    2. Summarize the relevant scholarships mentioned in the context, including their names, purpose, and any eligibility or application details provided.
                    3. If the context does not clearly answer the question, respond exactly with: "I don't have enough information to answer this question."
                    4. Do not add commentary, assumptions, or advice not present in the context.
                    5. Keep the response brief, clear, and focused on what is in the context.
                    6. End your response with: "For more information, you can visit: {institution_resources}"
                    7. Write the final response only under the section labeled ANSWER below.

                QUESTION:
                {user_query}

                ANSWER:
            """
    
    try:
        chat_completion = groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"{prompt}",
                    }
                ],
                model="llama-3.3-70b-versatile",
            )
        answer = chat_completion.choices[0].message.content
    except Exception as e:
        print(f"error: {e}")

    return {"answer": answer}

@api.get("/ping")
def ping():
    return {"status": "eSbot connected"}