from loguru import logger
import os

from listener.execution_listener import RabbitMQRpcListener


def main():
    logger.info(" [-] Starting executor-machine-learning-ms")
    rabbitmq_url = os.environ['RABBIT_MQ_URL']
    queue_name = os.environ['EXECUTOR_QUEUE_NAME']

    logger.info(f" [-] Starting listener for queue {queue_name} at {rabbitmq_url}")
    listener = RabbitMQRpcListener(rabbitmq_url, queue_name)
    listener.start()


if __name__ == '__main__':
    main()
