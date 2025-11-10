import chromadb

volume_path = "/usls_scholarships"
client = chromadb.PersistentClient(path=volume_path)
collection = client.get_or_create_collection(name="USLS_SCHOLARSHIPS")
print("Number of entries:", collection.count())