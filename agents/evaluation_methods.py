import os
import re
from utils.client import client
from utils.template_loader import render_template

MODEL_JUDGE = os.getenv("MODEL_JUDGE")

def holistic_evaluation(plan: str, domain: str) -> str:
    system_prompt = render_template("holistic_evaluation.jinja", plan=plan, domain=domain)
    response = client.chat.completions.create(
        model=MODEL_JUDGE,
        messages=[{"role": "system", "content": system_prompt}]
    )
    return response.choices[0].message.content.strip()

def domain_specific_evaluation(plan: str, domain: str) -> str:
    system_prompt = render_template("domain_specific_evaluation.jinja", plan=plan, domain=domain)
    response = client.chat.completions.create(
        model=MODEL_JUDGE,
        messages=[{"role": "system", "content": system_prompt}]
    )
    return response.choices[0].message.content.strip()

def evaluate_safety_and_ethics(plan: str, domain: str) -> str:
    system_prompt = render_template("safety_ethics_evaluation.jinja", plan=plan, domain=domain)
    response = client.chat.completions.create(
        model=MODEL_JUDGE,
        messages=[{"role": "system", "content": system_prompt}]
    )
    return response.choices[0].message.content.strip()

def comparative_judgment(output_a: str, output_b: str, original_question: str, domain: str) -> str:
    system_prompt = render_template(
        "comparative_judgment.jinja",
        output_a=output_a,
        output_b=output_b,
        original_question=original_question,
        domain=domain
    )
    response = client.chat.completions.create(
        model=MODEL_JUDGE,
        messages=[{"role": "system", "content": system_prompt}]
    )
    return response.choices[0].message.content.strip()

def parse_scores(evaluation_text: str) -> dict:
    scores = re.findall(r'(Accuracy|Clarity|Completeness|Biases|Ethical|Robustness|Domain Relevance|Overall Robustness):.*?(\d)', evaluation_text)
    return {criterion: int(score) for criterion, score in scores}

def comprehensive_evaluation(plan: str, domain: str) -> dict:
    holistic_text = holistic_evaluation(plan, domain)
    domain_text = domain_specific_evaluation(plan, domain)
    safety_ethics_text = evaluate_safety_and_ethics(plan, domain)

    return {
        "holistic": {
            "text": holistic_text,
            "scores": parse_scores(holistic_text)
        },
        "domain_specific": {
            "text": domain_text,
            "scores": parse_scores(domain_text)
        },
        "safety_ethics": {
            "text": safety_ethics_text,
            "scores": parse_scores(safety_ethics_text)
        }
    }
