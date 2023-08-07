#!/bin/bash


docker-compose -f docker-compose-prod-init.yml --env-file .env-cert.prod up --build

echo "Initialization complete!"

docker-compose -f docker-compose-prod.yml --env-file .env.prod up --build