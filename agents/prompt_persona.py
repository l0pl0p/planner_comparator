from utils.azure_openai import client
import os

def generate_legal_plan_prompt_persona(subject: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": os.getenv("PROMPT_PERSONA_SYSTEM_MESSAGE")},
            {"role": "user", "content": f"Create a legal research plan for: {subject}"}
        ]
    )
    return response.choices[0].message.content.strip()
