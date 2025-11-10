import os
import chromadb
# from dotenv import load_dotenv
from groq import Groq

def init_chroma(query: str) -> list:
    # railway volume path (local: ./chroma_db)
    chroma_client = chromadb.PersistentClient(path="/usls_scholarships")
    collection = chroma_client.get_or_create_collection(name="USLS_SCHOLARSHIPS")
    results = collection.query(
                    query_texts=[query], 
                    n_results=5
                    )
    return results["documents"]

def run_eSbot(query: str) -> str:
    # local use (load_dotenv()) 
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
    client = Groq(
        # railway env
        api_key=os.environ.get("GROQ_API"),
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{content_in}",
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    run_eSbot()