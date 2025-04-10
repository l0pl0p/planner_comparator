from utils.client import client
import os
from utils.template_loader import render_template

MODEL_PROLOG_FACTS = os.getenv("MODEL_PROLOG_FACTS", "gpt-4o")
MODEL_PROLOG_REASONER = os.getenv("MODEL_PROLOG_REASONER", "gpt-4o")

def generate_prolog_facts(subject: str) -> str:
    system_prompt = render_template("prolog_facts_system_prompt.jinja")
    user_prompt = render_template("prolog_facts_user_prompt.jinja", subject=subject)

    response = client.chat.completions.create(
        model=MODEL_PROLOG_FACTS,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def reason_with_prolog_facts(subject: str, prolog_facts: str) -> str:
    system_prompt = render_template("prolog_reasoner_system_prompt.jinja")
    user_prompt = render_template(
        "prolog_reasoner_user_prompt.jinja",
        subject=subject,
        prolog_facts=prolog_facts
    )

    response = client.chat.completions.create(
        model=MODEL_PROLOG_REASONER,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def generate_legal_plan_prolog(subject: str) -> str:
    prolog_facts = generate_prolog_facts(subject)
    reasoning_output = reason_with_prolog_facts(subject, prolog_facts)
    return reasoning_output