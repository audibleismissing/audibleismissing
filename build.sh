#!/bin/bash

docker compose -f docker/compose-dev.yaml down
# docker system prune -f
docker builder prune -f
docker rmi docker-audibleismissing-dev:latest
docker compose -f docker/compose-dev.yaml up --watch


# docker exec -it audibleismissing-dev sh