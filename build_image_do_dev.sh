#!/bin/bash

project_name='pricing-api'
environment='dev'
registry_name='irr-calc-backend'
redis_url='redis://localhost:6379'

PROJECT_NAME=${project_name}
ENV_BUILD=${environment}
TAG_NAME=${project_name}-${environment}
REGISTRY_NAME=${registry_name}
REDIS_URL=${redis_url}

docker build --squash -t ${TAG_NAME} -f Dockerfile \
  --build-arg PROJECT_NAME=${PROJECT_NAME} \
  --build-arg ENV_BUILD=${ENV_BUILD} \
  --build-arg REDIS_URL=${REDIS_URL} \
  --build-arg PYTHON_VERSION_TAG=3.8.6 \
  --build-arg LINK_PYTHON_TO_PYTHON3=1 .

#Use the docker tag command to tag your image with the fully qualified destination path:
docker tag ${TAG_NAME} registry.digitalocean.com/${REGISTRY_NAME}/${PROJECT_NAME}
#Use the docker push command to upload your image:
#docker push registry.digitalocean.com/${REGISTRY_NAME}/${PROJECT_NAME}

