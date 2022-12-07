# Build, tag and push the docker image for the frontend app

docker build -t uda-old-frontend modules/frontend
docker tag uda-old-frontend ap84gray/uda-old-frontend:latest
docker push ap84gray/uda-old-frontend:latest


