import os
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

responseJson = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Give 30 famous instagram accounts related to nature photography"},
        #{"role": "user", "content": "Who won the world series in 2020?"},
        #{"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    ]
)

print(responseJson["choices"][0]["message"]["content"])


def writeResponse_to_json(responseJson):
    with open("responseJson.json", "w") as f:
        f.write(str(responseJson))


writeResponse_to_json(responseJson)
