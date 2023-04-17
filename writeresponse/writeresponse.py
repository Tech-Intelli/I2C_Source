def write_response_to_json(responseJson):
    with open("responseJson.json", "a") as f:
        f.write(str(responseJson))
    with open("output.txt", "a") as f:
        f.write(responseJson["choices"][0]["message"]["content"])
