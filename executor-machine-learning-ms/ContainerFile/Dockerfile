FROM  python:3.7-slim-buster

WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV EXECUTOR_QUEUE_NAME=rpc_queue
ENV FACE_DETECTION_API_NAME=face_detection_api 
ENV RABBIT_MQ_URL=amqp://apitest:apitest@rabbitmq/%2f
ENV ML_MODEL_PATH=/usr/src/app/services/mocksdk_service/models/haarcascade_frontalface_default.xml

COPY ../requirements.txt /usr/src/app/requirements.txt

RUN apt-get update && apt-get install -y python3-opencv
RUN pip3 install --no-cache-dir -r /usr/src/app/requirements.txt

COPY ../app /usr/src/app

CMD [ "python3", "-u", "/usr/src/app/main.py" ]