# risk_engine.py
from typing import Dict, Any, List

# Scoring weights for each health factor
WEIGHTS = {
    "smoking": 25,
    "poor_diet": 20,
    "low_exercise": 15,
    "age_over_40": 10,
    "high_stress": 10,
    "high_blood_pressure": 10,
    "diabetes": 15,
    "high_cholesterol": 10,
    "obesity": 15,
    "poor_sleep": 10,
    "alcohol_use": 10
}

# Map factors to human-readable rationale
FACTOR_RATIONALE = {
    "smoking": "smoking",
    "poor_diet": "unhealthy diet",
    "low_exercise": "low physical activity",
    "age_over_40": "age over 40",
    "high_stress": "high stress",
    "high_blood_pressure": "high blood pressure",
    "diabetes": "diabetes",
    "high_cholesterol": "high cholesterol",
    "obesity": "obesity",
    "poor_sleep": "poor sleep",
    "alcohol_use": "alcohol consumption"
}

def extract_factors(answers: Dict[str, Any], detected_factors: List[str] = []) -> Dict:
    """
    Convert answers + parser-detected health keywords into factors list
    """
    factors = set(detected_factors)

    # Add structured checks from answers
    if answers.get("smoker") is True:
        factors.add("smoking")

    diet = (answers.get("diet") or "").lower()
    if any(k in diet for k in ["sugar", "high sugar", "junk", "fried", "fast food"]):
        factors.add("poor_diet")

    exercise = (answers.get("exercise") or "").lower()
    if any(k in exercise for k in ["rare", "rarely", "never", "seldom", "not"]):
        factors.add("low_exercise")

    age = answers.get("age")
    if isinstance(age, int) and age > 40:
        factors.add("age_over_40")

    confidence = 0.88 if factors else 0.6
    return {"factors": list(factors), "confidence": confidence}


def classify(factors_dict: Dict, answers: Dict[str, Any]) -> Dict:
    """
    Compute risk score and level based on weights
    """
    factors = factors_dict.get("factors", [])
    score = 0
    rationale = []

    for f in factors:
        w = WEIGHTS.get(f, 5)  # default small weight for unknown factors
        score += w
        r = FACTOR_RATIONALE.get(f, f)
        rationale.append(r)

    # Clamp score to 0-100
    score = min(score, 100)

    # Risk level thresholds
    if score >= 60:
        level = "high"
    elif score >= 31:
        level = "medium"
    else:
        level = "low"

    return {"risk_level": level, "score": score, "rationale": rationale}
