"""Package-wide LLM API utilities."""

import json
from openai import OpenAI


def helpful_assistant_json(user_message, api_key):
    """Call OpenAI chat completions API with user message.

    Insist on json output and use initial system message 'You are a helpful
    assistant.'

    Return value deserialized with json.loads.
    """
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message},
        ])

    return json.loads(completion.choices[0].message.content)
