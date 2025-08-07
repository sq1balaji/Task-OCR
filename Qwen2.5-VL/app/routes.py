# from fastapi import APIRouter, UploadFile, File
# from app.ocr_services import perform_ocr
# from PIL import Image
# import io

# router = APIRouter()

# @router.post("/ocr")
# async def ocr_endpoint(file: UploadFile = File(...)):
#     image_data = await file.read()
#     image = Image.open(io.BytesIO(image_data))
#     result = perform_ocr(image)
#     return {"ocr_text": result}


import io
from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import UnidentifiedImageError
from app.ocr_services import perform_ocr
from app.pdf_utils import pdf_to_images
import logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/ocr-pdf")
async def ocr_pdf(file: UploadFile = File(...)):
    logger.info("Begin")
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    logger.info("Into OCR route....")
    pdf_bytes = await file.read()
    
    try:
        logger.info("Converting the pdf into images...")
        images = pdf_to_images(pdf_bytes)
        logger.info("Converted into images.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF to image conversion failed: {e}")

    results = []
    for idx, image in enumerate(images, start=1):
        try:
            logger.info("Performing OCR....")
            text = perform_ocr(image)
            results.append({"page": idx, "text": text})
        except Exception as e:
            results.append({"page": idx, "text": f"Error: {e}"})
        print("\nResult :\n", results)
    return {"ocr_result": results}

