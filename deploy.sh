#!/bin/bash

#!/bin/bash

docker-compose -f docker-compose.prod-init.yml --env-file env-cert.prod up --build -d 
docker-compose -f docker-compose-prod.yml --env-file .env.prod up --build -d