import os

TEMPLATE_FILES_CONTENT = {
    "prompt_persona_system_message.jinja": "Develop a detailed {{ domain }} analysis, decomposing queries into interpretations, highlighting conflicts and complexities, and clearly reasoning through relevant frameworks.",

    "prolog_structure_prompt.jinja": "Generate structured PROLOG code clearly decomposing {{ domain }} queries into logical predicates, capturing nuances and practical considerations, ensuring readability and clear documentation.",

    "judge_system_prompt_plans.jinja": "You're an expert evaluator assessing the quality of {{ domain }} research plans. Evaluate clarity, completeness, precision, relevance, and logical coherence. Clearly state which plan is superior and why.",

    "judge_user_prompt_plans.jinja": "Evaluate these two {{ domain }} research plans. State clearly which plan is superior and why.\n\nPlan A:\n{{ prompt_plan }}\n\nPlan B:\n{{ prolog_plan }}",

    "judge_system_prompt_analysis.jinja": "You're an expert {{ domain }} analyst evaluating analyses for thoroughness, insight, accuracy, and practical guidance. Clearly determine the superior analysis and justify your decision.",

    "judge_user_prompt_analysis.jinja": "Evaluate these analyses. State clearly which analysis is superior and why.\n\nAnalysis A:\n{{ prompt_plan }}\n\nAnalysis B:\n{{ prolog_plan }}",

    "prolog_facts_system_prompt.jinja": "You are a {{ domain }} logician. Extract key concepts, relationships, and rules as Prolog-style facts and rules.",

    "prolog_facts_user_prompt.jinja": "Generate symbolic logic for this {{ domain }} subject:\n{{ subject }}",

    "prolog_reasoner_system_prompt.jinja": "You are a {{ domain }} research assistant that reasons using symbolic logic. Given symbolic rules and a subject, produce a comprehensive research plan.",

    "prolog_reasoner_user_prompt.jinja": "Here are Prolog-style facts and rules:\n{{ prolog_facts }}\nBased on these, create a detailed {{ domain }} research plan for the subject:\n{{ subject }}",

    "holistic_evaluation.jinja": "You are tasked with performing a holistic evaluation of the provided {{ domain }} research plan. Evaluate the following dimensions on a scale from 1 (poor) to 5 (excellent): 1. Accuracy: ___, 2. Clarity: ___, 3. Completeness: ___, 6. Robustness: ___. Provide a brief justification for each score. Research Plan: {{ plan }}",

    "domain_specific_evaluation.jinja": "Perform a domain-specific evaluation for the {{ domain }} domain. Consider domain standards, regulatory compliance, safety implications, and ethical considerations. Provide numerical scores (1-5) with justification. Evaluate the following dimensions on a scale from 1 (poor) to 5 (excellent): 1. Accuracy: ___, 2. Clarity: ___, 3. Completeness: ___, 6. Robustness: ___. Provide a brief justification for each score. Research Plan: {{ plan }}",

    "safety_ethics_evaluation.jinja": "Evaluate the provided {{domain}} research plan for ethical implications and potential safety risks. Identify areas that could lead to ethical concerns or unsafe recommendations. Evaluate the following dimensions on a scale from 1 (poor) to 5 (excellent): 1. Accuracy: ___, 2. Clarity: ___, 3. Completeness: ___, 6. Robustness: ___. Provide a brief justification for each score. Research Plan: {{ plan }}",

    "comparative_judgment.jinja": "Evaluate the following two answers based on accuracy, completeness, domain relevance, and robustness in the {{ domain }} domain; assign numerical scores (1-5) for each criterion and clearly state which answer is superior and why. Original Question: {{ original_question }} | Answer A: {{ output_a }} | Answer B: {{ output_b }}"
}

TEMPLATE_DIR = "templates"
ENV_FILE = ".env"
SHELL_SCRIPT = "create_templates.sh"

ENV_CONTENT = """MODEL_PROMPT_PERSONA=gpt-4o
MODEL_PROLOG_FACTS=o1
MODEL_PROLOG_REASONER=o1
MODEL_JUDGE=gpt-4o
MODEL_EXECUTE_PLAN=gpt-4o
MODEL_FOLLOW_UP=gpt-4o
SUBJECTS_FILE=questions.json
NUM_QUESTIONS=1
RANDOMIZE_QUESTIONS=true
LOG_LEVEL=medium
LOG_FILE=evaluation_log.txt
DOMAIN=legal
PROVIDER=azure
OPENAI_API_KEY=<your_api_key>
AZURE_OPENAI_API_KEY=<your_api_key>
AZURE_OPENAI_ENDPOINT=<your_https_endpoint>
AZURE_API_VERSION=<version>
"""

def create_dir_if_missing(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        print(f"Created directory: {dir_name}")
    else:
        print(f"Directory already exists: {dir_name}")

def create_files_if_missing(directory, files_content):
    for file, content in files_content.items():
        path = os.path.join(directory, file)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Created file: {path}")
        else:
            print(f"File already exists: {path}")

def create_shell_script_if_missing():
    if not os.path.exists(SHELL_SCRIPT):
        with open(SHELL_SCRIPT, "w", encoding="utf-8") as f:
            f.write("#!/bin/bash\nmkdir -p templates")
        os.chmod(SHELL_SCRIPT, 0o755)
        print(f"Created shell script: {SHELL_SCRIPT}")
    else:
        print(f"Shell script already exists: {SHELL_SCRIPT}")

def create_env_file_if_missing():
    if not os.path.exists(ENV_FILE):
        with open(ENV_FILE, "w", encoding="utf-8") as f:
            f.write(ENV_CONTENT)
        print(f"Created environment file: {ENV_FILE}")
    else:
        print(f"Environment file already exists: {ENV_FILE}")

def setup():
    create_dir_if_missing(TEMPLATE_DIR)
    create_files_if_missing(TEMPLATE_DIR, TEMPLATE_FILES_CONTENT)
    create_shell_script_if_missing()
    create_env_file_if_missing()

if __name__ == "__main__":
    setup()
