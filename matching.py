import ast
import pandas as pd
import numpy as np
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
from tqdm.auto import tqdm


api_key = "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"
client = OpenAI(api_key=api_key)

# Batch embedding with progress bar
def batch_embed(texts, model, batch_size=512):
    """Embed a list of texts in batches to reduce API calls."""
    embeddings = []
    for i in tqdm(range(0, len(texts), batch_size), desc="Embedding batches"):
        batch = texts[i:i+batch_size]
        resp = client.embeddings.create(model=model, input=batch)
        embeddings.extend([d.embedding for d in resp.data])
    return np.array(embeddings)


EMBEDDING_MODEL = "text-embedding-3-small"
SIMILARITY_THRESHOLD = 0.6


t1 = pd.read_csv("ah_recipes_pr.csv", encoding="iso-8859-1")
t2 = pd.read_csv("product_data.csv", encoding="iso-8859-1", names=['product_name'])


def drop_un(text):
    import re
    pattern = r' [a-zA-Z]+'
    return ''.join(re.findall(pattern, text))
t2['product_name'] = t2['product_name'].apply(drop_un).shift(-1)
t2.drop_duplicates(inplace=True)
t2.dropna(inplace=True)
product_names = (
    t2["product_name"]
    .dropna()
    .astype(str)
    .str.strip()
    .unique()
    .tolist()
)
product_names = [str(name) if name else " " for name in product_names]
print(f"Embedding {len(product_names)} unique product names...")
product_embeddings = batch_embed(product_names, EMBEDDING_MODEL)


def extract_name(item_str):
    import re
    parts = str(item_str).split()
    pattern = r'[a-zA-Z]+'
    a = " ".join(parts[2:]) if len(parts) > 2 else parts[-1]
    return ' '.join(re.findall(pattern, a))


ingredient_names = set()
for lst in tqdm(t1['Ingredients'].dropna(), desc="Collecting ingredient names"):
    try:
        items = ast.literal_eval(lst)
        for it in items:
            ingredient_names.add(extract_name(it))
    except Exception:
        continue
ingredient_names = list(ingredient_names)
ingredient_names = [str(name) if name else " " for name in ingredient_names]
print(f"Embedding {len(ingredient_names)} unique ingredients...")
ingredient_embeddings = batch_embed(ingredient_names, EMBEDDING_MODEL)


emb_index = {name: vec for name, vec in zip(ingredient_names, ingredient_embeddings)}


matched_indices = []
for idx, row in tqdm(t1.iterrows(), total=len(t1), desc="Mapping recipes"):
    try:
        items = ast.literal_eval(row['Ingredients'])
    except Exception:
        continue
    mapped = []
    ok = True
    for it in items:
        name = extract_name(it)
        vec = emb_index.get(name)
        if vec is None:
            ok = False
            break
        sims = cosine_similarity(vec.reshape(1, -1), product_embeddings)[0]
        best_idx = np.argmax(sims)
        if sims[best_idx] >= SIMILARITY_THRESHOLD:
            mapped.append(product_names[best_idx])
            if len(mapped) >= 0.8*len(items):
                break
        else:
            if len(mapped) >= 0.8*len(items):
                break
            ok = False
            break
    if ok:
        matched_indices.append(idx)


result = t1.loc[matched_indices].reset_index(drop=True)
result.to_csv("recipes_mapped.csv", index=False)

total = len(t1)
matched = len(matched_indices)
print(f"Matched {matched}/{total} ({matched/total:.2%}) recipes.")
