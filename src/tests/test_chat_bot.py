"""
Unit Test for ChatBot
"""

import os
import pytest
# pylint: disable=E0401
from generate_caption import Chatbot

@pytest.mark.skip(reason="This test is currently not required,\
                  this will be fixed and enabled later.")
def test_chat_bot():
    """
    Test the ChatBot response functionality.
    """
    chat_bot = Chatbot(os.environ["OPENAI_API_KEY"])

    # Testcase: 1 Get a small response
    response = chat_bot.get_response("Write a one line sentence on the Sun.")
    response = response["choices"][0]["message"]["content"]
    print(response)
    assert response != ''

    # Testcase: 2 Generate a numeric digit
    response = chat_bot.get_response('''Generate a numeric digit.
                                        No extra characters or text''')
    response = response["choices"][0]["message"]["content"]

    try:
        response = int(response)
    except ValueError:
        assert False, "Invalid response, not a digit!"

    # Testcase: 3 Generate an even number
    response = chat_bot.get_response('''Generate an even number.
                                        No extra characters or text''')
    response = response["choices"][0]["message"]["content"]

    try:
        response = int(response)
    except ValueError:
        assert False, "Invalid response, not a number!"

    assert response % 2 == 0

    # Testcase: 4 First US President
    response = chat_bot.get_response('''First US President''')
    response = response["choices"][0]["message"]["content"]
    assert "George Washington" in response
