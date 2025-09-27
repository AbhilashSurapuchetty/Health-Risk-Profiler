from typing import Dict, Any, List

def too_many_missing_guardrail(answers: Dict[str, Any], missing_fields: List[str]) -> bool:
    total = len(answers.keys())
    missing = len(missing_fields)
    return (missing / total) > 0.5
