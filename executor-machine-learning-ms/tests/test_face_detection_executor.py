import base64
import os
from app.face_detection.face_detection_executor import FaceDetectionMachineLearningExecutor
from app.services.mocksdk_service.MockSDKModule import MockSDK
from unittest.mock import patch
import pytest
from app.listener.listener_settings import LISTENER_CONFIG, EXECUTOR_KEY
import json

@pytest.fixture
def image_64_encode():
        main_script_dir = os.path.dirname(__file__)
        rel_path = "fixtures/images/Aaron_Eckhart_0001.jpg"
        image_file = os.path.join(main_script_dir, rel_path)
        image = open(image_file, "rb")
        image_read = image.read()
        return base64.b64encode(image_read).decode('utf-8')

@patch('app.services.mocksdk_service.MockSDKModule')        
def test_call_face_location(MockClass1, image_64_encode):  
        message_from_queue = {
            "filename": "Aaron_Eckhart_0001.jpg",
            "image_64_encode": image_64_encode,
            "api_name": "FACE_DETECTION_API_NAME"
        }       
        
        MockClass1.get_face_location.return_value = [67, 66, 118, 118]
        executor = FaceDetectionMachineLearningExecutor(MockClass1)
        response = executor.execute(message_from_queue)
        
        assert response is not None
        
def test_executor_form_listener_settings(mocker, image_64_encode):  
        message_from_queue = {
            "filename": "Aaron_Eckhart_0001.jpg",
            "image_64_encode": [image_64_encode],
            "api_name": "FACE_DETECTION_API_NAME"
        }              

        executor_config = LISTENER_CONFIG.get(message_from_queue["api_name"])
        executor = executor_config.get(EXECUTOR_KEY)

   
        response = executor.execute(message_from_queue)
        print(response)

