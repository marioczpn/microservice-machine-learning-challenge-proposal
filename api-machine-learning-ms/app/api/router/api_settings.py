from api.common.validation import RequestValidator

from api.face_detection.face_detection_invoker import FaceDetectionNumberFilesValidation

from api.face_detection.face_detection_rabbitmq import RabbitMQFaceDetectionInvoker

# Configuration keys
VALIDATOR_KEY = 'validator'
INVOKER_KEY = 'invoker'

# API's keys
FACE_DETECTION_API_KEY = 'face-detection'

"""
The responsibility of this module is to define the dependencies for the API are configured, 
achieving the inversion of control. 

For example, in the case of validators, it is very simple replace and/or extend the validators 
for an API, making it transparent for the component responsible for exposing the API.

The same logic applies to all other configurations.
"""

API_CONFIG = {
    FACE_DETECTION_API_KEY: {
        VALIDATOR_KEY: RequestValidator([FaceDetectionNumberFilesValidation()]),
        INVOKER_KEY: RabbitMQFaceDetectionInvoker()
    }
}
