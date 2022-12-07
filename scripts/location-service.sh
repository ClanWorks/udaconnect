# Build, tag and push the docker image for the kafka consumer/location service

docker build -t uda-location-service modules/location_service
docker tag uda-location-service ap84gray/uda-location-service:latest
docker push ap84gray/uda-location-service:latest
