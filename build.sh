#!/bin/bash

docker compose -f docker/compose-dev.yaml down
# docker system prune -f
docker builder prune -f
docker rmi audibleismissing-dev:latest
docker compose -f docker/compose-dev.yaml up


# docker exec -it audibleismissing-dev sh