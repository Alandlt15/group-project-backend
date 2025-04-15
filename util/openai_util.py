import openai


def completion_with_chatgpt(text: str, model: str = "gpt-3.5-turbo") -> str:
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "user", "content": text},
        ],
    )
    return response["choices"][0]["message"]["content"]
