import os
from dotenv import load_dotenv
from utils.client import client
from utils.template_loader import render_template

load_dotenv()

MODEL_JUDGE = os.getenv("MODEL_JUDGE")

def judge_outputs(prompt_plan: str, prolog_plan: str, judge_type: str = "plans") -> str:
    if judge_type == "plans":
        system_prompt = render_template("judge_system_prompt_plans.jinja")
        user_prompt = render_template(
            "judge_user_prompt_plans.jinja",
            prompt_plan=prompt_plan,
            prolog_plan=prolog_plan
        )
    elif judge_type == "analysis":
        system_prompt = render_template("judge_system_prompt_analysis.jinja")
        user_prompt = render_template(
            "judge_user_prompt_analysis.jinja",
            prompt_plan=prompt_plan,
            prolog_plan=prolog_plan
        )
    else:
        raise ValueError("Invalid judge_type provided.")

    response = client.chat.completions.create(
        model=MODEL_JUDGE,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return response.choices[0].message.content.strip()
