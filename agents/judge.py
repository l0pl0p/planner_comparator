import os
from utils.azure_openai import client
from dotenv import load_dotenv

load_dotenv()

def judge_outputs(prompt_plan: str, prolog_plan: str, judge_type: str = "plans") -> str:
    if judge_type == "plans":
        system_prompt = os.getenv("JUDGE_PROMPT_SYSTEM_PLANS")
        user_prompt_template = os.getenv("JUDGE_PROMPT_USER_TEMPLATE_PLANS")
    elif judge_type == "analysis":
        system_prompt = os.getenv("JUDGE_PROMPT_SYSTEM_ANALYSIS")
        user_prompt_template = os.getenv("JUDGE_PROMPT_USER_TEMPLATE_ANALYSIS")
    else:
        raise ValueError("Invalid judge_type provided.")

    if not system_prompt or not user_prompt_template:
        raise ValueError("Required prompts not found in environment variables.")

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
