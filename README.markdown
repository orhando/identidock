Identidock with Docker
===================

This is very little micro service example with deveoped with docker and python.
There 3 services. 
Main services which listens port 5000 of localhost.
Redis service
Ident creattion service on port 8080


Build docker
============
docker-compose up --build -d


Delete & Build Docker
=====================
docker rm $(docker stop $(docker ps -q)) ; docker-compose up --build -d



Installing/Configuring
======================

To install docker [https://www.docker.com/products/overview]


Run on Browser
======================
http://localhost:5000

