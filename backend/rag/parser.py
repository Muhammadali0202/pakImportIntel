import fitz  # PyMuPDF
import logging

logger = logging.getLogger(__name__)

def parse_pdf(file_path: str) -> str:
    """Extract text from a PDF file using PyMuPDF with an EasyOCR fallback."""
    text = ""
    try:
        doc = fitz.open(file_path)
        for page in doc:
            page_text = page.get_text()
            if page_text:
                text += page_text + "\n"
        
        # If no text was extracted, it might be a scanned PDF. Trigger OCR.
        if not text.strip():
            logger.info(f"PyMuPDF extracted no text for {file_path}, falling back to EasyOCR.")
            text = _fallback_ocr(file_path)
            
    except Exception as e:
        logger.error(f"Error parsing PDF with PyMuPDF: {e}")
        text = _fallback_ocr(file_path)
        
    return text.strip()

def _fallback_ocr(file_path: str) -> str:
    """Fallback OCR method for scanned PDFs. Gracefully skips if easyocr is not installed."""
    try:
        import easyocr  # Lazy import — only load if actually needed
    except ImportError:
        logger.warning("easyocr not installed. Skipping OCR fallback. Install it for scanned PDF support.")
        return ""

    try:
        reader = easyocr.Reader(['en'])
        text = ""
        doc = fitz.open(file_path)
        for page in doc:
            pix = page.get_pixmap()
            img_bytes = pix.tobytes("png")
            result = reader.readtext(img_bytes, detail=0)
            text += " ".join(result) + "\n"
        return text
    except Exception as e:
        logger.error(f"EasyOCR fallback failed: {e}")
        return ""
