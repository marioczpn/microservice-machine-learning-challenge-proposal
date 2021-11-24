
## Coding Challenge

## Project Description

You will build a scalable and decoupled HTTP API to serve the capabilities of a machine learning model (`MockSDKModule.py`) developed by a research group.

You are free to modify the `MockSDKModule.py` file if your architecture needs it.
> **Note**: The `MockSDKModule.py` is documented with properly formatted comments.

The only required Python package is the `opencv-python` included in the `requirements.txt` file.
> **Note**: You don't need to compile OpenCV from source, just use the `opencv-python` package from PyPI.

The project must comply with all the [technical criteria](#technical-criteria).

Given the [test data](#test-data--expected-results), the HTTP API must output the expected results.

## Technical Criteria

1. The project must be built with a **microservices architecture** and the service responsible for running the machine learning code must be capable of horizontally scale. You don't need to implement the automated scaling and the scaling strategy, but the container and the architecture you propose must expect and be prepared for scaling.
    - We expect that each service will have its own directory with a `Containerfile`/`Dockerfile` that successfully builds an image (either with `docker build` or `podman build`).
    - We expect a `docker-compose.yaml` file or Kubernetes compliant YAML files for deployment. 
    - You don't need to worry with the `Ingress` component, you can assume it will forward the requests (ports 80 or 8080), with TLS/SSL already terminated, to the container running your web server.
> **Hint**: You can implement process-based parallelism (with Python's `multiprocessing` library) for requests that send multiple files for processing.

2. The architecture must include a messaging system (e.g., **RabbitMQ**, queue structures on **Redis** or even **Apache Kafka**) to communicate between the microservices in the same namespace (it's an overkill for this project, but we want to evaluate how the candidate will deal with this requirement).
> **Hint**: Take a look at RabbitMQ's `Message Exchanges`, it can be useful and interesting, but it's not needed. **Use your time wisely**.

3. The HTTP API must have **at least** one route (named `/process`) to receive the request data (image files) to be processed by the machine learning algorithm. You can change the `/process` route name and implement more routes if your architecture needs it.

4. You will define the request structure, just keep in mind that the user needs to upload one or multiple image files in the same request to satisfy test scenarios.
> **Note**: You don't need to worry about `timeout`, set it to any number you want. If you have knowhow and want to deal with the `timeout` issue to show off your skills, then you can take a look at `HTTP Long Polling` or implement an **asynchronous HTTP API architecture** with routes for checking status, retrieving results, etc.

> **Hint**: Using **Redis** is an easy way and it's a good tool for implementing an **asynchronous HTTP API architecture**, but keep in mind that **Redis** is an in-memory data structure store, it can persist data on disk, but it has some caveats. You can still use **RabbitMQ**, custom code or anything else to implement it.

5. The HTTP API must have a user documentation. You are free to decide how to implement, format and distribute the user documentation (custom web site, Markdown files, GitHub pages, [swagger.io](swagger.io), [openapis.org](openapis.org), etc.)

6. We encourage you to use **Python** with [**FastAPI**](https://fastapi.tiangolo.com/) + [**Uvicorn**](https://www.uvicorn.org/)/[**Hypercorn**](https://gitlab.com/pgjones/hypercorn) or with [**Flask**](https://flask.palletsprojects.com/en/2.0.x/) + [**Gunicorn**](https://gunicorn.org/) as your web server framework, but, since the solution is decoupled, you can use **Node.js** with [**Express**](https://expressjs.com/) or [**Koa**](https://koajs.com/), perhaps **Go** with [**Fiber**](https://gofiber.io/), or even **Elixir**, it's all up to your preferences.
> **Note**: The microservice application responsible for running the machine learning code (imported from `MockSDKModule.py` and instantiated) must be written in **Python**.

7. The use of clean code and design patterns, such as SOLID, is recommended.

8. The project must be uploaded to GitHub so that reviewers can access the project.

9. The project must include:
    - A `README.md` file with instructions you see fit.
    - Simple architecture drawing.
    - UML type diagram illustrating your pipeline.
    > **Hint**: You can use [draw.io](draw.io) for the drawings and diagrams.

## Test Data & Expected Results

The purpose of the test data is to guarantee that the `MockSDKModule.py` is working correctly.

The test data (located under the `test-data` directory) is composed by 5 JPG images from the [Labeled Faces in the Wild](http://vis-www.cs.umass.edu/lfw/) dataset.

The expected results for each image on the test data:

`Aaron_Eckhart_0001.jpg`
```
[[67, 66, 118, 118]]
```

`Ahmed_Lopez_0001.jpg`
```
[[65, 65, 122, 122]]
```

`Alan_Mulally_0001.jpg`
```
[[63, 63, 123, 123]]
```

`Alex_Corretja_0001.jpg`
```
[[71, 67, 114, 114]]
```

`Anne_Donovan_0001.jpg`
```
[[64, 68, 118, 118]]
```
