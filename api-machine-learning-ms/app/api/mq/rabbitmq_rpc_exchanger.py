import uuid

import pika
from loguru import logger


class RpcRequest:
    """[RpcRequest]
    This class represents the request that will be sent to rabbitmq.
    """

    def __init__(self, queue_name, message):
        self.queue_name = queue_name
        self.message = message


class RabbitMQRpcClient(object):
    """[RabbitMQRpcClient]
    This class is using the RabbitMQ to build an Remote Procedure Call and it is exposing a method which sends an RPC request and blocks until the answer is received.
   
    Args:
        url ([type]): [constructor is receiving the url address]
    """

    def __init__(self, url):
        self.response = None
        self.corr_id = None

        params = pika.URLParameters(url)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()
        self.callback_queue = self.channel.queue_declare(queue='', exclusive=True).method.queue

        self.channel.basic_consume(queue=self.callback_queue, on_message_callback=self.on_response,
                                   auto_ack=True)

    def on_response(self, channel, method, properties, body):
        logger.info(f' [-] Response: {body}')
        if self.corr_id == properties.correlation_id:
            logger.info(f' [-] Getting response for the correlation_id: {self.corr_id}')
            self.response = body

    def send_message(self, rpc_request: RpcRequest):
        """[send_message]
        The mehtod sends a request message and wait the Rabbitmq RPC server replies a reponse message back.
        In order to receive a response the client needs to send a callback queue address with the request.
        Args:
            rpc_request (RpcRequest): [description]

        Returns:
            [type]: [description]
        """
        logger.info(' [-] Sending message to RPC request....')
        self.response = None
        self.corr_id = str(uuid.uuid4())

        # Defining the call back queue address and correlate_id to tie the response with request
        properties = pika.BasicProperties(reply_to=self.callback_queue, correlation_id=self.corr_id)

        logger.info(f' -> Sending Request for api')
        # Sending a message to Rabbitmq 
        self.channel.basic_publish(exchange='', routing_key=rpc_request.queue_name,
                                   properties=properties,
                                   body=rpc_request.message)
        logger.info(' [X] Message was sent')
        while self.response is None:
            self.connection.process_data_events()
        return self.response
