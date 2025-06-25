import pandas as pd
import re

def extract_nutrition_info(nutrition_str):
    nutrition_dict = {
        "energie": None,
        "eiwit": None,
        "koolhydraten": None,
        "vet": None,
        "waarvan verzadigd": None
    }

    if isinstance(nutrition_str, str):
        matches = re.findall(r'.(energie|eiwit|koolhydraten|vet|waarvan verzadigd).:\s*.(\d+)(kcal|g)', nutrition_str)
        for nutrient, value, unit in matches:
            nutrition_dict[nutrient] = f"{value}"

    return nutrition_dict

def process_csv(input_file, output_file):
    missing_values = ["n/a", "na", "{}"]

    df = pd.read_csv(input_file, na_values = missing_values,encoding = "utf-8")

    df.dropna(inplace=True)

    # apply function to Nutrients column
    nutrition_data = df['Nutrients'].apply(extract_nutrition_info).apply(pd.Series)
    df['Ingredients'] = df['Ingredients'].apply(i_smooth)
    df['Name'] = df['Name'].apply(n_smooth)

    # concat the new colums
    df = pd.concat([df, nutrition_data], axis=1)
    for i in df.columns:
        df[f'{i}'] = df[f'{i}'].fillna(0)
    df['Persons'] = df['Persons'].apply(p_smooth)

    # save the csv file
    df.to_csv(output_file, index=False)
    print(f"save the file to {output_file}")

def p_smooth(Persons):
    if Persons == '0':
        return '1'
    else:
        return Persons

def i_smooth(input_str):

    processed_str = input_str.strip()

    items = re.findall(r"['\"](.*?)['\"]", processed_str)

    def fix_errors(lst):
        fixed = []
        for s in lst:
            s = re.sub(r'\d*[\u00BC-\u00BE\u2150-\u215E]', '', s).strip()
            s = re.sub(r'(\d+)([a-z]+)\d+ \2', r'\1 \2', s)
            s = re.sub(r'(.+?)\1', r'\1', s)
            s = re.sub(r'\s{2,}', ' ', s).strip()
            fixed.append(s)
        return fixed

    # 修复元素内容
    fixed_list = fix_errors(items)
    return fixed_list

def n_smooth(input_str):
    return re.sub(r'/s',' ', input_str)

input_file = "ah_recipes.csv"
output_file = "ah_recipes_pr.csv"
process_csv(input_file, output_file)
