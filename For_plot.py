
import pandas as pd
df = pd.read_csv("ah_recipes_pr.csv", encoding="iso-8859-1")
df_sampled = df.sample(frac=0.79, random_state=42)
df_sampled.to_csv("recipes_mapped.csv", index=False)