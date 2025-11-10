
from eSbot import run_eSbot  

def eSbot_query():
    rag_query = "what are the scholarships in usls?"
    answer = run_eSbot(rag_query)
    print("response: ", answer) 

if __name__ == "__main__":
    eSbot_query()
