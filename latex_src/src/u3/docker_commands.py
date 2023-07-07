#lists all images
docker image ls                     
#lists all containers
docker ps -a               

#stops all containers
docker stop $(docker ps -a -q)      
#deletes all containers
docker rm $(docker ps -a -q)
#deletes all images
docker rmi -f $(docker images -a -q)      

#builds images of docker_compose.yml
docker-compose build                
#creates containers of docker_compose.yml in detached mode and overwrites old images
docker-compose up -d --force-recreate
#deletes all images and containers created by last docker-compose up call            
docker-compose down                 

#save image file
docker save -o <path for generated tar file> <image name>
#load image file
docker load -i <path to image tar file>