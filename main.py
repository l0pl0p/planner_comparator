import os
import json
import random
from dotenv import load_dotenv
from datetime import datetime
from agents.method_comparator import evaluate_methods
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

def main():
    config = load_config()
    subjects = load_subjects(config["subjects_file"], config["num_questions"], config["randomize_questions"])
    domain = config["domain"]
    print(f"Running evaluation sequentially on {len(subjects)} question(s).")

    criteria = ['Accuracy', 'Quality', 'Completeness', 'Adaptability', 'Domain Relevance', 'Robustness']
    eval_types = ['holistic', 'domain_specific', 'safety_ethics']

    cumulative_totals = {'Traditional':{c:[] for c in criteria}, 'Neuro-symbolic':{c:[] for c in criteria}}
    question_aggregates = []

    for idx, subject in enumerate(subjects, 1):
        print(f"Processing Question #{idx}: {subject}")

        # ** use evaluate_methods to execute the full pipeline **
        results = evaluate_methods(subject, domain)

        trad_plan = results['traditional']['plan']
        neuro_plan = results['neuro_symbolic']['plan']

        trad_eval = results['traditional']['evaluation']
        neuro_eval = results['neuro_symbolic']['evaluation']

        final_judgment = results['final_judgment']
        final_judgment_scores = results['final_judgment_scores']

        # Optional: Log the inference details if configured
        if config["log_level"] >= LOG_LEVELS["high"]:
            inference_log = (
                f"Question #{idx}: {subject}\n\n"
                "--- Traditional Plan & Output ---\n"
                f"{trad_plan}\n\n"
                "--- Neuro-symbolic Plan & Output ---\n"
                f"{neuro_plan}\n\n"
                "--- Final Comparative Judgment of Plans ---\n"
                f"{final_judgment}"
            )
            log_result("high", inference_log, config)

        # Construct detailed scoring table
        detailed_table = f"Question #{idx}: {subject}\n\n"
        for eval_type in eval_types:
            detailed_table += f"### {eval_type.replace('_', ' ').title()} Scores\n"
            detailed_table += "| Criterion         | Traditional | Neuro-symbolic |\n"
            detailed_table += "|-------------------|-------------|----------------|\n"
            trad_total, neuro_total, trad_count, neuro_count = 0, 0, 0, 0
            for criterion in criteria:
                t_score = trad_eval[eval_type]['scores'].get(criterion, 'N/A')
                n_score = neuro_eval[eval_type]['scores'].get(criterion, 'N/A')
                detailed_table += f"| {criterion:<17} | {str(t_score):^11} | {str(n_score):^14} |\n"

                if isinstance(t_score, int):
                    trad_total += t_score
                    trad_count += 1
                if isinstance(n_score, int):
                    neuro_total += n_score
                    neuro_count += 1

            trad_avg = round(trad_total/trad_count,2) if trad_count else 'N/A'
            neuro_avg = round(neuro_total/neuro_count,2) if neuro_count else 'N/A'

            detailed_table += "|-------------------|-------------|----------------|\n"
            detailed_table += f"| **Average**       | {trad_avg:^11} | {neuro_avg:^14} |\n\n"

        log_result("medium", detailed_table, config)

        # Aggregation logic
        q_aggregate = {'Traditional':{}, 'Neuro-symbolic':{}}
        for criterion in criteria:
            trad_scores = [trad_eval[et]['scores'].get(criterion) for et in eval_types if isinstance(trad_eval[et]['scores'].get(criterion), int)]
            neuro_scores = [neuro_eval[et]['scores'].get(criterion) for et in eval_types if isinstance(neuro_eval[et]['scores'].get(criterion), int)]

            trad_avg = round(sum(trad_scores)/len(trad_scores),2) if trad_scores else 'N/A'
            neuro_avg = round(sum(neuro_scores)/len(neuro_scores),2) if neuro_scores else 'N/A'

            q_aggregate['Traditional'][criterion] = trad_avg
            q_aggregate['Neuro-symbolic'][criterion] = neuro_avg

            cumulative_totals['Traditional'][criterion] += trad_scores
            cumulative_totals['Neuro-symbolic'][criterion] += neuro_scores

        question_aggregates.append((subject, q_aggregate))

    final_log = f"FINAL BATCH AGGREGATED SUMMARY\nDomain: {domain}\n{'='*80}\n"

    for idx, (subject, totals) in enumerate(question_aggregates,1):
        final_log += f"\n### Question #{idx} Aggregates: {subject}\n"
        final_log += "| Criterion         | Traditional | Neuro-symbolic |\n"
        final_log += "|-------------------|-------------|----------------|\n"
        for criterion in criteria:
            t = totals['Traditional'][criterion]
            n = totals['Neuro-symbolic'][criterion]
            final_log += f"| {criterion:<17} | {t:^11} | {n:^14} |\n"

    final_log += f"\n{'-'*80}\n### Final Aggregate (All Questions Combined)\n"
    final_log += "| Criterion         | Traditional | Neuro-symbolic |\n"
    final_log += "|-------------------|-------------|----------------|\n"
    grand_trad, grand_neuro = [], []
    for criterion in criteria:
        trad_list = cumulative_totals['Traditional'][criterion]
        neuro_list = cumulative_totals['Neuro-symbolic'][criterion]

        trad_final_avg = round(sum(trad_list)/len(trad_list),2) if trad_list else 'N/A'
        neuro_final_avg = round(sum(neuro_list)/len(neuro_list),2) if neuro_list else 'N/A'

        grand_trad += trad_list
        grand_neuro += neuro_list

        final_log += f"| {criterion:<17} | {trad_final_avg:^11} | {neuro_final_avg:^14} |\n"

    trad_grand_avg = round(sum(grand_trad)/len(grand_trad),2) if grand_trad else 'N/A'
    neuro_grand_avg = round(sum(grand_neuro)/len(grand_neuro),2) if grand_neuro else 'N/A'

    final_log += "|-------------------|-------------|----------------|\n"
    final_log += f"| **Grand Avg**     | {trad_grand_avg:^11} | {neuro_grand_avg:^14} |\n"
    final_log += f"{'='*80}\n"

    log_result("low", final_log, config)

if __name__ == "__main__":
    main()
