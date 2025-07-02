import pandas as pd
import chromadb
import uuid
import os

class Portfolio:
    def __init__(self, file_path="resource/portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient(path="vectorstore")
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                techstack = str(row["Techstack"])
                link = str(row["Links"])
                if techstack.strip():
                    self.collection.add(
                        documents=[techstack],
                        metadatas=[{"links": link}],
                        ids=[str(uuid.uuid4())]
                    )

    def query_links(self, skills):
        if not skills or not isinstance(skills, list):
            return []
        try:
            results = self.collection.query(query_texts=skills, n_results=2)
            return results.get("metadatas", [])
        except Exception as e:
            print(f"Error during query: {e}")
            return []
