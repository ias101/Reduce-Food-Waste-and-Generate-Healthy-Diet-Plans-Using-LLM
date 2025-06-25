from LLM_API import *
import json
def calculate_nutritional_needs(weight, low_intensity_time, moderate_intensity_time, high_intensity_time):
    # Define nutrition requirement per kg per min
    protein_low = 0.0033
    protein_moderate = 0.005
    protein_high = 0.0067

    carb_low = 0.0018
    carb_moderate = 0.0012
    carb_high = 0.0015

    fat_low = 0.0066
    fat_moderate = 0.011
    fat_high = 0.0076

    # Calculate nutrition
    protein_total = (protein_low * low_intensity_time ) + \
                    (protein_moderate * moderate_intensity_time ) + \
                    (protein_high * high_intensity_time )
    carb_total = (carb_low * low_intensity_time ) + \
                 (carb_moderate * moderate_intensity_time)  + \
                 (carb_high * high_intensity_time )
    saturated_fat = ((fat_low * low_intensity_time ) +
                     (fat_moderate * moderate_intensity_time ) +
                     (fat_high * high_intensity_time ))*0.1


    return {
        "Proteins (g)": protein_total * weight,
        "Carbohydrates (g)": carb_total * weight,
        "Saturated Fat (g)": saturated_fat * weight
    }

def cal_nu(prompt_word,weight):
    prompt = 'Training Plan:\n' + prompt_word
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": f"{Basic_prompt+prompt}"},
        ],
        response_format={
            'type': 'json_object'
        },
        stream=False
    )
    content = response.choices[0].message.content
    content = json.loads(content)

    low_intensity_time = content["Low-intensity exercise"]
    moderate_intensity_time = content["Moderate-intensity exercise"]
    high_intensity_time = content["High-intensity exercise"]

    # calculate nutritional needs
    weight = weight
    nutritional_needs = calculate_nutritional_needs(weight, int(low_intensity_time), int(moderate_intensity_time), int(high_intensity_time))
    return nutritional_needs


