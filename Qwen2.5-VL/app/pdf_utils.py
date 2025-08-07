from pdf2image import convert_from_bytes

def pdf_to_images(pdf_bytes):
    images = convert_from_bytes(pdf_bytes)
    return images  # List of PIL.Image
