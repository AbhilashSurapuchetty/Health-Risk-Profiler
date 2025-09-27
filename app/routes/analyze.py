'''from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi import Body
from app.schemas import SurveyInput, ParseOutput, FinalOutput
from app.services import parser, ocr_service, risk_engine, recommender
from app.utils.helpers import too_many_missing_guardrail

router = APIRouter()

@router.post("/analyze/text", response_model=FinalOutput)
async def analyze_text(survey: SurveyInput = Body(...)):
    # parse JSON input
    parsed = parser.parse_from_json(survey)
    # guardrail
    if too_many_missing_guardrail(parsed["answers"], parsed["missing_fields"]):
        raise HTTPException(status_code=400, detail={
            "status": "incomplete_profile",
            "reason": ">50% fields missing",
            "missing_fields": parsed["missing_fields"]
        })
    # factors + risk
    factors = risk_engine.extract_factors(parsed["answers"])
    risk = risk_engine.classify(factors, parsed["answers"])
    
    recs = recommender.generate_recommendations(
    factors=factors["factors"],
    risk_level=risk["risk_level"]
)
    
    return {
        "risk_level": risk["risk_level"],
        "factors": factors["factors"],
        "recommendations": recs,
        "score": risk["score"],
        "rationale": risk["rationale"],
        "status": "ok"
    }

@router.post("/analyze/image", response_model=FinalOutput)
async def analyze_image(file: UploadFile = File(...)):
    content = await file.read()
    # OCR
    ocr_result = ocr_service.image_to_text(content)
    parsed = parser.parse_from_text(ocr_result["text"])
    if too_many_missing_guardrail(parsed["answers"], parsed["missing_fields"]):
        raise HTTPException(status_code=400, detail={
            "status": "incomplete_profile",
            "reason": ">50% fields missing",
            "missing_fields": parsed["missing_fields"]
        })
    factors = risk_engine.extract_factors(parsed["answers"])
    risk = risk_engine.classify(factors, parsed["answers"])
    
    recs = recommender.generate_recommendations(
    factors=factors["factors"],
    risk_level=risk["risk_level"]
)
    return {
        "risk_level": risk["risk_level"],
        "factors": factors["factors"],
        "recommendations": recs,
        "score": risk["score"],
        "rationale": risk["rationale"],
        "status": "ok"
    }'''

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi import Body
from app.schemas import SurveyInput, FinalOutput
from app.services import parser, ocr_service, risk_engine, recommender
from app.utils.helpers import too_many_missing_guardrail

router = APIRouter()


# --- Text input route ---
@router.post("/analyze/text", response_model=FinalOutput)
async def analyze_text(survey: SurveyInput = Body(...)):
    # Step 1: Parse
    parsed = parser.parse_from_json(survey)

    if too_many_missing_guardrail(parsed["answers"], parsed["missing_fields"]):
        raise HTTPException(status_code=400, detail={
            "status": "incomplete_profile",
            "reason": ">50% fields missing",
            "missing_fields": parsed["missing_fields"]
        })

    # Step 2: Factor Extraction
    factors = risk_engine.extract_factors(parsed["answers"])

    # Step 3: Risk Classification
    risk = risk_engine.classify(factors, parsed["answers"])

    # Step 4: Recommendations
    recs = recommender.generate_recommendations(
        factors=factors["factors"],
        risk_level=risk["risk_level"]
    )

    return {
        "answers": parsed["answers"],
        "missing_fields": parsed["missing_fields"],
        "parse_confidence": parsed.get("confidence", 0),
        "factors": factors["factors"],
        "factor_confidence": factors.get("confidence", 0),
        "risk_level": risk["risk_level"],
        "score": risk["score"],
        "rationale": risk["rationale"],
        "recommendations": recs,
        "status": "ok"
    }


# --- Image input route ---
@router.post("/analyze/image", response_model=FinalOutput)
async def analyze_image(file: UploadFile = File(...)):
    content = await file.read()

    # OCR
    ocr_result = ocr_service.image_to_text(content)
    parsed = parser.parse_from_text(ocr_result["text"])

    if too_many_missing_guardrail(parsed["answers"], parsed["missing_fields"]):
        raise HTTPException(status_code=400, detail={
            "status": "incomplete_profile",
            "reason": ">50% fields missing",
            "missing_fields": parsed["missing_fields"]
        })

    # Step 2: Factor Extraction
    factors = risk_engine.extract_factors(parsed["answers"])

    # Step 3: Risk Classification
    risk = risk_engine.classify(factors, parsed["answers"])

    # Step 4: Recommendations
    recs = recommender.generate_recommendations(
        factors=factors["factors"],
        risk_level=risk["risk_level"]
    )

    return {
        "answers": parsed["answers"],
        "missing_fields": parsed["missing_fields"],
        "parse_confidence": parsed.get("confidence", 0),
        "ocr_confidence": ocr_result.get("confidence", 0),
        "factors": factors["factors"],
        "factor_confidence": factors.get("confidence", 0),
        "risk_level": risk["risk_level"],
        "score": risk["score"],
        "rationale": risk["rationale"],
        "recommendations": recs,
        "status": "ok"
    }
