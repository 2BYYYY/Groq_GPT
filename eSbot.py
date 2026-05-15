import os
import chromadb
from groq import Groq

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# module-level singletons — initialized once on startup
chroma_client = chromadb.PersistentClient(path=os.path.join(BASE_DIR, "chroma_db"))
collection = chroma_client.get_or_create_collection(name="USLS_SCHOLARSHIPS")
groq_client = Groq(api_key=os.environ.get("GROQ_API"))

def init_chroma(query: str) -> list:
    results = collection.query(query_texts=[query], n_results=3)
    return results["documents"]

def get_collection_count() -> int:
    return collection.count()

def run_eSbot(query: str) -> str:
    institution_resources = "https://www.usls.edu.ph/overviews/Scholarships"
    content_in = f"""
        You are an AI assistant for eSkolar that must answer questions based on the provided context.

        CONTEXT:
        {init_chroma(query)}

        INSTRUCTIONS:
            1. Only use information explicitly stated in the context to answer the question.
            2. Summarize the relevant scholarships mentioned in the context, including their names, purpose, and any eligibility or application details provided.
            3. If the context does not clearly answer the question, respond exactly with: "I don't have enough information to answer this question."
            4. Do not add commentary, assumptions, or advice not present in the context.
            5. Keep the response brief, clear, and focused on what is in the context.
            6. End your response with: "For more information, you can visit: {institution_resources}"
            7. Write the final response only under the section labeled ANSWER below.

        QUESTION:
        {query}

        ANSWER:
    """
    chat_completion = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": content_in}],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content