import json
from loguru import logger
from executor.executor import BaseExecutor


class FaceDetectionMachineLearningExecutor(BaseExecutor):
    """[FaceDetectionMachineLearningExecutor]

    This class is responsable to invoke the module that are placed in the service folder.
    
    Args:
        face_detection_sdk ([type]): [provide the module that will be executed]
    """

    def __init__(self, face_detection_sdk) -> None:
        self.face_detection_sdk = face_detection_sdk

    def execute(self, message):
        logger.info(' [-] Machine Learning Invoker started... ')

        file_name = str(message["filename"])
        image_as_base64 = message["image_64_encode"][0]

        logger.info(f"Analyzing for item: {file_name}")
        result = [file_name, self.face_detection_sdk.get_face_location(image_as_base64)]

        logger.info(f' Response: {result}')
        logger.info(' [X] Machine Learning Invoker is completed. ')
        return json.dumps(result)
