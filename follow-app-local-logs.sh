#!/usr/bin/env bash

API_SERVICE_NAME="api-machine-learning-ms"
EXECUTOR_SERVICE_NAME="executor-machine-learning-ms"

case "$1" in
	'api') services="$API_SERVICE_NAME" ;;
	'executor') services="$EXECUTOR_SERVICE_NAME" ;;
	*) services="$API_SERVICE_NAME $EXECUTOR_SERVICE_NAME" ;;
esac

docker-compose -f deploy/local/docker-compose.yaml logs -f  $services
