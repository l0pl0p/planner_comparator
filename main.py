import os
from dotenv import load_dotenv
from utils.azure_openai import client
from agents.prompt_persona import generate_legal_plan_prompt_persona
from agents.prolog_reasoner import generate_legal_plan_prolog
from agents.judge import judge_outputs

load_dotenv()

def llm_follow_up(system_prompt: str, user_prompt: str) -> str:
    response = client.chat.completions.create(
        model=os.getenv("AZURE_MODEL_EXECUTE_PLAN"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content.strip()


def main():
    subject = os.getenv("SUBJECT")

    print("Generating legal research plan using prompt persona...")
    prompt_plan = generate_legal_plan_prompt_persona(subject)

    print("Generating legal research plan using Prolog approach...")
    prolog_plan = generate_legal_plan_prolog(subject)

    print("Executing follow-up with prompt persona plan...")
    prompt_followup_output = llm_follow_up(prompt_plan, subject)

    print("Executing follow-up with prolog persona plan...")
    prolog_followup_output = llm_follow_up(prolog_plan, subject)

    print("Judging both follow-up outputs...")
    judgment = judge_outputs(prompt_followup_output, prolog_followup_output)

    print("\n🔍 Subject:", subject)
    print("\n🧠 Prompt Persona Plan:\n", prompt_plan)
    print("\n📝 Prompt Persona Follow-up Output:\n", prompt_followup_output)
    print("\n🧠 Prolog Plan:\n", prolog_plan)
    print("\n📝 Prolog Persona Follow-up Output:\n", prolog_followup_output)
    print("\n⚖️ Judgment:\n", judgment)

if __name__ == "__main__":
    main()