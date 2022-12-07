# Build, tag and push the docker image for the person api

docker build -t person-api modules/person
docker tag person-api ap84gray/person-api:latest
docker push ap84gray/person-api:latest


