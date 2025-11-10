import shutil
import os
import chromadb

def load_data():
    local_chroma_db = "./chroma_db"
    # 500MB FREE TIER          
    volume_path = "/usls_scholarships"   

    if os.path.exists(local_chroma_db) and not os.listdir(volume_path):
        shutil.copytree(local_chroma_db, volume_path, dirs_exist_ok=True)
        print("ChromaDB folder copied into Railway volume.")

    chroma_client = chromadb.PersistentClient(path=volume_path)
    collection = chroma_client.get_or_create_collection(name="USLS_SCHOLARSHIPS")

    print(f"ChromaDB loaded with {collection.count()} entries.")
    return collection

if __name__ == "__main__":
    load_data()