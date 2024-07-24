"""Package-wide LLM API utilities."""

from openai import OpenAI


def helpful_assistant(user_message, api_key):
    """Call OpenAI chat completions API with user message and return response.
    With initial system message: 'You are a helpful assistant.'"""
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message},
        ])

    return completion.choices[0].message.content
