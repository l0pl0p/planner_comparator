import os
from utils.azure_openai import client
from dotenv import load_dotenv

load_dotenv()

def judge_outputs(prompt_plan: str, prolog_plan: str) -> str:
    system_prompt = os.getenv("JUDGE_PROMPT_SYSTEM")
    user_prompt_template = os.getenv("JUDGE_PROMPT_USER_TEMPLATE")

    if not system_prompt or not user_prompt_template:
        raise ValueError("Prompts not found in environment variables.")

    user_prompt = user_prompt_template.format(
        prompt_plan=prompt_plan,
        prolog_plan=prolog_plan
    )

    response = client.chat.completions.create(
        model=os.getenv("AZURE_MODEL_JUDGE"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return response.choices[0].message.content.strip()
