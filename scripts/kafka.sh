# Build, tag and push the docker image for the kafka broker

docker build -t kafka modules/kafka
docker tag kafka ap84gray/kafka:latest
docker push ap84gray/kafka:latest
