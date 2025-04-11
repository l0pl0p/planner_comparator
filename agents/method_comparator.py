import os
import re
from utils.client import client
from dotenv import load_dotenv
from agents.prompt_persona import generate_legal_plan_prompt_persona
from agents.prolog_reasoner import generate_legal_plan_prolog
from agents.evaluation_methods import comprehensive_evaluation
from utils.template_loader import render_template

load_dotenv()

MODEL_PLAN_GENERATION = os.getenv("MODEL_PLAN_GENERATION")
MODEL_EXECUTION = os.getenv("MODEL_EXECUTION")
MODEL_JUDGE = os.getenv("MODEL_JUDGE")
DOMAIN= os.getenv("DOMAIN")


def execute_plan(plan: str, user_question: str) -> str:
    response = client.chat.completions.create(
        model=MODEL_EXECUTION,
        messages=[
            {"role": "system", "content": plan},
            {"role": "user", "content": user_question}
        ]
    )
    return response.choices[0].message.content.strip()


def comparative_judgment(output_a: str, output_b: str, original_question: str) -> dict:
    system_prompt = render_template(
        "comparative_judgment.jinja",
        output_a=output_a,
        output_b=output_b,
        original_question=original_question
    )
    response = client.chat.completions.create(
        model=MODEL_JUDGE,
        messages=[{"role": "system", "content": system_prompt}]
    )
    full_text = response.choices[0].message.content.strip()

    scores_a, scores_b = parse_comparative_scores(full_text)

    return {
        "text": full_text,
        "scores": {
            "traditional": scores_a,
            "neuro_symbolic": scores_b
        }
    }

def parse_comparative_scores(text: str):
    pattern = r'\|\s*(Accuracy|Quality|Completeness|Adaptability|Domain Relevance|Robustness)\s*\|\s*(\d)\s*\|\s*(\d)\s*\|'
    matches = re.findall(pattern, text)

    scores_a = {criterion: int(a_score) for criterion, a_score, _ in matches}
    scores_b = {criterion: int(b_score) for criterion, _, b_score in matches}

    return scores_a, scores_b



# Primary workflow function:
def evaluate_methods(user_question: str, domain: str = DOMAIN) -> dict:
    # Generate research plans
    plan_traditional = generate_legal_plan_prompt_persona(user_question)
    plan_neurosymbolic = generate_legal_plan_prolog(user_question)

    # Comprehensive evaluations
    eval_plan_traditional = comprehensive_evaluation(plan_traditional, domain)
    eval_plan_neurosymbolic = comprehensive_evaluation(plan_neurosymbolic, domain)

    # Execute plans if you want to comapre results of plan in simple pipeline, add switch for this in future
    # output_traditional = execute_plan(plan_traditional, user_question)
    # output_neurosymbolic = execute_plan(plan_neurosymbolic, user_question)

    # Comparative judgment with structured scores
    final_comparison = comparative_judgment(eval_plan_traditional, eval_plan_neurosymbolic, user_question)

    return {
        "traditional": {
            "plan": plan_traditional,
            #"output": output_traditional,
            "evaluation": eval_plan_traditional
        },
        "neuro_symbolic": {
            "plan": plan_neurosymbolic,
            #"output": output_neurosymbolic,
            "evaluation": eval_plan_neurosymbolic
        },
        "final_judgment": final_comparison["text"],
        "final_judgment_scores": final_comparison["scores"]
    }
