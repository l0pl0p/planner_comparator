from utils.azure_openai import client
import os

def generate_prolog_facts(subject: str) -> str:
    system_prompt = os.getenv("PROLOG_FACTS_SYSTEM_PROMPT")
    user_prompt = os.getenv("PROLOG_FACTS_USER_PROMPT").replace("{subject}", subject)

    response = client.chat.completions.create(
        model=os.getenv("AZURE_MODEL_PROLOG_FACTS"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def reason_with_prolog_facts(subject: str, prolog_facts: str) -> str:
    system_prompt = os.getenv("PROLOG_REASONER_SYSTEM_PROMPT")
    user_prompt = os.getenv("PROLOG_REASONER_USER_PROMPT") \
        .replace("{prolog_facts}", prolog_facts) \
        .replace("{subject}", subject)

    response = client.chat.completions.create(
        model=os.getenv("AZURE_MODEL_PROLOG_REASONER"),
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
