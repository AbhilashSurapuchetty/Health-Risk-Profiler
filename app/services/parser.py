# parser.py
from typing import Dict, Any, List

# Mapping keywords in text to health factors
HEALTH_KEYWORDS = {
    "smoke": "smoking",
    "cigarette": "smoking",
    "alcohol": "alcohol_use",
    "sugar": "poor_diet",
    "high sugar": "poor_diet",
    "fast food": "poor_diet",
    "exercise": "low_exercise",
    "inactive": "low_exercise",
    "stress": "high_stress",
    "hypertension": "high_blood_pressure",
    "bp": "high_blood_pressure",
    "diabetes": "diabetes",
    "cholesterol": "high_cholesterol",
    "obese": "obesity",
    "weight": "obesity",
    "sleep": "poor_sleep",
    "age": "age_over_40",  # age-based factor handled separately
}

FIELD_KEYS = ["age", "smoker", "exercise", "diet"]

def _clean_bool(v: Any):
    if isinstance(v, bool):
        return v
    if v is None:
        return None
    s = str(v).strip().lower()
    if s in ("yes", "y", "true", "1"):
        return True
    if s in ("no", "n", "false", "0"):
        return False
    return None

def parse_from_json(survey) -> Dict:
    raw = survey.dict()
    answers = {}
    missing = []

    for k in FIELD_KEYS:
        val = raw.get(k)
        if k == "smoker":
            val = _clean_bool(val)
        answers[k] = val
        if val is None or (isinstance(val, str) and val.strip() == ""):
            missing.append(k)

    # Also detect health factors in diet/exercise/smoker fields
    text_to_scan = " ".join([str(raw.get(k, "")) for k in FIELD_KEYS if raw.get(k)])
    factors_detected = _detect_health_keywords(text_to_scan)

    confidence = 0.95 if not missing else 0.7
    return {
        "answers": answers,
        "missing_fields": missing,
        "confidence": confidence,
        "detected_factors": factors_detected
    }

def parse_from_text(text: str) -> Dict:
    text_lower = text.lower()
    answers = {"age": None, "smoker": None, "exercise": None, "diet": None}

    # Simple extraction for age if mentioned
    import re
    m = re.search(r"age[:\s]*([0-9]{1,3})", text_lower)
    if m:
        answers["age"] = int(m.group(1))

    # Smoker detection
    if "smoke" in text_lower or "cigarette" in text_lower:
        answers["smoker"] = True
    elif "non-smoker" in text_lower or "no smoke" in text_lower:
        answers["smoker"] = False

    # Exercise / Diet extraction (just capture text after keywords)
    m = re.search(r"exercise[:\s]*([a-z ]{2,30})", text_lower)
    if m:
        answers["exercise"] = m.group(1).strip()
    m = re.search(r"diet[:\s]*([a-z0-9 \-]+)", text_lower)
    if m:
        answers["diet"] = m.group(1).strip()

    missing = [k for k, v in answers.items() if v is None or (isinstance(v, str) and v.strip() == "")]

    detected_factors = _detect_health_keywords(text_lower)

    confidence = 0.85 if not missing else 0.6
    return {
        "answers": answers,
        "missing_fields": missing,
        "confidence": confidence,
        "detected_factors": detected_factors
    }

def _detect_health_keywords(text: str) -> List[str]:
    factors = set()
    for keyword, factor in HEALTH_KEYWORDS.items():
        if keyword in text:
            factors.add(factor)
    return list(factors)
