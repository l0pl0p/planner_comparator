# Legal Research Plan Comparator

This project provides scaffolding to compare two AI-driven methods for auto-generating domain research plans.

Credit to rXiv:2502.17638 for the idea!

## Approaches Compared

### 1. **Prompt-Engineered Persona Approach**  
Generates domain plans using persona-driven natural language prompts.

### 2. **Neuro-Symbolic (Prolog) Reasoning Approach**  
Generates domain plans based on structured symbolic logic using Prolog facts and rules.

### 3. **Judge Agent**  
A GPT-powered evaluator that compares both approaches and identifies the superior plan.

## Project Flexibility

This scaffolding is designed for **experimentation, prototyping, and customization**. You can easily:

- **Extend or modify reasoning methods**
- **Implement alternative evaluation criteria**
- **Add interfaces** such as CLI, API, logging, tests, or a user interface

## Quick Start

Run the setup script once to initialize the required files and configurations:

```bash
python setup.py

## Important Notes

- **The setup script will not overwrite existing files.**
- Templates and environment files provided are **initial examples**.
- For best results, **customize the prompts** located in the `template_sources` directory.

## Results Example

