from utils.client import client
import os
from utils.template_loader import render_template

MODEL_PROMPT_PERSONA = os.getenv("MODEL_PROMPT_PERSONA", "gpt-4o")

def generate_legal_plan_prompt_persona(subject: str) -> str:
    system_prompt = render_template("prompt_persona_system_message.jinja")
    user_prompt = f"Create a legal research plan for: {subject}"

    response = client.chat.completions.create(
        model=MODEL_PROMPT_PERSONA,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content.strip()
