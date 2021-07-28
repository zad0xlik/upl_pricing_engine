#!/bin/bash

project_name='pricing-api'
environment='loc'
redis_url='redis://localhost:6379'

PROJECT_NAME=${project_name}
ENV_BUILD=${environment}
TAG_NAME=${project_name}-${environment}
REDIS_URL=${redis_url}

docker build -t ${TAG_NAME} -f Dockerfile \
  --build-arg PROJECT_NAME=${PROJECT_NAME} \
  --build-arg ENV_BUILD=${ENV_BUILD} \
  --build-arg REDIS_URL=${REDIS_URL} \
  --build-arg PYTHON_VERSION_TAG=3.8.6 \
  --build-arg LINK_PYTHON_TO_PYTHON3=1 .

docker run -p 8888:8888 -p 5000:5000 -p 6379:6379 -p 9181:9181 ${TAG_NAME}:latest


