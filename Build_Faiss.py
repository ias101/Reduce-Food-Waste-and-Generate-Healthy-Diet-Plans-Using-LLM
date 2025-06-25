import pandas as pd
import ast
import openai
import numpy as np
import faiss
import time
import json
from tqdm import tqdm

# api key
openai.api_key = "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"

# path
CSV_PATH = "recipes_mapped.csv"
EMBEDDING_MODEL = "text-embedding-3-small"
FAISS_INDEX_PATH = "recipe_index.faiss"
METADATA_PATH = "recipe_metadata.json"

#load CSV
df = pd.read_csv(CSV_PATH,encoding='iso-8859-1')


def clean_keywords(row):
    try:
        kw_list = ast.literal_eval(row)
        return " ".join(kw_list)
    except:
        return ""

df["keyword_text"] = df["Keywords"].apply(clean_keywords)

# apply embedding model
def get_embeddings(text_list, model=EMBEDDING_MODEL, batch_size=100):
    embeddings = []
    for i in tqdm(range(0, len(text_list), batch_size)):
        batch = text_list[i:i+batch_size]
        try:
            response = openai.Embedding.create(input=batch, model=model)
            batch_embeddings = [e['embedding'] for e in response['data']]
            embeddings.extend(batch_embeddings)
        except Exception as e:
            print(f"Batch {i}-{i+batch_size} failed:", e)
            time.sleep(5)
            # retry once
            try:
                response = openai.Embedding.create(input=batch, model=model)
                batch_embeddings = [e['embedding'] for e in response['data']]
                embeddings.extend(batch_embeddings)
            except:
                print("Failed again. Skipping batch.")
                embeddings.extend([None] * len(batch))  # placeholder
    return embeddings

df = df[df["keyword_text"].notnull() & (df["keyword_text"] != "")]
texts = df["keyword_text"].tolist()
print(f"Total valid entries: {len(texts)}")

embeddings = get_embeddings(texts)

df = df.reset_index(drop=True)
valid_rows = [i for i, emb in enumerate(embeddings) if emb is not None]
embeddings = [embeddings[i] for i in valid_rows]
df = df.iloc[valid_rows]

# create faiss index
embedding_dim = len(embeddings[0])
embedding_matrix = np.array(embeddings).astype("float32")

index = faiss.IndexFlatL2(embedding_dim)
index.add(embedding_matrix)

# save index
faiss.write_index(index, FAISS_INDEX_PATH)

# save other data
metadata = df[["Name", "URL", "Keywords", "energie", "eiwit", "koolhydraten", "vet"]].to_dict(orient="records")
with open(METADATA_PATH, "w", encoding="iso-8859-1") as f:
    json.dump(metadata, f, ensure_ascii=False, indent=2)

print("finish")
