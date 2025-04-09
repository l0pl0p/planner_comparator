from utils.azure_openai import client
import os

def judge_outputs(prompt_plan: str, prolog_plan: str) -> str:
    prompt = os.getenv("JUDGE_PROMPT")
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"""Compare the following legal research plans and determine which is superior and why.

Plan A:
{prompt_plan}

Plan B:
{prolog_plan}
"""}
        ]
    )
    return response.choices[0].message.content.strip()
