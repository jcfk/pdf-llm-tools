"""Package-wide LLM API utilities"""

import json
from openai import OpenAI
from .opts import opts

OPENAI_MODEL = "gpt-4o-mini"


def helpful_assistant_json(user_message):
    """Call OpenAI chat completions API with user message.

    Insist on json output and use initial system message 'You are a helpful
    assistant.'

    Return value deserialized with json.loads.
    """
    client = OpenAI(api_key=opts["openai_api_key"])
    completion = client.chat.completions.create(
        model=OPENAI_MODEL,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message},
        ])

    return json.loads(completion.choices[0].message.content)
