# MealMind - Reduce Food Waste and Generate Healthy Diet Plans Using LLM
[Paper](./Bep.pdf)
## 📖 Overview

**MealMind** is an AI-powered application designed to tackle two critical global challenges: **food waste reduction** and **personalized meal planning**. By leveraging Large Language Models (LLMs) and semantic search techniques, MealMind helps users transform surplus food into delicious, nutritious meals while generating diet plans tailored to their lifestyle and health goals.

The system consists of two main modules:
- **Eco Meal Maker**: Recommends recipes based on surplus ingredients and user preferences.
- **Fit Meal Planner**: Generates personalized daily meal plans based on weight and activity levels.

---

## ✨ Features

- **Surplus Ingredient Matching**: Matches discarded food items from retailers with recipes using semantic similarity.
- **Natural Language Recipe Search**: Accepts flexible queries (e.g., "spicy comfort food") and returns relevant recipes.
- **Personalized Nutrition Planning**: Calculates daily nutritional needs based on weight and activity schedule.
- **FAISS-based Semantic Search**: Enables fast and accurate recipe retrieval.
- **LLM-Powered Activity Parsing**: Uses DeepSeek-R1 to interpret free-text daily schedules.
- **Nutrition-Aware Meal Combination**: Finds optimal recipe combinations meeting calculated macros.

---

## 🗂️ Project Structure

```
├── AH_script.py               # Script for processing supermarket data
├── Build_Faiss.py             # Builds FAISS index for recipe vectors
├── Calculate_Nutrition.py     # Calculates nutritional requirements
├── Data_preprocessing.py      # Cleans and prepares datasets
├── Eco_Meal_Maker.py          # Eco Meal Maker module
├── Fitmeal_Planer.py          # Fit Meal Planner module
├── For_plot.py                # Visualization utilities
├── LLM_API.py                 # Handles LLM API calls (e.g., DeepSeek-R1)
├── Mealmind.py                # Main application entry point
├── matching.py                # Matches surplus products with recipe ingredients
├── rp.txt                     # Recipe data or related text
├── api key                    # API key file (keep secure)
└── Bep.pdf                    # Thesis document detailing the project
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API key (for text-embedding-3-small)
- DeepSeek API access (for DeepSeek-R1)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/ias101/Reduce-Food-Waste-and-Generate-Healthy-Diet-Plans-Using-LLM.git
cd Reduce-Food-Waste-and-Generate-Healthy-Diet-Plans-Using-LLM
```

2. Install required dependencies:
```bash
pip install faiss-cpu openai pandas numpy requests
```

3. Set up API keys in `api key` or as environment variables.

### Usage

1. **Preprocess Data**:
   Run `Data_preprocessing.py` to clean and prepare recipe and surplus food datasets.

2. **Build FAISS Index**:
   Execute `Build_Faiss.py` to create the semantic search index.

3. **Run the Application**:
   Launch the main app:
   ```bash
   python Mealmind.py
   ```

4. **Use Modules**:
   - **Eco Meal Maker**: Input a food preference (e.g., “vegetarian pasta”) to get recipe suggestions.
   - **Fit Meal Planner**: Enter weight and daily activity to receive a personalized meal plan.

---

## 🧠 How It Works

### 1. Data Integration
- Surplus food data from a Dutch supermarket chain is matched with recipes scraped from Allerhande.
- Ingredients are vectorized using `text-embedding-3-small` and matched via cosine similarity.

### 2. Eco Meal Maker
- User inputs a free-text query (e.g., “light and refreshing”).
- Query is embedded and compared with recipe vectors in a FAISS index.
- Top-k recipes are returned based on semantic similarity.

### 3. Fit Meal Planner
- User provides weight and free-text daily schedule.
- DeepSeek-R1 parses activities and maps them to intensity levels.
- Nutritional requirements are calculated per activity.
- The system searches for recipe combinations meeting macro needs within a 10% error margin.

---

## ⚠️ Limitations & Future Work

### Current Limitations
- No support for allergies or dietary restrictions.
- Single-user focus; no family/group planning.
- Brute-force search in Fit Meal Planner can be slow for >3 meals.

### Planned Improvements
- Add user profiles for allergens and preferences.
- Extend to multi-user meal planning.
- Optimize search with dynamic programming or genetic algorithms.
- Implement feedback loops for recommendation tuning.

---

## 📄 License

This project is part of an academic thesis. Use for research and educational purposes is encouraged. Please cite the work if used in publications.

---

## 📚 References

Key references are listed in `Bep.pdf`. Major sources include:
- Schanes et al. (2018) on household food waste.
- Aschemann-Witzel et al. (2015) on consumer-related food waste.
- Amawi et al. (2024) on athletes' nutritional demands.

---

## 👤 Author

**Shen Jikun**  
Jheronimus Academy of Data Science  
Thesis submitted on 26-04-2025

GitHub: [@ias101](https://github.com/ias101)  
Project Link: [https://github.com/ias101/Reduce-Food-Waste-and-Generate-Healthy-Diet-Plans-Using-LLM](https://github.com/ias101/Reduce-Food-Waste-and-Generate-Healthy-Diet-Plans-Using-LLM)
