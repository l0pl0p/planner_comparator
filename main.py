import os
from dotenv import load_dotenv
from utils.azure_openai import client
from agents.prompt_persona import generate_legal_plan_prompt_persona
from agents.prolog_reasoner import generate_legal_plan_prolog
from agents.judge import judge_outputs

load_dotenv()

def llm_follow_up(system_prompt: str, user_prompt: str) -> str:
    response = client.chat.completions.create(
        model=os.getenv("AZURE_MODEL_FOLLOW_UP"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def main():
    subject = os.getenv("SUBJECT")

    print("🔹 Generating research plans...")
    prompt_plan = generate_legal_plan_prompt_persona(subject)
    prolog_plan = generate_legal_plan_prolog(subject)

    print("\n🔸 Directly judging the research plans (Path 1)...")
    direct_plan_judgment = judge_outputs(prompt_plan, prolog_plan, judge_type="plans")

    print("\n🔹 Generating analyses from each research plan...")
    prompt_analysis = llm_follow_up(prompt_plan, subject)
    prolog_analysis = llm_follow_up(prolog_plan, subject)

    print("\n🔸 Judging plans via guided analyses (Path 2)...")
    analysis_based_judgment = judge_outputs(prompt_analysis, prolog_analysis, judge_type="analysis")

    # Clearly print your structured results
    print("\n=== Results Summary ===")
    print(f"🔍 Subject:\n{subject}\n")

    print("🗒️ Prompt-based Research Plan:\n", prompt_plan, "\n")
    print("🗒️ Prolog-based Research Plan:\n", prolog_plan, "\n")
    print("🧑‍⚖️ Direct Plan Judgment (Path 1):\n", direct_plan_judgment, "\n")

    print("📚 Prompt-guided Analysis:\n", prompt_analysis, "\n")
    print("📚 Prolog-guided Analysis:\n", prolog_analysis, "\n")
    print("🧑‍⚖️ Analysis-Based Judgment (Path 2):\n", analysis_based_judgment)

if __name__ == "__main__":
    main()
