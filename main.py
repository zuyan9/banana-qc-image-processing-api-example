from fastapi import FastAPI, File, UploadFile, Response
from fastapi.responses import RedirectResponse
from io import BytesIO
from PIL import Image, ImageFilter, UnidentifiedImageError

class ImageProcessingError(Exception):
    """Base class for other exceptions in image processing"""
    pass


class ColorCheckerNotFoundError(ImageProcessingError):
    """Raised when no MacBeth ColorChecker is found"""
    pass


class BananaObjectNotFoundError(ImageProcessingError):
    """Raised when no banana object is found"""
    pass

description = """
Example API for banana image processing 🍌📸🔪

## Color Correction
Correct colors in the image with the help of a [MacBeth ColorChecker](https://en.wikipedia.org/wiki/ColorChecker)

Return the color-corrected image with average delta E measures in the header

## Banana Extraction
Extract the banana object part of the image

Return the banana-injected image with number of bananas in the header

## Combined Processing
Perform both color correction and banana extraction on the image

Return the processed image with other metadata in the header
"""

tags_metadata = [
    {
        "name": "Image Processing",
    },
    {
        "name": "Misc",
    },
]

app = FastAPI(
    title = "Banana QC Image Processing API Example",
    description = description,
    version = "0.0.1",
    contact = {
        "name": "Zuyang @ Strella",
        "url": "https://www.strellabiotech.com",
    },
    redoc_url = None,
    openapi_tags = tags_metadata,
)

@app.get("/", tags=["Misc"])
async def redirect_to_docs_page():
    response = RedirectResponse(url='/docs')
    return response

@app.post("/color_correction", tags=["Image Processing"])
def image_color_correction(img: UploadFile = File(...)):
    """
    Perform color correction on the image using ColorChecker
    """
    try:
        img_orig = Image.open(img.file)

        # a simple image color transform
        color_filter = ImageFilter.Color3DLUT.generate(5, lambda r, g, b: (0.7 * r, 0.7 * g, 1.2 * b))
        img_orig = img_orig.filter(color_filter)
        img_processed = BytesIO()
        img_orig.save(img_processed, "PNG")
        img_processed.seek(0)

        # construct response header
        delta_e_orig = 9.2
        delta_e_corrected = 5.3
        color_correction_version = "0.0.1"
        message = {}
        message["delta_e_orig"] = f"{delta_e_orig}"
        message["delta_e_corrected"] = f"{delta_e_corrected}"
        message["color_correction_version"] = color_correction_version

        return Response(content = img_processed.getvalue(), headers = message, media_type="image/png")
    
    except UnidentifiedImageError:
        message = {"error": "Not valid image file"}
        return Response(headers = message)
    
    except ColorCheckerNotFoundError as E:
        message = {"error": "No ColorChecker found"}
        return Response(headers = message)

    except Exception as E:
        message = {"error": f"{E}"}
        return Response(headers = message)


@app.post("/banana_extraction", tags=["Image Processing"])
def banana_extraction(img: UploadFile = File(...)):
    """
    Extract banana object from the image
    """
    try:
        img_orig = Image.open(img.file)

        # a simple image crop
        width, height = img_orig.size
        left = int(width * 0.25)
        top = int(height * 0.25)
        right = int(width * 0.75)
        bottom = int(height * 0.75)
        area = (left, top, right, bottom)
        img_orig = img_orig.crop(area)
        img_processed = BytesIO()
        img_orig.save(img_processed, "PNG")
        img_processed.seek(0)

        # construct response header
        banana_extraction_version = "0.0.1"
        message = {}
        message["number_of_bananas"] = f"2"
        message["banana_extraction_version"] = banana_extraction_version

        return Response(content = img_processed.getvalue(), headers = message, media_type="image/png")
    
    except UnidentifiedImageError:
        message = {"error": "Not valid image file"}
        return Response(headers = message)
    
    except BananaObjectNotFoundError as E:
        message = {"error": "No banana found"}
        return Response(headers = message)

    except Exception as E:
        message = {"error": f"{E}"}
        return Response(headers = message)


@app.post("/combined_processing", tags=["Image Processing"])
def combined_processing(img: UploadFile = File(...)):
    """
    Perform color correction and extract banana object
    """
    try:
        img_orig = Image.open(img.file)

        # a simple image color transform
        color_filter = ImageFilter.Color3DLUT.generate(5, lambda r, g, b: (0.7 * r, 0.7 * g, 1.2 * b))
        img_orig = img_orig.filter(color_filter)

        # a simple image crop
        width, height = img_orig.size
        left = int(width * 0.25)
        top = int(height * 0.25)
        right = int(width * 0.75)
        bottom = int(height * 0.75)
        area = (left, top, right, bottom)
        img_orig = img_orig.crop(area)
        img_processed = BytesIO()
        img_orig.save(img_processed, "PNG")
        img_processed.seek(0)

        # construct response header
        delta_e_orig = 9.2
        delta_e_corrected = 5.3
        color_correction_version = "0.0.1"
        message = {}
        message["delta_e_orig"] = f"{delta_e_orig}"
        message["delta_e_corrected"] = f"{delta_e_corrected}"
        message["color_correction_version"] = color_correction_version

        # construct response header
        banana_extraction_version = "0.0.1"
        message["number_of_bananas"] = f"2"
        message["banana_extraction_version"] = banana_extraction_version

        return Response(content = img_processed.getvalue(), headers = message, media_type="image/png")
    
    except UnidentifiedImageError:
        message = {"error": "Not valid image file"}
        return Response(headers = message)

    except ColorCheckerNotFoundError as E:
        message = {"error": "No ColorChecker found"}
        return Response(headers = message)

    except BananaObjectNotFoundError as E:
        message = {"error": "No banana found"}
        return Response(headers = message)

    except Exception as E:
        message = {"error": f"{E}"}
        return Response(headers = message)