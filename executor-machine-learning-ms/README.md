# EXECUTOR-MACHINE-LEARNING-MS

## Overview

This microservice is a backend listener application which function is to receive the message sent by [api-machine-learning-ms](../api-machine-learning-ms/README.md) and it will process the message invoking the machine-learning module [MockSDK](app/services/mocksdk_service/README.md) and finally publish a message to reply queue in the RabbitMQ.

## Table of Contents
- [EXECUTOR-MACHINE-LEARNING-MS](#executor-machine-learning-ms)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [How the backend  works](#how-the-backend--works)
  - [Technologies](#technologies)
  - [How to start the application](#how-to-start-the-application)
  - [Next Steps](#next-steps)

## How the backend  works

The backend is a listener which capture the message from RabbitMQ and delegate it to the executor, which wil take a action to invoke the machine-learning module.

The ***design*** of the executor (backend) is similar to the [api-machine-learning-ms](../api-machine-learning-ms/README.md) making it generic and extensible to additional apis.

When processing the executor the tasks become messages and the listener class will check the `api_name` defined in the message and based on that, it will trigger the corresponding executor.

The listener will use the `listener_setting.py` to verify what is the corresponding executor for the given api.

```python
# Configuration keys
EXECUTOR_KEY = 'executor'

# API's keys
FACE_DETECTION_API_KEY = os.environ['FACE_DETECTION_API_NAME']

LISTENER_CONFIG = {
    FACE_DETECTION_API_KEY: {
        EXECUTOR_KEY: FaceDetectionMachineLearningExecutor(MockSDK()),
    }
}
```

>Note: As you can see it is extensible, flexible because allows us to change the executor and also the SDK module used, basically change everything.


## Technologies

-  [Python3](https://www.python.org/downloads/)
   - [loguru](https://github.com/Delgan/loguru) - to handling logs
   - [pika](https://github.com/pika/pika) - implementation of the AMQP protocol including RabbitMQ
   - [pytest](https://docs.pytest.org/en/6.2.x/) - unit/integration tests
   - [opencv_python](https://docs.opencv.org/master/d6/d00/tutorial_py_root.html)
   - [numpy](https://numpy.org)
-  [Docker](https://www.docker.com)

## How to start the application

The application has two ways to run directly or through docker

- First Method: 
  - Docker: 
    - Build you can run the [Dockerfile](ContainerFile/Dockerfile)
  
  ```shell 
  docker build -t marioczpn/executor-machine-learning-ms:latest -f executor-machine-learning-ms/ContainerFile/Dockerfile executor-machine-learning-ms
  ``` 

    - Run:
  
   ``` 
   docker run -d -p 80:80 marioczpn/executor-machine-learning-ms:latest
   ```

   
  - Second Method

Before to start you will need to setup the environment variables:

```shellscript
export EXECUTOR_QUEUE_NAME=rpc_queue
export FACE_DETECTION_API_NAME=face_detection_api 
export RABBIT_MQ_URL=amqp://apitest:apitest@localhost/%2f
export ML_MODEL_PATH=./app/services/mocksdk_service/models/haarcascade_frontalface_default.xml
```

To run:
```shellscript
python3 /executor-machine-learning-ms/app/main.py

```
    
## Next Steps

- Handling exceptions in general (e.g validation ones)
- Increase the code coverage through the unit-tests (Mocking components)

