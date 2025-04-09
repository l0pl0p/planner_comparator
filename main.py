import os
from dotenv import load_dotenv
from agents.prompt_persona import generate_legal_plan_prompt_persona
from agents.prolog_reasoner import generate_legal_plan_prolog
from agents.judge import judge_outputs

load_dotenv()

def main():
    subject = os.getenv("SUBJECT")

    print("Generating legal research plan using prompt persona...")
    prompt_output = generate_legal_plan_prompt_persona(subject)

    print("Generating legal research plan using Prolog approach...")
    prolog_output = generate_legal_plan_prolog(subject)

    print("Judging both outputs...")
    result = judge_outputs(prompt_output, prolog_output)

    print("\n🔍 Subject:", subject)
    print("\n🧠 Prompt Persona Output:\n", prompt_output)
    print("\n🧠 Prolog Output:\n", prolog_output)
    print("\n⚖️ Judgment:\n", result)

if __name__ == "__main__":
    main()
