FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

# set environment variables
ENV EXECUTOR_QUEUE_NAME=rpc_queue
ENV FACE_DETECTION_API_NAME=face_detection_api
ENV RABBIT_MQ_URL=amqp://apitest:apitest@rabbitmq/%2f

COPY ../app/requirements.txt /tmp/requirements.txt

RUN pip3 install --no-cache-dir -r /tmp/requirements.txt
RUN pip3 install python-multipart

COPY ../app /app