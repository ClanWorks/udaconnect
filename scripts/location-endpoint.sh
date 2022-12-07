# Build, tag and push the docker image for the kafka producer

docker build -t uda-location-endpoint modules/location_endpoint
docker tag uda-location-endpoint ap84gray/uda-location-endpoint:latest
docker push ap84gray/uda-location-endpoint:latest
