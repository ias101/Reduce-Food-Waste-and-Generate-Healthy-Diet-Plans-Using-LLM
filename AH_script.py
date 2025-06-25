import requests
from bs4 import BeautifulSoup
import re
import  csv
from tqdm import tqdm
def clean_ingredient(text):
    # 匹配结构：数量 + 单位 + 数量 + 单位 + 食材 + 食材
    pattern = r"(\d+)\s*([a-zA-Z]+)\s*\1\s+\2\s+([a-zA-Z ]+)\3"
    match = re.search(pattern, text)
    if match:
        quantity = match.group(1)
        unit = match.group(2)
        ingredient = match.group(3).strip()
        return f"{quantity} {unit} {ingredient}"
    else:
        # 尝试一个更宽松的版本（防止单位部分未完全重复）
        fallback_pattern = r"(\d+)\s*([a-zA-Z]+)\s+([a-zA-Z ]+)\3"
        match = re.search(fallback_pattern, text)
        if match:
            return f"{match.group(1)} {match.group(2)} {match.group(3).strip()}"
        return text  # 如果都不匹配，原样返回

def parse_nutrition_entry(entry):
    match = re.match(r"([a-zA-Z\s]+)([\d.,]+[a-zA-Z]+)", entry)
    if match:
        key = match.group(1).strip()
        value = match.group(2)
        return key, value
    else:
        return entry, None  # fallback in case pattern doesn't match

def scrape_recipe(url):
    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:

        title = soup.find('h1').get_text(strip=True)
        ingredients = [li.get_text(strip=True) for li in soup.select('table.recipe-ingredients-ingredient-list_table__18qtY tr')]
        nutrition = [p.get_text(strip=True)for p in soup.select('div.recipe-footer-nutrition_section__9WXac p')]
        num_of_person = [span.get_text(strip=True) for span in soup.select('div.servings-input_iconsContainer__NUnAL p')]
        tags = [li.get_text(strip=True)for li in soup.select('ul.recipe-header-tags_tags__Qscil li')]
        cleaned_ingredients = [clean_ingredient(item) for item in ingredients]
        nutrition_dict = dict(parse_nutrition_entry(item) for item in nutrition)

        return {
            "Name": title,
            "Persons": num_of_person[0],
            "Nutrients": nutrition_dict,
            'Ingredients': cleaned_ingredients,
            "URL": url,
            "Keywords": tags
        }
    except Exception as e:
        return {"Name": "N/A", "Persons": "N/A", "Nutrients": "N/A",'Ingredients': 'N/A', "URL": 'N/A', "Keywords": 'N/A'}

file_path = 'rp.txt'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

links = content.split()

with open("ah_recipes.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["Name", "Persons", "Nutrients",'Ingredients', "URL",'Keywords'])
    writer.writeheader()
    for url in  tqdm(links, desc="Processing"):
        data = scrape_recipe(url)
        writer.writerow(data)




