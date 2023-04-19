"""Write the response to json file"""

# pylint: disable=C0103


def write_response_to_json(response_json):
    """
    Writes a JSON response to a file named 'response_json.json' and extracts
    the content of the first message in the 'choices' array of the response
    and appends it to a file named 'output.txt'.

    Args:
        response_json (dict): A JSON response containing a 'choices' array
        with at least one message.

    Returns:
        None
    """

    with open("response_json.json", "a", encoding="utf-8") as f:
        f.write(str(response_json))
    with open("output.txt", "a", encoding="utf-8") as f:
        f.write(response_json["choices"][0]["message"]["content"])
