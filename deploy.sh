#!/bin/bash

docker build --build-arg USER=$USER --build-arg UID=$UID --build-arg GID=$GID -t sirimullalab/redial-2020-website:v1.5 .
docker run -p 8000:8000 sirimullalab/redial-2020-website:v1.5