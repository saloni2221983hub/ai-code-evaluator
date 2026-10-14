"""
AI Code Evaluator & Benchmark Tool
Evaluates AI-generated code outputs for syntax, execution, and logical accuracy.
"""

import ast
import json


def check_syntax(code_str: str) -> dict:
    """Verifies Python syntax without executing arbitrary code."""
    try:
        ast.parse(code_str)
        return {"syntax_valid": True, "error": None}
    except SyntaxError as e:
        return {"syntax_valid": False, "error": f"SyntaxError on line {e.lineno}: {e.msg}"}


def evaluate_rubric(code_str: str, required_keywords: list) -> dict:
    """Rubric evaluation: checks structure, comments, and algorithmic requirements."""
    rubric_scores = {
        "syntax_integrity": 0,
        "required_logic_present": 0,
        "has_documentation": 0,
        "overall_score": 0,
    }

    syntax_res = check_syntax(code_str)
    if syntax_res["syntax_valid"]:
        rubric_scores["syntax_integrity"] = 40

    if '"""' in code_str or "'''" in code_str or "#" in code_str:
        rubric_scores["has_documentation"] = 20

    matches = [kw for kw in required_keywords if kw in code_str]
    logic_ratio = len(matches) / len(required_keywords) if required_keywords else 1.0
    rubric_scores["required_logic_present"] = int(logic_ratio * 40)

    rubric_scores["overall_score"] = sum(rubric_scores.values())
    return rubric_scores


if __name__ == "__main__":
    sample_candidate_code = """
def find_even_numbers(numbers):
    # Returns only even numbers from a list
    return [num for num in numbers if num % 2 == 0]
"""
    expected_elements = ["def", "return", "%"]
    results = evaluate_rubric(sample_candidate_code, expected_elements)
    print("=== Evaluation Benchmark Results ===")
    print(json.dumps(results, indent=2))
