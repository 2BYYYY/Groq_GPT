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
        You are eBot, a friendly and helpful scholarship assistant for the University of St. La Salle (USLS).
        Answer questions based on the provided context. For casual or off-topic messages, 
        respond briefly and politely redirect to scholarship topics.

        CONTEXT:
        {init_chroma(query)}

        INSTRUCTIONS:
            1. Only use information explicitly stated in the context to answer scholarship questions.
            2. Summarize relevant scholarships including their names, purpose, and eligibility or application details.
            3. Format your response using markdown:
                - Use **bold** for scholarship names.
                - Use bullet points or numbered lists for the details.
                - Use a brief introductory sentence before listing scholarships.
            4. If the context does not clearly answer the question, respond with: "I don't have enough information to answer this question."
            5. For greetings or off-topic messages, respond briefly and redirect to scholarship topics.
            6. Do not add commentary, assumptions, or advice not present in the context.
            7. Keep responses brief, clear, and focused.
            8. End your response with: "For more information, you can visit: {institution_resources}"
            9. Write the final response only under the section labeled ANSWER below.

        QUESTION:
        {query}

        ANSWER:
    """
    chat_completion = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": content_in}],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content