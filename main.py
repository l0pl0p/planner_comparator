import os
import json
import random
from dotenv import load_dotenv
from datetime import datetime
from agents.method_comparator import comprehensive_evaluation
from utils.template_loader import render_template

load_dotenv()

LOG_LEVELS = {"low": 1, "medium": 2, "high": 3}

def load_config():
    return {
        "log_level": LOG_LEVELS.get(os.getenv("LOG_LEVEL").lower(), 1),
        "log_file": os.getenv("LOG_FILE"),
        "subjects_file": os.getenv("SUBJECTS_FILE"),
        "num_questions": int(os.getenv("NUM_QUESTIONS")),
        "randomize_questions": os.getenv("RANDOMIZE_QUESTIONS").lower() == "true",
        "domain": os.getenv("DOMAIN")
    }

def load_subjects(subjects_file, num_questions, randomize):
    with open(subjects_file, "r", encoding="utf-8") as file:
        subjects = json.load(file)
    return random.sample(subjects, min(num_questions, len(subjects))) if randomize else subjects[:num_questions]

def log_result(log_level, content, config):
    required_level = LOG_LEVELS.get(log_level, 1)
    if required_level <= config["log_level"]:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_path = os.path.abspath(config["log_file"])
        try:
            with open(log_path, "a+", encoding="utf-8") as file:
                file.write(f"[{timestamp}] [{log_level.upper()}]\n{content}\n{'-'*80}\n")
            print(f"Logged ({log_level}) to {log_path}")
        except Exception as e:
            print(f"Logging failed ({log_level}): {e}")

def aggregate_scores(eval_dict):
    aggregated = {}
    for evaluation in eval_dict.values():
        for criterion, score in evaluation['scores'].items():
            aggregated[criterion] = aggregated.get(criterion, 0) + score
    return aggregated

def main():
    config = load_config()
    subjects = load_subjects(config["subjects_file"], config["num_questions"], config["randomize_questions"])
    domain = config["domain"]

    print(f"Running evaluation sequentially on {len(subjects)} question(s).")
    final_results = []

    for idx, subject in enumerate(subjects, 1):
        print(f"Processing Question #{idx}: {subject}")
        
        try:
            trad_plan = render_template("prompt_persona_system_message.jinja", question=subject)
            neuro_plan = render_template("prolog_structure_prompt.jinja", question=subject)

            trad_eval = comprehensive_evaluation(trad_plan, domain)
            neuro_eval = comprehensive_evaluation(neuro_plan, domain)

            scores_trad = aggregate_scores(trad_eval)
            scores_neuro = aggregate_scores(neuro_eval)

            criteria = ['Accuracy', 'Clarity', 'Completeness', 'Domain Relevance', 'Robustness']
            eval_types = ['holistic', 'domain_specific', 'safety_ethics']

            total_trad = total_neuro = 0

            # Header
            eval_table = f"Question #{idx}: {subject}\n\n"

            # Detailed per-type scores
            for eval_type in eval_types:
                eval_table += f"### {eval_type.replace('_', ' ').title()} Scores\n"
                eval_table += "| Criterion         | Traditional | Neuro-symbolic |\n"
                eval_table += "|-------------------|-------------|----------------|\n"
                
                for criterion in criteria:
                    trad_score = trad_eval[eval_type]['scores'].get(criterion, 'N/A')
                    neuro_score = neuro_eval[eval_type]['scores'].get(criterion, 'N/A')
                    eval_table += f"| {criterion:<17} | {str(trad_score):^11} | {str(neuro_score):^14} |\n"
                eval_table += "\n"

            # Aggregated summary scores
            for criterion in criteria:
                trad_score = scores_trad.get(criterion, 'N/A')
                neuro_score = scores_neuro.get(criterion, 'N/A')
                total_trad += trad_score if isinstance(trad_score, int) else 0
                total_neuro += neuro_score if isinstance(neuro_score, int) else 0

            # Logging medium-level detailed scores
            log_result("medium", eval_table, config)

            detailed_log = (
                f"{eval_table}\n\n"
                f"Trad Prompt Engineered Detailed Evaluation:\n"
                f"Holistic:\n{trad_eval['holistic']['text']}\n\n"
                f"Domain Specific:\n{trad_eval['domain_specific']['text']}\n\n"
                f"Safety Ethics:\n{trad_eval['safety_ethics']['text']}\n\n"
                f"Neuro-symbolic Detailed Evaluation:\n"
                f"Holistic:\n{neuro_eval['holistic']['text']}\n\n"
                f"Domain Specific:\n{neuro_eval['domain_specific']['text']}\n\n"
                f"Safety Ethics:\n{neuro_eval['safety_ethics']['text']}"
            )


            log_result("high", detailed_log, config)

            final_results.append(eval_table)

        except Exception as e:
            error_msg = f"Error processing Question #{idx}: {subject}\n{e}"
            print(error_msg)
            log_result("high", error_msg, config)
            final_results.append(error_msg)

    overall_judgment = ("\n" + "-" * 21 + "\n").join(final_results)
    # Accumulate totals during your evaluation loop
    final_results_summary = []

    for idx, subject in enumerate(subjects, 1):
        # existing evaluation logic here...

        # Aggregate summary per question (exactly your "Aggregated Scores" table)
        summary_table = (
            f"Question #{idx}: {subject}\n\n"
            "### Aggregated Scores\n"
            "| Criterion         | Traditional | Neuro-symbolic |\n"
            "|-------------------|-------------|----------------|\n"
        )

        criteria = ['Accuracy', 'Clarity', 'Completeness', 'Domain Relevance', 'Robustness']
        for criterion in criteria:
            trad_score = scores_trad.get(criterion, 'N/A')
            neuro_score = scores_neuro.get(criterion, 'N/A')
            summary_table += f"| {criterion:<17} | {str(trad_score):^11} | {str(neuro_score):^14} |\n"

        summary_table += "|-------------------|-------------|----------------|\n"
        summary_table += f"| **Total**         | {total_trad:^11} | {total_neuro:^14} |\n"

        final_results_summary.append(summary_table)

    # After the loop completes, log only aggregated summaries at LOW level
    final_log_content = (
        f"FINAL BATCH AGGREGATED SUMMARY\nDomain: {domain}\n{'='*80}\n"
        + ("\n" + "-" * 80 + "\n").join(final_results_summary) +
        f"\n{'='*80}"
    )

    log_result("low", final_log_content, config)


    print("Sequential evaluation completed and final judgment logged.")

if __name__ == "__main__":
    main()
