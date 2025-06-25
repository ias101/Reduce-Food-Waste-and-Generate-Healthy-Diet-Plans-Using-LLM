import streamlit as st
from Eco_Meal_Maker import search_recipe
from Fitmeal_Planer import Fitmeal_plan


def Eco_Meal_Maker(input_text,count ):
    top_results = search_recipe(input_text,top_k=count)
    formatted = []
    for i, r in enumerate(top_results):
        formatted.append(f"{i+1}. {r['Name']}\n    {r['URL']}")
    return "\n\n".join(formatted)



def Fitmeal_Planner(input_text,count,weight ) -> str:
    res = Fitmeal_plan(input_text,count,weight)
    return res

# Streamlit
st.set_page_config(page_title="MealMind", layout="centered")
st.title("MealMind")

# choose function
option = st.selectbox(
    "Select A Function:",
    ("Eco meal maker", "Fit meal planner")
)

# input
input_text = st.text_area("Input:", height=150)

# count
count = st.number_input(
    "Number of Meals:",
    min_value=0,
    step=1,
    value=1
)

weight = st.number_input(
    "Your weight:",
    min_value=10,
    step=1,
    value=10
)

# button
if st.button("go"):
    if not input_text:
        st.warning("empty input！")
    else:
        if option == "Eco meal maker":
            result = Eco_Meal_Maker(input_text,count)
        else:
            result = Fitmeal_Planner(input_text,count,weight)
        st.text_area("Output:", value=result, height=650)
