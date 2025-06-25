from openai import OpenAI

client = OpenAI(api_key="sk-c6efe937659540fea00f44923a8c73a2", base_url="https://api.deepseek.com")
Basic_prompt=('Please classify each exercise in the following training plan into one of the three intensity categories based on VO2max percentages,and calculate the total training time (in minutes) for each intensity category:Low-intensity exercise (25% VO2max)Moderate-intensity exercise (65% VO2max)High-intensity exercise (85% VO2max) examaple out put：Low-intensity exercise: [total time] mins Moderate-intensity exercise: [total time] mins High-intensity exercise: [total time] mins and output them in JSON format\n')
