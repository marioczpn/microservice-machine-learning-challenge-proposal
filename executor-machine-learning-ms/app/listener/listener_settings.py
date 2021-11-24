import os

from face_detection.face_detection_executor import FaceDetectionMachineLearningExecutor
from services.mocksdk_service.MockSDKModule import MockSDK

# The purpose of this configuration file is to give more flexibility, allowing to add more modules into the application.

# Configuration keys
EXECUTOR_KEY = 'executor'

# API's keys
FACE_DETECTION_API_KEY = os.environ['FACE_DETECTION_API_NAME']

LISTENER_CONFIG = {
    FACE_DETECTION_API_KEY: {
        EXECUTOR_KEY: FaceDetectionMachineLearningExecutor(MockSDK()),
    }
}
