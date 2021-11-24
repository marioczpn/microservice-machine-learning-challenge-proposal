import json
import os
from multiprocessing import Pool

from api.face_detection.face_detection_invoker import FaceDetectionInvoker
from api.mq.rabbitmq_rpc_exchanger import RpcRequest, RabbitMQRpcClient
from api.util.ImageUtil import ImageUtil
from loguru import logger

EXECUTOR_QUEUE_NAME = os.environ['EXECUTOR_QUEUE_NAME']
FACE_DETECTION_API_NAME = os.environ['FACE_DETECTION_API_NAME']
RABBITMQ_URL = os.environ['RABBIT_MQ_URL']


class RabbitMQFaceDetectionInvoker(FaceDetectionInvoker):
    def __init__(self) -> None:
        super().__init__()

    """[RabbitMQFaceDetectionInvoker]
    
    This class is responsable to  creates multiple Python processes in the background and spreads out your computations 
    for you across multiple CPU cores and also call RabbitMQ class to send the message.
    
    Args:
        FaceDetectionInvoker ([AbastractBaseCalss]): [It allows to implement/override the abstract method.]
    """

    async def invoke(self, image_files):
        """[invoke_face_detection]
        The method send the message to rabbitmq and creates multiply processes creating data paralellism.
        
        Args:
            image_files ([file]): [image that will be sent to rabbitmq]

        Returns:
            [json]: [it returns the image's analysis data to caller]
        """
        logger.info("Invoking the face detection")
        number_of_files = len(image_files)
        with Pool(processes=number_of_files) as pool:
            logger.info(f"[-] Starting pool of {number_of_files} processes")

            pool_call = pool.map_async(self.send_message_to_mq, image_files)

            pool.close()
            pool.join()

            result = pool_call.get()
            logger.info(f"[x] Completed processing for face-recognition. Result {result}")
            return result

    def send_message_to_mq(self, image_file):
        """[send_message_to_mq]
        The method is getting the file received and it's prepare the request converting the image's file to base64 that will be sent to rabbitmq.
        
        Args:
            file ([Image]): [The image that will be sent to rabbitmq]

        Returns:
            [json]: [it returns the image's analysis data to caller]
        """
        logger.info(f"[-] Sending message to mq...")

        # Converting image to base64
        imgUtil = ImageUtil()
        image_as_base64 = imgUtil.prepare_img_msg(image_file)

        # Preparing Rabbitmq request
        data = {
            "filename": image_file.filename,
            "image_64_encode": image_as_base64,
            "api_name": FACE_DETECTION_API_NAME
        }
        request = RpcRequest(EXECUTOR_QUEUE_NAME, json.dumps(data))

        # Sending request to rabbitmq
        client = RabbitMQRpcClient(RABBITMQ_URL)
        logger.info(f"[X] Request was sent to rabbitmq.")
        return client.send_message(request)
