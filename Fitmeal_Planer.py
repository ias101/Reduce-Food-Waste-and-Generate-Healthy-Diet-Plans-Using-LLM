import pandas as pd
from itertools import combinations
import numpy as np
from Calculate_Nutrition import cal_nu
# load csv
df = pd.read_csv("ah_recipes_pr.csv",encoding='iso-8859-1')
df = df[["Name", "URL","Persons", "eiwit", "koolhydraten", "vet"]].dropna()

# transfer the data type
df[["eiwit", "koolhydraten", "vet"]] = df[["eiwit", "koolhydraten", "vet"]].astype(float)
df["Persons"] = df["Persons"].astype(float)
df["eiwit_pp"] = df["eiwit"] / df["Persons"]
df["koolhydraten_pp"] = df["koolhydraten"] / df["Persons"]
df["vet_pp"] = df["vet"] / df["Persons"]

# pruning the oversized data
def filter_candidates(df, targets, tolerance=0.1):
    max_vals = [t * (1 + tolerance) for t in targets]
    condition = (
            (df["eiwit_pp"] <= max_vals[0]) &
            (df["koolhydraten_pp"] <= max_vals[1]) &
            (df["vet_pp"] <= max_vals[2])
    )
    return df[condition]

def is_within_tolerance(values, targets, tolerance=0.1):
    return all([
        abs(v - t) <= t * tolerance
        for v, t in zip(values, targets)
    ])

# linear search
def find_matching_combinations(df, targets,tolerance=0.1, max_comb_size=3,):
    df = filter_candidates(df, targets, tolerance)
    matches = []

    for combo in combinations(df.itertuples(), max_comb_size):
        total = [
            sum(getattr(x, "eiwit_pp") for x in combo),
            sum(getattr(x, "koolhydraten_pp") for x in combo),
            sum(getattr(x, "vet_pp") for x in combo),
        ]
        if is_within_tolerance(total, targets, tolerance) :
            matches.append(combo)
        if matches:
            break
    return matches

# print out
def print_combinations(matches):
    word = []
    combo = matches[0]
    word.append("combination:")
    for item in combo:
        word.append(f" - {item.Name} ({item.URL}) | per person: eiwit: {item.eiwit_pp:.2f}, koolhydraten: {item.koolhydraten_pp:.2f}, vet: {item.vet_pp:.2f} (for {item.Persons} persons)")
    total = [
        sum(getattr(x, "eiwit_pp") for x in combo),
        sum(getattr(x, "koolhydraten_pp") for x in combo),
        sum(getattr(x, "vet_pp") for x in combo),
    ]
    word.append(f"in total（per person）: eiwit={total[0]:.2f}, koolhydraten={total[1]:.2f}, vet={total[2]:.2f}")
    word.append("-----")
    return "\n\n".join(word)

def Fitmeal_plan(plan: str,meal_num: int,weight):
    nu = cal_nu(plan,weight)
    target_protein = nu["Proteins (g)"]
    target_carbs = nu["Carbohydrates (g)"]
    target_fat =nu["Saturated Fat (g)"]

    matches = find_matching_combinations(df, [target_protein, target_carbs, target_fat],max_comb_size=meal_num)
    word = print_combinations(matches)
    if not matches:
        return "no recipe find"
    else:
        return word
