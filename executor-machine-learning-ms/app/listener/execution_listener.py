from loguru import logger
import pika
import json
from listener.listener_settings import LISTENER_CONFIG, EXECUTOR_KEY


class RabbitMQRpcListener(object):
    """[RabbitMQRpcListener]
    This class is an Remote Procedure Call worker that provide methods to wait for requests and reply to the caller.
    
    Args:
        url ([string]): [rabbitmq's url]
        queue_name ([string]): [queue name]
    """
    def __init__(self, url, queue_name) -> None:
        self.queue_name = queue_name
        params = pika.URLParameters(url)
        connection = pika.BlockingConnection(params)
        self.channel = connection.channel()
        self.channel.queue_declare(queue=queue_name)

    def on_request(self, ch, method, props, message_body):
        """ [on_request]
            This method is capturing the message from rabbitmq and based on the api-name call an "executor" a.
                - The executor is responsible to call the external module placed on services's folder and after his execution the response
                will be publish in the reply_to queue provided by the caller.
        Args:
            ch ([type]): [channel]
            method ([type]): [method]
            props ([type]): [properties]
            message_body ([type]): [message sent through queue]
        """
        logger.info(' [-] Publishing through Remote Rrocedure Call (RPC)...')
        logger.info(' [x] Received %r' % message_body)

        message = json.loads(message_body.decode('utf-8'))
        api_name_to_execute = message['api_name']
        logger.info(f"The API to be executed is {api_name_to_execute}")

        executor_config = LISTENER_CONFIG.get(api_name_to_execute)
        executor = executor_config.get(EXECUTOR_KEY)

        logger.info(f"Calling executor [{executor.__class__.__name__}] for API: {api_name_to_execute}")
        response = executor.execute(message)

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id=props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start(self):
        """[start]
            This method allows the Remote Procedure Call consume the messages sent through rabbitmq.
        """
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.on_request)

        logger.info(" [x] Awaiting RPC requests")
        self.channel.start_consuming()
