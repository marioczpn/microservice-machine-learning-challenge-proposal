#vars
VERSION=1.0
ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
BUILD_VERSION=latest
DEPLOY_ENV=local
# For this stage of the project, this is defined as a variable that could be updated or overridden
# during make invocation. In the long-term, a proper auto-scaling based on the number of
# unprocessed messages in the queue could be implemented, scaling up and down the number of instances
# according to the load
NUM_INSTANCES_ML_EXECUTOR=6

# Machine Learning Executor config
ML_EXECUTOR_CONTAINER_NAME=ml-executor-ms
ML_EXECUTOR_TAG=marioczpn/${ML_EXECUTOR_CONTAINER_NAME}:${BUILD_VERSION}
ML_EXECUTOR_FOLDER=executor-machine-learning-ms

# Machine Learning API config
ML_API_CONTAINER_NAME=api-machine-learning-ms
ML_API_TAG=marioczpn/${ML_API_CONTAINER_NAME}:${BUILD_VERSION}
ML_API_FOLDER=api-machine-learning-ms
#ML_API_FOLDER=api-producer-ms
ML_API_INTEGRATION_TEST_PATH=${ROOT_DIR}/${ML_API_FOLDER}/tests/integration


IMAGE_RABBITMQ=rabbitmq
DOCKER_COMPOSE_RABBITMQ_PATH=${ROOT_DIR}/rabbitmq/ContainerFile/docker-compose.yaml
DOCKER_COMPOSE_CONSUMER_PATH=${ROOT_DIR}/${ML_EXECUTOR_FOLDER}/ContainerFile/docker-compose.yaml
DOCKER_COMPOSE_PRODUCER_PATH=${ROOT_DIR}/${ML_API_FOLDER}/ContainerFile/docker-compose.yaml

.PHONY: help build push all

help:
	    @echo "Makefile commands:"
	    @echo "make build"
		@echo "make run"
	    @echo "make push"
		@echo "make stop"
	    @echo "all"

.DEFAULT_GOAL := all

# Docker build
build: .build.ml_executor .build.api

.build.ml_executor:
		@echo "Building docker image for Machine Learning Executor ms"
		docker build -t ${ML_EXECUTOR_TAG} -f ${ML_EXECUTOR_FOLDER}/ContainerFile/Dockerfile ${ML_EXECUTOR_FOLDER}

.build.api:
		@echo "Building docker image for Machine Learning API"
		docker build -t ${ML_API_TAG} -f ${ML_API_FOLDER}/ContainerFile/Dockerfile ${ML_API_FOLDER}

# Docker publish
push:
	    @echo "Pushing docker consumer image"
	    docker push ${ML_EXECUTOR_TAG}
		docker push ${ML_API_TAG}

# Docker run
run:
		@echo "Starting Application"
		BUILD_VERSION=${BUILD_VERSION} docker-compose -f deploy/${DEPLOY_ENV}/docker-compose.yaml down --remove-orphans
		BUILD_VERSION=${BUILD_VERSION} docker-compose -f deploy/${DEPLOY_ENV}/docker-compose.yaml up -d --scale executor-machine-learning-ms=${NUM_INSTANCES_ML_EXECUTOR}

stop:
		@echo "Stopping Application"
		BUILD_VERSION=${BUILD_VERSION} docker-compose -f deploy/${DEPLOY_ENV}/docker-compose.yaml down --remove-orphans

test:
		@echo Cleaning old reports ${ML_API_INTEGRATION_TEST_PATH}
		rm -rf ${ML_API_INTEGRATION_TEST_PATH}/integration_test_report/
		
		@echo Generating new integration test report
		python3 -m pytest ${ML_API_INTEGRATION_TEST_PATH} --capture=tee-sys  --html=${ML_API_INTEGRATION_TEST_PATH}/integration_test_report/out_report.html

rm:
		@echo "Purging All Unused or Dangling Images, Containers, Volumes, and Networks"
		docker system prune -a

		@echo "Removing all images"
		docker images -a
		
logs:
		@echo  "Getting logs"
		docker-compose -f deploy/local/docker-compose.yaml logs -f  executor-machine-learning-ms ${ML_API_CONTAINER_NAME}

all: build run