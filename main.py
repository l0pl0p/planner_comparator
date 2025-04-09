import os
from dotenv import load_dotenv
from utils.azure_openai import client
from agents.prompt_persona import generate_legal_plan_prompt_persona
from agents.prolog_reasoner import generate_legal_plan_prolog
from agents.judge import judge_outputs
from datetime import datetime

load_dotenv()

LOG_MODE = os.getenv("LOG_MODE", "verbose")  # Set to 'verbose' or 'eval_only'
LOG_FILE = os.getenv("LOG_FILE", "evaluation_log.txt")

def llm_follow_up(system_prompt: str, user_prompt: str) -> str:
    response = client.chat.completions.create(
        model=os.getenv("AZURE_MODEL_FOLLOW_UP"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def log_results(content: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as file:
        file.write(f"[{timestamp}]\n{content}\n{'-'*80}\n")

def main():
    subject = os.getenv("SUBJECT")

    prompt_plan = generate_legal_plan_prompt_persona(subject)
    prolog_plan = generate_legal_plan_prolog(subject)

    direct_plan_judgment = judge_outputs(prompt_plan, prolog_plan, judge_type="plans")

    prompt_analysis = llm_follow_up(prompt_plan, subject)
    prolog_analysis = llm_follow_up(prolog_plan, subject)

    analysis_based_judgment = judge_outputs(prompt_analysis, prolog_analysis, judge_type="analysis")

    if LOG_MODE == "verbose":
        verbose_log = (f"Subject: {subject}\n\n"
                       f"Prompt Plan:\n{prompt_plan}\n\n"
                       f"Prolog Plan:\n{prolog_plan}\n\n"
                       f"Direct Plan Judgment:\n{direct_plan_judgment}\n\n"
                       f"Prompt Analysis:\n{prompt_analysis}\n\n"
                       f"Prolog Analysis:\n{prolog_analysis}\n\n"
                       f"Analysis-Based Judgment:\n{analysis_based_judgment}")
        log_results(verbose_log)
    elif LOG_MODE == "eval_only":
        eval_only_log = (f"Subject: {subject}\n\n"
                         f"Prompt Analysis:\n{prompt_analysis}\n\n"
                         f"Prolog Analysis:\n{prolog_analysis}\n\n"
                         f"Analysis-Based Judgment:\n{analysis_based_judgment}")
        log_results(eval_only_log)

    print("Evaluation completed and logged.")

if __name__ == "__main__":
    main()
