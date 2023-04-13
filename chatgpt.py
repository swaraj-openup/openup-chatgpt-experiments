import openai
# import argparse
# parser = argparse.ArgumentParser("simple_example")
# parser.add_argument("prompt", help="An integer will be increased by 1 and printed.", type=str)
# args = parser.parse_args()
# print (args)


openai.api_key = ""

context = []
context.append({
    "role": "system", "content": "It was raining yesterday, but today it's sunny."})

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=context,
    max_tokens=100,
)

print(response)

def use_chatgpt():