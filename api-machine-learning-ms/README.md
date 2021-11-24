# API-MACHINE-LEARNING-MICROSERVICE

## Overview

This microservice is responsible for exposing APIs as an edge for the whole solution. 
By the proposed challenge, the APIs are used as a way for clients to invoke machine learning functionalities. 
The edge was designed to allow the addition of APIs - and for the current state, the only 
exposed API is **face-location** (defined here as face-detection), 
however new APIs may be added to the edge.

All the APIs are defined in the router package, and the edge architecture does not assume how the 
integration with the backend service implementing the machine learning process will be done. 

In the case of face-recognition API, I am using an async integration leveraging RabbitMQ, with
the Invoker implementation sending messages representing the request and waiting for the response
from the Executor microservice.

The solution is flexible, scalable and decoupled HTTP API developed using multiprocessing to improve the performance and serve the machine learning capabilities. The feature-based **face verification/detection** uses  Labeled Face in the Wild dataset.


## Table of Contents
- [API-MACHINE-LEARNING-MICROSERVICE](#api-machine-learning-microservice)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [How the application works](#how-the-application-works)
    - [Face Location API Usage](#face-location-api-usage)
    - [Flow](#flow)
    - [Programming Language](#programming-language)
    - [Parallelism](#parallelism)
    - [Messaging System](#messaging-system)
  - [Technologies](#technologies)
  - [How to start the application](#how-to-start-the-application)
  - [Integration Test](#integration-test)
  - [Next Steps](#next-steps)



## How the application works

- router package contains all APIs exposed. For example, the module `face_detection_api.py` is responsible for all endpoints related to Face location
- `api_settings.py` defines all dependencies used by all APIs, achieving the inversion of control. In this, there is no direct coupling of the API with the implementation classes.
- For each API, two main components need to be defined: the request validator (that may have one or more validators) and the invoker. 


![Overview Diagram](docs/images/overview.png)

As said previously, the `api_settings.py` plays a crucial part in the application, as it will be the responsible for 
defining which implementations for the `Invoker` and `RequestValidator` will be used. This module defines a map (`API_CONFIG`) that has the following
structure:

```
# Configuration keys
VALIDATOR_KEY = 'validator'
INVOKER_KEY = 'invoker'

API_CONFIG = {
    <<api-name>>: {
        VALIDATOR_KEY: RequestValidator([<<list-of-implementations-of-baseValidator>>]),
        INVOKER_KEY: <<implementation-of-base-invoker>>
    }
}
```

### Face Location API Usage

The Face Location API uses the RabbitMQ for integrating with the Executor microservice that is
responsible for calling the Machine Learning SDK. 

Below you can see a diagram representing the design of the Face Detection API:

![Face Detection API](docs/images/face_detection_api.png).

The `api_settings.py` for this API looks like the following:

```python
from api.common.validation import RequestValidator

from api.face_detection.face_detection_invoker import FaceDetectionNumberFilesValidation

from api.face_detection.face_detection_rabbitmq import RabbitMQFaceDetectionInvoker

# Configuration keys
VALIDATOR_KEY = 'validator'
INVOKER_KEY = 'invoker'

# API's keys
FACE_DETECTION_API_KEY = 'face-detection'

API_CONFIG = {
    FACE_DETECTION_API_KEY: {
        VALIDATOR_KEY: RequestValidator([FaceDetectionNumberFilesValidation()]),
        INVOKER_KEY: RabbitMQFaceDetectionInvoker()
    }
}
```

This is a flexible solution, as we could add new Validators just by extending/changing the declaration of `RequestValidator` instantiation
as well as we could change completely the solution by just exchanging the instantiated invoker by any other one, without
modifying anything in `face_detection_api.py`.

### Flow

The application sends the request data (image files) to be processed on the route `/api/face-detection` (the code is available on [face_detection_api.py](app/api/router/face_detection_api.py)).
Based on the map defined in `api_settings.py`, the validation and invoking stages will be executed. 
As it is implemented, the invoker used will send a message to RabbitMQ to be processed by Executor microservice.

The message contract is presented below:

```json
{
  "filename": "<<file_name>>",
  "image_64_encode": "<<image_encoded_as_base64",
  "api_name": "face_detection_api"
}
```

As it may be seen, the field `api_name` makes the whole solution extensible, as the executor microservice 
uses it to identify which API needs to be executed. Currently, there is only `face-detection`, but
we could add more APIs and different implementations for them.

### Programming Language

As the face-detection module was written in python, the decision was to make the whole structure in the same language and apply the [Object-oriented programming (OOP)](https://en.wikipedia.org/wiki/Object-oriented_programming).

> **Disclaimer**: I don't work with python in my daily basis, but I've decided to challenge myself on this implementation and expand my knowledge.

### Parallelism

As the user will send multiple files to be processed, the api  exposed is using **async** to enable the processing many request in paralell. In addition to that, I'm using multiprocessing when sending the message (e.g Python's __multiprocessing__).
You can check hte implementation looking on [face_detection_api.py](app/api/face_detection/face_detection_rabbitmq.py) 

### Messaging System

The application is using AMQP broker, [RabbitMQ](https://www.rabbitmq.com) and it is utilizing a remote procedure call (RPC) for communication between the microservices. 

## Technologies

-  [Python3](https://www.python.org/downloads/)
   - [loguru](https://github.com/Delgan/loguru) - to handling logs
   - [pika](https://github.com/pika/pika) - implementation of the AMQP protocol including RabbitMQ
   - [pytest](https://docs.pytest.org/en/6.2.x/) - unit/integration tests

-  [FastAPI](https://fastapi.tiangolo.com) + [Uvicorn](https://www.uvicorn.org)
-  [Docker](https://www.docker.com)


## How to start the application

The application has two ways to run you can use docker or uvicorn, sharing the both methods below.

> **Hint**: If you wan to run by yourself please setup a RabbitMQ and the Environment variables. Otherwise you can check the [make all](../README.md) to run the whole infrastructure information.

- First Method: 
  - Docker: 
    - Build you can run the [Dockerfile](ContainerFile/Dockerfile)
  
  ``` 
  docker build -t marioczpn/api-machine-learning-ms:latest -f api-machine-learning-ms/ContainerFile/Dockerfile api-machine-learning-ms
  ``` 

  Output:

  ![alt text](docs/images/docker_build_output.png)

  If you are using the docker desktop you will see the image created as the picture bellow:

  ![alt text](docs/images/docker_desktop_output.png)


    - Run:
  
   ``` 
   docker run -d -p 80:80 marioczpn/api-machine-learning-ms:latest
   ```

    Output:
    
    ![alt text](docs/images/docker_run_output.png)

    If you are using the docker desktop you will see the image created as the picture bellow:

    ![alt text](docs/images/docker_run_desktop_output.png)


- Second Method: 

  - First Step: you need to setup the environment variables:

```shellscript
 export EXECUTOR_QUEUE_NAME=rpc_queue 
 export FACE_DETECTION_API_NAME=face_detection_api
 export RABBIT_MQ_URL=amqp://apitest:apitest@localhost/%2f
 ```

- Second Step: run with the command into the folder /api-machine-learning-ms/app
  
     ``` uvicorn main:app --reload ```

Output:
    
![alt text](docs/images/uvicorn_output_command_line.png)


Now the application is ready to receive REST calls.

## Integration Test

You can run the integration test executing the command below:

```python
python3 -m pytest /api-machine-learning-ms/tests --capture=tee-sys  --html=$/api-machine-learning-ms/tests/integration_test_report/out_report.html
```


## Next Steps

- Handling exceptions in general (e.g validation ones)
- Increase the code coverage through the unit-tests (Mocking components)



















  


    
