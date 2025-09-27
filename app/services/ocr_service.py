from typing import Dict
from PIL import Image
import io
import pytesseract
import numpy as np
import cv2

# If Tesseract binary is not on PATH, set:
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # adjust to your system

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def _pil_from_bytes(b: bytes) -> Image.Image:
    return Image.open(io.BytesIO(b)).convert("RGB")

def image_to_text(file_bytes: bytes) -> Dict:
    """
    Returns {"text": "...", "confidence": 0.85}
    confidence computed as average of tesseract word confidences (0-100 -> 0.0-1.0)
    """
    img = _pil_from_bytes(file_bytes)
    # basic preproc: convert to grayscale + threshold (helps noisy scans)
    np_img = np.array(img)
    gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    pil_proc = Image.fromarray(thresh)

    raw_text = pytesseract.image_to_string(pil_proc)
    # compute confidences
    data = pytesseract.image_to_data(pil_proc, output_type=pytesseract.Output.DICT)
    confs = []
    for c in data.get("conf", []):
        try:
            v = float(c)
            if v >= 0:
                confs.append(v)
        except:
            pass
    conf = (sum(confs) / len(confs) / 100.0) if confs else 0.6
    return {"text": raw_text, "confidence": round(conf, 2)}
