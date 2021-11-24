from time import time
from typing import List

from api.router.api_settings import API_CONFIG, FACE_DETECTION_API_KEY, VALIDATOR_KEY, INVOKER_KEY
from fastapi import APIRouter, File
from fastapi.datastructures import UploadFile
from loguru import logger

router = APIRouter()
face_detection_request_config = API_CONFIG.get(FACE_DETECTION_API_KEY)


@router.post("/api/face-detection")
async def detect_faces_api(image_files: List[UploadFile] = File(...)):
    """[process_images]

    This method is exposing the service through process route and it will allow the user send images to be analysed by the 
    Machine Learning service.

    Args:
        image_files (List[UploadFile], optional): [The image(s) is coming from the http's request]. Defaults to File(...).

    Returns:
        [json]: [The response contain the machine learning results for each image sent in the request]
    """
    logger.info("[-] Face Detection API - Starting Processing")
    start_time = time()

    validator = face_detection_request_config.get(VALIDATOR_KEY)
    validator.validate(image_files)

    invoker = face_detection_request_config.get(INVOKER_KEY)

    response = await invoker.invoke(image_files)
    elapsed_time = time() - start_time

    logger.info(f"[X] Face Detection API - Completed processing in {elapsed_time} seconds")
    return response
