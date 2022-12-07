# Build, tag and push the docker image for the connection api

docker build -t connection-api modules/connection
docker tag connection-api ap84gray/connection-api:latest
docker push ap84gray/connection-api:latest


