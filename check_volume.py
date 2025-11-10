import chromadb

volume_path = "/mnt/volume_chroma_db"
client = chromadb.PersistentClient(path=volume_path)
collection = client.get_or_create_collection(name="USLS_SCHOLARSHIPS")
print("Number of entries:", collection.count())