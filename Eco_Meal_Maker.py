import faiss
import numpy as np
import json
from openai import OpenAI

# api
api_key = "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"
client = OpenAI(api_key=api_key)

# load faiss and meatadata
FAISS_INDEX_PATH = "recipe_index.faiss"
METADATA_PATH = "recipe_metadata.json"

index = faiss.read_index(FAISS_INDEX_PATH)

with open(METADATA_PATH, "r", encoding="iso-8859-1") as f:
    metadata = json.load(f)

# search
def search_recipe(query, top_k=1, model="text-embedding-3-small"):
    # get query embedding
    response = client.embeddings.create(
        input=[query],
        model=model
    )
    query_embedding = np.array(response.data[0].embedding).astype("float32").reshape(1, -1)

    # search in FAISS index
    D, I = index.search(query_embedding, top_k)

    results = []
    for idx in I[0]:
        item = metadata[idx]
        results.append({
            "Name": item["Name"],
            "URL": item["URL"]
        })
    return results


if __name__ == "__main__":
    query = 'Recommend me a vegetarian main dish that I can serve to others'
    top_results = search_recipe(query)

    print("\n recipe:")
    for i, r in enumerate(top_results):
        print(f"{i+1}. {r['Name']}\n    {r['URL']}")
