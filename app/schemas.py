from typing import Optional, List, Dict, Any
from pydantic import BaseModel

# Input when client sends JSON:
class SurveyInput(BaseModel):
    age: Optional[int] = None
    smoker: Optional[Any] = None      # accept True/False or "yes"/"no"
    exercise: Optional[str] = None
    diet: Optional[str] = None

# OCR / parse output
class ParseOutput(BaseModel):
    answers: Dict[str, Any]
    missing_fields: List[str]
    confidence: float

# Factors
class FactorOutput(BaseModel):
    factors: List[str]
    confidence: float

# Risk classification
class RiskOutput(BaseModel):
    risk_level: str
    score: int
    rationale: List[str]

# Final combined
class FinalOutput(BaseModel):
    answers: Dict[str, Any]
    missing_fields: List[str]
    parse_confidence: float
    ocr_confidence: Optional[float] = None
    factors: List[str]
    factor_confidence: float
    risk_level: str
    score: int
    rationale: List[str]
    recommendations: List[str]
    status: str

